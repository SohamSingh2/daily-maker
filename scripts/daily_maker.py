from __future__ import annotations

import datetime as dt
import hashlib
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DAILY_DIR = ROOT / "daily"
INDEX = ROOT / "index.md"

APP_TYPES = [
    "focus timer",
    "mood tracker",
    "micro journal",
    "habit spark",
    "quote shuffler",
    "tiny budget board",
    "recipe picker",
    "study sprint tool",
    "stretch reminder",
    "daily wins log",
]

MOODS = [
    "quiet and crisp",
    "bright but calm",
    "midnight dashboard",
    "paper notebook",
    "retro terminal",
    "soft arcade",
    "clean studio",
    "warm command center",
]

FEATURES = [
    "one-click reset",
    "localStorage persistence",
    "keyboard shortcuts",
    "random prompt generation",
    "copy-to-clipboard",
    "progress rings",
    "daily streak tracking",
    "editable cards",
    "compact mobile layout",
    "export as plain text",
]

PALETTES = [
    ("#101820", "#f2aa4c", "#f7f7f2"),
    ("#17252a", "#3aafa9", "#def2f1"),
    ("#2d3047", "#fffd82", "#ff9b71"),
    ("#1b1b3a", "#693668", "#a74482"),
    ("#0b132b", "#5bc0be", "#f4f1de"),
    ("#262322", "#ddc9b4", "#f0f7ee"),
    ("#0f1a20", "#c2f970", "#ffffff"),
    ("#202c39", "#f29559", "#ead2ac"),
]

VERBS = [
    "sketch",
    "sort",
    "capture",
    "nudge",
    "collect",
    "shape",
    "stack",
    "track",
]


def seeded_random(day: dt.date) -> random.Random:
    digest = hashlib.sha256(day.isoformat().encode("utf-8")).hexdigest()
    return random.Random(int(digest[:16], 16))


def titleize(value: str) -> str:
    return " ".join(piece.capitalize() for piece in value.split())


def build_entry(day: dt.date) -> tuple[str, str]:
    rng = seeded_random(day)
    app_type = rng.choice(APP_TYPES)
    mood = rng.choice(MOODS)
    features = rng.sample(FEATURES, 3)
    palette = rng.choice(PALETTES)
    verb = rng.choice(VERBS)
    title = f"{titleize(verb)} {titleize(app_type)}"
    slug = day.isoformat()

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    body {{
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      background: {palette[0]};
      color: {palette[2]};
      font-family: system-ui, sans-serif;
    }}
    main {{
      width: min(34rem, calc(100% - 2rem));
      border: 1px solid {palette[1]};
      border-radius: 8px;
      padding: 1.25rem;
    }}
    button {{
      border: 0;
      border-radius: 6px;
      padding: 0.7rem 0.9rem;
      background: {palette[1]};
      color: {palette[0]};
      font-weight: 700;
    }}
  </style>
</head>
<body>
  <main>
    <h1>{title}</h1>
    <p>A {mood} {app_type} with {features[0]}, {features[1]}, and {features[2]}.</p>
    <button id="spark">Make today count</button>
    <p id="out"></p>
  </main>
  <script>
    const notes = ["Start tiny.", "Ship the useful bit.", "Make it pleasant."];
    spark.onclick = () => out.textContent = notes[Math.floor(Math.random() * notes.length)];
  </script>
</body>
</html>"""

    markdown = f"""# {title}

Date: {day.isoformat()}

Tiny app concept: a {mood} **{app_type}**.

Core touches:

- {features[0]}
- {features[1]}
- {features[2]}

Palette:

- Background: `{palette[0]}`
- Accent: `{palette[1]}`
- Text: `{palette[2]}`

Starter file:

```html
{html}
```

Build note: keep the first version under one screen and make the primary action obvious.
"""

    return slug, markdown


def update_index(day: dt.date, slug: str) -> None:
    entries = sorted(DAILY_DIR.glob("*.md"), reverse=True)
    lines = [
        "# Daily GitHub Maker Index",
        "",
        "Small generated ideas, one day at a time.",
        "",
    ]
    for entry in entries:
        label = entry.stem
        lines.append(f"- [{label}](daily/{entry.name})")
    lines.append("")
    lines.append(f"Last generated: {day.isoformat()}")
    lines.append("")
    INDEX.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    today = dt.datetime.now(dt.timezone.utc).date()
    DAILY_DIR.mkdir(exist_ok=True)

    slug, markdown = build_entry(today)
    entry_path = DAILY_DIR / f"{slug}.md"
    entry_path.write_text(markdown, encoding="utf-8")
    update_index(today, slug)

    print(f"Wrote {entry_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
