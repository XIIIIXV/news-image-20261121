# Saturday 21 November 2026 — The World in One Page

[![Competition](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![Rank](https://make.fun/badge/news-image-20261121/XIIIIXV/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![Reward](https://make.fun/badge/news-image-20261121/XIIIIXV/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

Entry for the make.fun bounty
[news-image-20261121 — "Sum up 21 November's world news in one image"](https://make.fun/bounty/news-image-20261121).

One page, 36 stories, 8 regions — every fact date-checked to Saturday
21 November 2026. Three illustrated leads (Bahrain, Riyadh, Junín),
ten more illustrated cards, a UTC timeline, a numbered world map,
a day-in-numbers strip, and a DATE CHECK strip naming the 19/20 November
stories left out on purpose and the 22 November stories that had not
happened yet.

## How it runs

`main.py` copies the pre-rendered `entry.png` into
`$MAKEFUN_OUTPUT_DIR`. It renders nothing and writes nothing into the
repository directory.

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`gen_real.py` is the deterministic PIL generator that drew `entry.png`
(1024×1024, 155,444 bytes). Running it twice produces byte-identical
output (SHA-256 `c0092a59c5ba7df949c0fd8e0cdbc3ebf94cc079a9e169ac80a2e1aa2adb4d42`).

## License

MIT — see `LICENSE`.
