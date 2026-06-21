#!/usr/bin/env python3
"""
check_audio.py
Verifies that every audio file in /audio/ corresponds to a dictionary entry.
Flags any orphan files or misnamed files.
"""
import json, os, sys

with open('dictionary.json', encoding='utf-8') as f:
    dictionary = json.load(f)

# Build set of expected filenames from dictionary
expected = {entry['audio'].split('/')[-1] for entry in dictionary if entry.get('audio')}

# Get actual files in audio/ folder
audio_dir = 'audio'
actual = set()
if os.path.isdir(audio_dir):
    actual = {f for f in os.listdir(audio_dir) if f.endswith('.mp3') or f.endswith('.webm') or f.endswith('.ogg')}

orphans = actual - expected
missing_in_dict = expected - actual  # files expected but not uploaded yet (normal)

errors = []

if orphans:
    errors.append(f"⚠️  Orphan audio files (not in dictionary): {sorted(orphans)}")
    errors.append("   These files don't match any dictionary entry filename.")
    errors.append("   Check spelling or update dictionary.json accordingly.")

if errors:
    for e in errors:
        print(e)
    sys.exit(1)
else:
    print(f"✅ Audio check passed.")
    print(f"   {len(actual)} audio files uploaded.")
    print(f"   {len(expected) - len(actual)} words still need audio.")
    if actual:
        print(f"   Latest additions: {sorted(actual)[-5:]}")
