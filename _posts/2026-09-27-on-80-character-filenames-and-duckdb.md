---
layout: post
title: "On 80-Character Filenames and DuckDB"
date: 2026-09-27 14:30 +0530
categories: [Physics, Computing]
tags: [simulations, duckdb, bash]
---

For years, my simulation workflow relied on a time-honored habit: **putting every parameter directly into the output filename.**

There is an undeniable, straightforward logic to it. You open a directory and see every physical variable at a single glance without having to inspect any files:

```terminal
$ ls coords_unfold*.txt
coords_unfold_ptlno262144_boxlx557.19_boxly482.54_density0.9750_gamma1.0_temp1.00.txt
coords_unfold_ptlno262144_boxlx557.19_boxly482.54_density0.9750_gamma1.0_temp1.10.txt
coords_unfold_ptlno262144_boxlx558.62_boxly483.78_density0.9700_gamma1.0_temp1.00.txt
coords_unfold_ptlno262144_boxlx558.62_boxly483.78_density0.9700_gamma1.0_temp1.10.txt
...
```

It gets the job done, but as parameter grids grew, the trade-offs became noticeable:
* Listing files produced an overwhelming wall of identical-looking text.
* Tab completion halted on box dimensions, forcing clumsy wildcards.
* Filtering runs meant writing brittle `grep` chains in bash scripts:

```bash
for f in $(ls | grep "density0.9700" | grep "temp1.00"); do
  ./analyze "$f"
done
```

Then there was the storage cost: saving coordinates as plain text `.txt` files burned gigabytes of disk space formatting 4-byte floats into bulky ASCII strings.

The first step was separating the two: organizing runs into simple folders and writing coordinates as raw binary streams (`trajectory.bin` at 8 bytes per particle per frame):

```plaintext
data/
└── rho0.970/
    ├── temp1.00/
    │   ├── metadata.json
    │   ├── trajectory.bin
    │   └── rdf.csv
    └── temp1.10/
        ├── metadata.json
        └── trajectory.bin
```

No ASCII overhead, no rounding errors, no 80-character filenames.

The harder part was bookkeeping: *Which runs actually finished? Which crashed halfway through?* (In the text-file era, the only clue was usually a file with suspiciously fewer lines than its neighbors.)

The textbook engineering answer is to use a database, but that felt like overkill just to track simulation runs—I wanted to do physics, not babysit one. The compromise was keeping a small `metadata.json` in each folder to record state:

```json
{
  "status": "COMPLETED",
  "density": 0.970,
  "temperature": 1.0,
  "num_particles": 262144
}
```
{: file='metadata.json'}

Pointing **[DuckDB](https://duckdb.org)** at these files was the missing piece. Because it can run SQL directly over raw files on disk, checking on an entire grid of simulations takes just one query—no database to manage, no importing:

```sql
SELECT 
    parse_dirpath(m.filename) AS run_dir,
    m.status,
    if(r.file IS NOT NULL, '✓', '-') AS has_rdf,
    m.density,
    m.temperature
FROM read_json_auto('data/**/metadata.json', filename=true) m
LEFT JOIN glob('data/**/rdf.csv') r
  ON replace(m.filename, 'metadata.json', 'rdf.csv') = r.file;
```
{: file='query.sql'}

In a single query, DuckDB crawls the folders with `read_json_auto`, checks for existing analysis files with `glob`, and uses a `LEFT JOIN` to flag which runs still need an `rdf.csv`[^1]. Running it gives an instant overview:

```terminal
$ duckdb < query.sql
┌────────────────────────┬───────────┬─────────┬─────────┬─────────────┐
│        run_dir         │  status   │ has_rdf │ density │ temperature │
├────────────────────────┼───────────┼─────────┼─────────┼─────────────┤
│ data/rho0.970/temp1.00 │ COMPLETED │    ✓    │   0.970 │         1.0 │
│ data/rho0.970/temp1.10 │ COMPLETED │    -    │   0.970 │         1.1 │
│ data/rho0.975/temp1.00 │  RUNNING  │    -    │   0.975 │         1.0 │
└────────────────────────┴───────────┴─────────┴─────────┴─────────────┘
``` 

Even better, this isn't just a terminal party trick. You can run the exact same query in Python (`duckdb.sql(...)`)—filtering runs for a plot, or picking up trajectories that still need an RDF without having to glob through folders and check files by hand.

I haven't settled on every detail of this workflow yet, but the basic idea feels right: keep the heavy physics in simple binaries, keep the bookkeeping in small JSON files, and let DuckDB tie them together. 

P.S. If you ever catch yourself writing a bash script that pipes `ls` into three consecutive `grep` filters just to find a temperature point, consider this an intervention.

[^1]: This only checks whether the file exists. If you ever extend a simulation, you'd also want to compare file timestamps to see if the RDF is stale.
