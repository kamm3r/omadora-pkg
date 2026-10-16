#!/usr/bin/env python3
"""Check the spec's usr/ guard against library names shipped by T3 Code 0.1.0."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
for name in ('t3code-bin', 't3code-nightly-bin'):
    spec = (root / 'packages' / name / f'{name}.spec').read_text()
    pattern = re.search(r"unexpected=\$\(find usr .*?grep -vE '([^']+)'", spec)[1]
    # These are real entries from the upstream x86_64 AppImage, including symlinks.
    paths = [
        'usr/lib/libXss.so.1.0.0',
        'usr/lib/libXtst.so.6.1.0',
        'usr/lib/libappindicator3.so.1.0.0',
        'usr/lib/libgconf-2.so.4.1.5',
        'usr/lib/libindicator3.so.7.0.0',
        'usr/lib/libnotify.so.4.0.0',
        'usr/lib/libappindicator3.so.1',
        'usr/lib/libindicator3.so.7',
        'usr/share/icons/hicolor/256x256/apps/t3code.png',
    ]
    for path in paths:
        assert re.search(pattern, path), (name, 'rejects upstream file', path)
    for path in ('usr/bin/helper', 'usr/lib/libunknown.so.1', 'usr/share/config.json'):
        assert not re.search(pattern, path), (name, 'silently discards unknown file', path)
    print(f'PASS: {name} accepts upstream library names and rejects unknown files')
