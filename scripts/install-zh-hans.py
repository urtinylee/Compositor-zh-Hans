#!/usr/bin/env python3
"""Install the task-built Chinese app without replacing the official app."""
from pathlib import Path
import plistlib,subprocess
root=Path(__file__).resolve().parent.parent
source=root/'build/Compositor 简体中文.app'
target=Path('/Applications/Compositor 简体中文.app')
if not source.is_dir():raise SystemExit('Build the Chinese app first.')
if target.exists():
    info=plistlib.loads((target/'Contents/Info.plist').read_bytes())
    if info.get('CFBundleIdentifier')!='com.wonderassembly.compositor.zhHans':
        raise SystemExit('Target is an unrelated app; installation stopped.')
    raise SystemExit('Chinese app already installed; quit it and move this exact app to Trash before reinstalling.')
subprocess.run(['codesign','--verify','--deep','--strict',str(source)],check=True)
subprocess.run(['ditto',str(source),str(target)],check=True)
subprocess.run(['codesign','--verify','--deep','--strict',str(target)],check=True)
print(f'INSTALLED: {target}')
