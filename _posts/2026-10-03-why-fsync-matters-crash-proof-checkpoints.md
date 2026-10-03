---
layout: post
title: "Why fsync Matters: Crash-Proof Checkpoints"
date: 2026-10-03 14:50 +0530
categories: [Physics, Computing]
tags: [simulations, cpp, posix, storage]
---

In my [last post]({% post_url 2026-10-02-binary-io-for-simulations-in-modern-cpp %}), we used `std::ofstream` to dump trajectory frames. `trajectory.bin` is append-only, so a crash is forgiving: earlier frames are safe on disk, and the partial tail is easily truncated.

Checkpoints are far less forgiving. Unlike a trajectory (paired with `metadata.json`), a checkpoint must contain everything needed to resume. We can embed the metadata at the start of the file:

```cpp
struct Header {
    uint64_t step;
    float box_x, box_y;
    uint32_t num_particles;
    // RNG state, etc.
};
```

A naive first attempt looks innocent enough. Just write the header, dump the particle buffer, and call it a day. In standard C++, that takes only a couple of lines:

```cpp
std::ofstream out("checkpoint.bin", std::ios::binary);
out.write(reinterpret_cast<const char*>(&header), sizeof(Header));
out.write(reinterpret_cast<const char*>(frame.data()), frame.size_bytes());
```

Back in my C days, saving state seemed trivial: just `fopen` and dump the bytes. Then a cluster node killed my job mid-write, leaving a zero-byte file and three days of wasted compute. My workaround was two files: one to save, one to load.

`std::ofstream` has the exact same trap: opening it truncates the existing file by default. Naturally, the next attempt is writing to a `.tmp` file and renaming it—a cleaner version of that same two-file idea:

```cpp
std::ofstream out("checkpoint.bin.tmp", std::ios::binary);
out.write(reinterpret_cast<const char*>(&header), sizeof(Header));
out.write(reinterpret_cast<const char*>(frame.data()), frame.size_bytes());
out.close();  // flushes to OS page cache, not disk!

std::filesystem::rename("checkpoint.bin.tmp", "checkpoint.bin");
```

This looks safe at first, but closing or flushing only pushes bytes to the operating system's memory cache, not to physical storage.[^1] If the power cuts, those unwritten bytes disappear, leaving a zero-byte file on reboot.

To guarantee bytes are physically on disk before renaming, we need POSIX `fsync`. But C++ `ofstream` hides the underlying file handle.[^2]

The cleanest solution is wrapping a C `FILE*` with a [smart pointer](https://educatedguesswork.org/posts/memory-management-3/) and writing with `std::fwrite`:

```cpp
using FileHandle = std::unique_ptr<FILE, decltype(&std::fclose)>;

const std::string tmp = path + ".tmp";
FileHandle f(std::fopen(tmp.c_str(), "wb"), &std::fclose);
if (!f) throw std::runtime_error("open failed: " + tmp);

std::fwrite(&header, sizeof(Header), 1, f.get());
std::fwrite(frame.data(), sizeof(pos), N, f.get());
std::fflush(f.get());
if (::fsync(::fileno(f.get())) != 0)
    throw std::runtime_error("fsync failed: " + tmp);

f.reset();  // close file handle before rename

std::filesystem::rename(tmp, path);  // needs C++17
```

Once `fsync`[^3] confirms the bytes are physically on disk, `rename` swaps the temporary file into place atomically.[^4] It is physically impossible to end up with a half-written checkpoint.

There is one more loose end. If the simulation crashed between checkpoints, the trajectory likely contains extra frames or a half-written tail. Before resuming, we can roll it back to match the checkpoint:

```cpp
const size_t target_bytes = frames_to_keep * frame_bytes;
if (std::filesystem::file_size(path) > target_bytes) {
    std::filesystem::resize_file(path, target_bytes);
}
```

With the checkpoint guaranteed intact and the trajectory rewound, the simulation resumes from the last known good state without a hitch.

Thinking through all this was a good reality check. Writing to a temp file and renaming it is only half the battle. Without `fsync` to flush those bytes to physical storage, the crash-proofing is not robust.

Modern C++ gives us clean abstractions for almost everything, but when durability is on the line, good old POSIX `fsync` is still undefeated.

[^1]: `out.flush()` or `fflush()` only flushes user buffers to the OS page cache. The kernel writes dirty pages to disk on its own lazy schedule; `fsync` forces that write immediately.
[^2]: ISO C++ abstracts away physical hardware, so `std::ofstream` completely encapsulates the OS file descriptor (`int fd`) with no portable way to extract it. C's `FILE*` exposes it directly via `fileno()`.
[^3]: `fsync()` and `fileno()` are POSIX system functions from `<unistd.h>`, not part of the ISO C++ standard. The leading `::` specifies the global namespace rather than `std::`.
[^4]: In POSIX, `rename()` within the same filesystem is an atomic directory update. The file path always points to either the old checkpoint or the new one — never a half-written file.
