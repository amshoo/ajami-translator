#!/usr/bin/env python3
"""
report_coverage.py
Reports audio coverage statistics per category.
Runs as part of CI to show progress in PR comments.
"""
import json, os
from collections import defaultdict

with open('dictionary.json', encoding='utf-8') as f:
    dictionary = json.load(f)

audio_dir = 'audio'
uploaded = set()
if os.path.isdir(audio_dir):
    uploaded = {f for f in os.listdir(audio_dir)
                if f.endswith(('.mp3', '.webm', '.ogg'))}

# Count by category
by_cat = defaultdict(lambda: {'total': 0, 'done': 0})
for entry in dictionary:
    cat = entry.get('cat', 'Unknown')
    filename = entry.get('audio', '').split('/')[-1]
    by_cat[cat]['total'] += 1
    if filename in uploaded:
        by_cat[cat]['done'] += 1

total = len(dictionary)
done = sum(1 for e in dictionary if e.get('audio','').split('/')[-1] in uploaded)
pct = round(done / total * 100, 1) if total else 0

print(f"\n🎙️  Hausa Ajami Audio Coverage Report")
print(f"{'='*45}")
print(f"Total words:     {total}")
print(f"With audio:      {done}  ({pct}%)")
print(f"Still needed:    {total - done}")
print(f"\nBy category:")
for cat, counts in sorted(by_cat.items()):
    bar_len = int(counts['done'] / counts['total'] * 20) if counts['total'] else 0
    bar = '█' * bar_len + '░' * (20 - bar_len)
    print(f"  {cat:<14} [{bar}] {counts['done']}/{counts['total']}")
print()
