# The World Today — 19 November 2026

A one-image summary of 19 November 2026's world news, drawn as a classic
newspaper front page: a large masthead, a clear date line, one lead story
and three supporting stories.

Stories covered: the Trump–Xi–Putin trilateral summit in Shenzhen; the
global rollout of GTA VI; Anthropic's record $81.3bn IPO; and NASA's
Voyager 1 reaching one light-day from Earth.

## How it works

- `generate.py` draws `entry.png` (1024×1024) with Pillow. Run it locally
  whenever the artwork is changed.
- `main.py` (Python 3.13, standard library only) copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png`, so repeated runs are byte-identical.

## Run

```sh
python3 generate.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```
