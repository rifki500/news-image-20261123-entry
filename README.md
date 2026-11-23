# The World Today — Monday 23 November 2026

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/rifki500/news-image-20261123-entry/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/rifki500/news-image-20261123-entry/reward.svg)](https://make.fun/bounty/news-image-20261123)

A one-day world news front page for [news-image-20261123](https://make.fun/bounty/news-image-20261123)
on make.fun: **The World Today**, summing up Monday 23 November 2026 in a
single 1024x1024 image — 35 stories across 8 regions, from the collapse of
the COP31 climate talks in Antalya to Nvidia bringing back Jensen Huang.

## How it works

`main.py` (Python 3, standard library only) draws the whole front page from
scratch: a hand-written 5x7 bitmap font, a small canvas, and a hand-rolled
PNG encoder. No network, no files read, no timestamps anywhere — two runs
write byte-identical output.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

## The day in brief

- **Hero — Climate:** COP31 collapses in Antalya: no deal, as the fossil-fuel
  fight sinks the talks; the longest climate summit ever.
- **Markets:** Nvidia reinstates Jensen Huang as CEO; shares soar 30%, S&P 500
  +4.8%.
- **Middle East:** Iran vows to fight the US blockade; Trump warns strikes
  could resume.
- **Ukraine:** Zelenskyy confirms Ukraine hit a Russian warship in Libya's
  Benghazi port.
- **Americas:** Democrats take their largest House majority since 1992.

Plus 30 briefs in three columns: the Dymer and Kryvyi Rih strikes, NATO and
Poland, the capture of "Chapo Isidro", ICE arrests in Seattle, India's
$1.62bn pledge to Nepal, South Korea's cabinet reshuffle, Kenya and DR Congo
restoring ties, the SEC's Nvidia probe, and the NFL's Sunday scores.

Sources: BBC, Reuters, AP, NYT, NPR, WSJ, Al Jazeera, Axios, WIRED,
OkayAfrica — all stories as reported on 23 November 2026.

## License

MIT — see [LICENSE](LICENSE).
