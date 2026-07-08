# Daily GitHub Maker

This repo makes one small creative commit every day.

It uses a GitHub Actions schedule to run `scripts/daily_maker.py`, which writes a tiny, deterministic artifact into `daily/` and updates `index.md`. The workflow commits and pushes the change back to the repository.

## What It Creates

Each day gets a small Markdown file with:

- a tiny app idea
- a color palette
- starter HTML/CSS/JS
- a quick build note

The output is intentionally small so the repo grows steadily without becoming noisy.

## Turn It On

1. Create a GitHub repository for this folder.
2. Push this repo to GitHub.
3. In GitHub, go to `Settings -> Actions -> General`.
4. Under `Workflow permissions`, choose `Read and write permissions`.
5. Make sure `Allow GitHub Actions to create and approve pull requests` is not required for this workflow.

The schedule runs every day at 9:17 AM UTC. You can also start it manually from the `Actions` tab by running **Daily Maker Commit**.

## Run Locally

```bash
python scripts/daily_maker.py
git add daily index.md
git commit -m "Add daily maker entry"
```
