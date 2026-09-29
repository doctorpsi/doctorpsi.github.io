---
layout: post
title: "How to Read Binary Files with NumPy"
date: 2026-09-30 16:43 +0530
categories: [Physics, Computing]
tags: [simulations, python, numpy]
---

[Last time]({% post_url 2026-09-27-on-80-character-filenames-and-duckdb %}) I swapped ASCII `.txt` files for a raw `trajectory.bin`
— 8 bytes per particle per frame. That begs the obvious question:
how do you read it back?

Say we simulated a Lennard-Jones fluid in 2D. That means `N` pairs of `(x, y)` float32 per frame, back-to-back — no spaces, no newlines:

```plaintext
data/
└── rho0.970/
    └── temp1.00/
        ├── metadata.json
        └── trajectory.bin
```

One frame is `N * 2 * 4` bytes. For `N = 262144`, that's exactly
2 MiB. 1000 frames is ~2 GiB — the same data as `.txt` would be
~2-3x larger, slower to parse, and rounded.

The catch: the file doesn't know `N`. We do, from `metadata.json`:

```json
{
  "status": "COMPLETED",
  "density": 0.970,
  "temperature": 1.0,
  "num_particles": 262144
}
```
{: file='metadata.json'}

So we can read the file in two steps — get `N` and `n_frames`[^1], then interpret bytes:

```python
import json, numpy as np
from pathlib import Path

run = Path("data/rho0.970/temp1.00")
meta = json.loads((run / "metadata.json").read_text())
N = meta["num_particles"]

frame_bytes = N * 2 * 4
size = (run / "trajectory.bin").stat().st_size
n_frames = size // frame_bytes  # COMPLETED only
```
{: file='read.py'}

For that second step, we can use
[np.fromfile](https://numpy.org/doc/stable/reference/generated/numpy.fromfile.html):

```python
traj = np.fromfile(run / "trajectory.bin", dtype=np.float32)
traj = traj.reshape(n_frames, N, 2)  # [frame, particle, xy]
x0 = traj[0, :, 0]  # unfolded x at frame 0
```

Load and `reshape` — no parsing, no splitting. Fine for small tests, but it
loads the full 2 GiB into RAM.[^2]

For large runs, we can do better and page it with [np.memmap](https://numpy.org/doc/stable/reference/generated/numpy.memmap.html):

```python
traj = np.memmap(run / "trajectory.bin", dtype=np.float32,
                   mode="r", shape=(n_frames, N, 2))
x0 = traj[0, :, 0]  # unfolded x at frame 0
```

Same shape, same indexing, but the OS loads pages on demand. So grabbing the last frame is just a 2 MiB seek.

I'm curious what the same read will look like in modern C++.

[^1]: A kill mid-write leaves a partial frame at the tail. To catch it explicitly: `n_frames, remainder = divmod(size, frame_bytes); assert remainder == 0` — nonzero means partial.
[^2]: At 10k frames that's ~20 GiB, exceeding typical laptop RAM, where paging wins.
