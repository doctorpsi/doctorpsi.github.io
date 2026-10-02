---
layout: post
title: "Binary I/O for Simulations in Modern C++"
date: 2026-10-02 18:30 +0530
categories: [Physics, Computing]
tags: [simulations, cpp, binary]
---

I left off [last time]({% post_url 2026-09-30-how-to-read-binary-files-with-numpy %}) with a thought in mind. My main simulation code is written in CUDA, and I still do most of the post-processing outside Python.

I'm more of a C guy with minimal C++98 experience. But I've recently started shifting to modern C++. So how would I read — or even write — binary data in C++ these days?

As before, we'll assume the file has `N` `(x, y)` float32 pairs per frame back-to-back and nothing else. Let's consider the write side first. A `pos` is just two floats with no padding:

```cpp
struct pos {
    float x;
    float y;
}; // particle position
```

We can write frame by frame passing a span[^1] of `N` pairs straight to an `ofstream` (opened with `std::ios::binary`)[^2]:

```cpp
void write_frame(std::ofstream& out, std::span<const pos> frame)
{
    out.write(reinterpret_cast<const char*>(frame.data()),
              frame.size_bytes());  // needs C++20
}
```

On the read side, we start with the frame count. A single frame is `N * 2 * 4` bytes, where `N` is the number of particles from a config file[^3]:

```cpp
const size_t frame_bytes = N * sizeof(pos);
const size_t n_frames =
    std::filesystem::file_size(path) / frame_bytes;  // needs C++17
```

A crash mid-write can leave a partial tail but integer division ignores it. We can be a bit smarter and check with `std::filesystem::file_size(path) % frame_bytes != 0` — nonzero means we crashed, so we either truncate or discard the entire run.

We can then stream[^4] frames in batches — say 32 at a time — into a reusable `vector` instead of loading the whole file:

```cpp
std::ifstream in(path, std::ios::binary);
const size_t batch = 32;
std::vector<pos> buf(batch * N);

for (size_t i = 0; i < n_frames; i += batch) {
    const size_t frames = std::min(batch, n_frames - i);
    in.read(reinterpret_cast<char*>(buf.data()), frames * frame_bytes);
    if (in.fail()) throw std::runtime_error("short read: partial frame");
    // process frames in buf...
}
```

And if all we need is the last frame, it's still a 2 MiB seek—just as in NumPy:

```cpp
in.seekg((n_frames - 1) * frame_bytes);
std::vector<pos> last(N);
in.read(reinterpret_cast<char*>(last.data()), frame_bytes);
```

That's all there is, really. Dump frames with `write` (no particle loops), and keep `N` in a config file. Then read in batches or seek when needed.

P.S. As I dug deeper into modern C++, I was genuinely surprised that even in C++26, there is no native equivalent to `np.memmap`. `mmap` is still just a [low-level POSIX call](https://www.youtube.com/watch?v=m7E9piHcfr4) in `<sys/mman.h>`.

[^1]: `std::span` (`<span>` since C++20) is a non-owning view: pointer + size, no copy. A pointer and a size passed separately can disagree; a span cannot, so it's safer: [a short video](https://www.youtube.com/watch?v=-DBCFemT2-U).
[^2]: Unlike C's `fwrite` which takes `const void*` implicitly, `std::ostream::write` expects `const char*` — hence the cast.
[^3]: Last time this was `metadata.json`; a checkpoint header or run config does the same job — anything outside the byte stream.
[^4]: In Python, `np.memmap` uses the OS page cache to load frames on demand. Here, streaming fixed chunks into a reusable buffer achieves the same flat-memory goal.
