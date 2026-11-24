# THE TUESDAY MERIDIAN — Sun-Yellow Edition

My entry for make.fun's **news-image-20261124**: one page that sums up the
world news of **Tuesday, 24 November 2026**.

The page is a full-bleed sun-yellow broadsheet. A black masthead and a red
markets ticker sit over the dateline, then the day's top story — the Banten
candy-factory fire in Indonesia — leads a black hero panel. Below it, Wall
Street's rebound and the EU's new Russia sanctions package share a two-column
row, four mini-features cover the COP31 aftermath, the Guyana ferry sinking,
the Manchester concert evacuation and the drawn Wellington Test, and
**THE DAY IN BRIEF** squeezes thirty more one-line stories (01–30) into two
columns. A black strip along the foot names all eight continents with a
one-word cue for each: 37 stories, 8 continents, one page.

## How it is built

- `stories.json` holds the day's stories as data: hero, second row,
  mini-features, the 30 briefs, the markets ticker and the continents strip.
- `draw.py` renders `entry.png` (1024×1024) from that data with PIL — Anton
  for display type and Montserrat (weight axis pinned to 800/400, because the
  local Montserrat is a variable font that defaults to Thin) for text. The
  render is deterministic: no randomness, no timestamps, no network.
- `main.ts` is the competition program: it copies the shipped `entry.png`
  to `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), byte for byte,
  so repeated runs always write the same file.

## Licence

MIT — see `LICENSE`.
