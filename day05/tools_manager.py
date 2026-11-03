"""Smoke test for read_text_file (run from repo root)."""

from tools import read_text_file

fileText = read_text_file("day05/data/notes.txt")
print(fileText)
