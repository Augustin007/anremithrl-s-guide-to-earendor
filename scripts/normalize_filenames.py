from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path('guide-to-earendor')

def normalize(name: str) -> str:
    name = name.lower()
    name = re.sub(r'\s+', '-', name)
    name = re.sub(r'[^a-z0-9\-\.]', '', name)
    return name

for path in sorted(ROOT.rglob('*'), reverse=True):
    if path.name.startswith('.'):
        continue

    new_name = normalize(path.name)
    if path.name != new_name:
        new_path = path.with_name(new_name)
        if not new_path.exists():
            path.rename(new_path)

