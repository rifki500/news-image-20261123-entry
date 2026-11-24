# The World Today — Monday 23 November 2026

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/rifki500/news-image-20261123-entry/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/rifki500/news-image-20261123-entry/reward.svg)](https://make.fun/bounty/news-image-20261123)

A one-day world news front page for [news-image-20261123](https://make.fun/bounty/news-image-20261123)
on make.fun: **The World Today**, summing up Monday 23 November 2026 in a
single 1024×1024 image — 35 stories across 8 regions.

## The day in brief

- **Hero — Business:** Nvidia reinstates Jensen Huang as CEO, 11 days after he
  quit; shares jump 31% — the best day since 2003 — adding $952bn in value,
  and lifting the S&P 500 by 4.7% and the Nasdaq by 6.5%.
- **Global:** COP31 collapses in Antalya — no deal, the longest climate summit
  ever and the first failure since Copenhagen 2009.
- **Middle East:** Ukraine sinks the Russian corvette Merkury off Libya with
  seven sea drones; Iran says it downed a US drone near Hormuz.
- **Europe:** The Dymer rescue ends with a toll of 11; the EU unveils its 22nd
  package of Russia sanctions.
- **Americas:** Democrats clinch 258 House seats, their largest majority since
  1992.

Plus 30 briefs in three columns. Every story was verified against reporting
dated 23 November 2026; stories whose event was earlier but which were first
reported that day are marked † — see [BUILD-LOG.md](BUILD-LOG.md) for the
full story list, sources, caveats and rejected candidates.

## How it works

`main.py` (Python 3, standard library only) copies the finished front page,
`entry.png`, to the output directory. The page itself was drawn with Pillow
(DejaVu fonts, flat vector-style pictograms) from the story list in
`BUILD-LOG.md`. It takes no arguments and reads no files besides the PNG
next to it:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`entry.png` is 1024×1024, 170,239 bytes. Rendering is deterministic: two runs
produce byte-identical output (same sha256 — see BUILD-LOG.md).

## License

MIT — see [LICENSE](LICENSE).
