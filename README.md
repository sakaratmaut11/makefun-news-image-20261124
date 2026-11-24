[![make.fun bounty](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/sakaratmaut11/makefun-news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/sakaratmaut11/makefun-news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124)

Bounty: https://make.fun/bounty/news-image-20261124

# ONE DAY CHRONICLE — Tuesday 24 November 2026 in one image

One front page that sums up Tuesday 24 November 2026: 36 stories across
7 regions, every one dated to the day. Lead stories: New Zealand bat out
a draw with India at Wellington (239/5), Liverpool rout Manchester United
4–0, and Ukraine sinks the Russian warship Merkury off Benghazi with
7 sea drones launched.

## What is in the picture

- Masthead date in full: **Tuesday 24 November 2026**, with a kicker count
  that is honest about the page (36 stories, 7 regions).
- A numbers strip of the day (7 sea drones · 239/5 · 4–0 · COP31 no deal ·
  $3,588 gold · $61,284 Bitcoin · $3.8bn GTA VI · +31% Nvidia) — every
  number ties to a card on the page.
- A colour-coded region strip, a Tuesday timeline in WIB (plus
  Monday-evening wires labelled as reported), and a dotted world map drawn
  from real continent polygons with numbered pins that match story numbers.
- 14 cards, each with a certainty tag and named sources, and a deck of at
  least two facts; 22 numbered ALSO ON briefs continue the numbering.
- A DATE CHECK box names seven stories that are NOT Tuesday's news, with
  their real dates, so nothing stale is sold as today.

## How it is built

`compose_ak17.py` draws the page (Pillow, local run only) at 3900×3900
and downscales it to the 1024×1024 `entry.png` in this repository.
`main.py` is the entrypoint: standard library only, it copies `entry.png`
to the output directory after checking the PNG header is exactly
1024×1024 and the file is at most 1 MiB. Two runs write identical bytes.

## Run

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Pictures and map: original, drawn in code. Original drawings.
