#!/bin/bash

uv run python scripts/update_home_recent.py
uv run python scripts/update_note_counts.py
uv run python scripts/update_timeline.py
uv run python scripts/update_essay_timeline.py
uv run python scripts/update_nav_blog.py
uv run python scripts/update_nav_notes.py
uv run python scripts/update_quiz.py
