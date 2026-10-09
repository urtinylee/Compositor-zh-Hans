#!/usr/bin/env python3
"""Build the 1.4.8 Chinese fork using the compatible command-line SDK."""
from pathlib import Path
import subprocess, plistlib
root = Path(__file__).resolve().parent.parent
build = root / 'build'
build.mkdir(exist_ok=True)
# Artwork can come from either same-version installed edition.
original = None
for app_path, expected_id in [('/Applications/Compositor.app', 'com.wonderassembly.compositor'),
                              ('/Applications/Compositor 简体中文.app', 'com.wonderassembly.compositor.zhHans')]:
    candidate = Path(app_path) / 'Contents'
    if not (candidate / 'Info.plist').is_file():
        continue
    candidate_info = plistlib.loads((candidate / 'Info.plist').read_bytes())
    if (candidate_info.get('CFBundleIdentifier') == expected_id
            and candidate_info.get('CFBundleShortVersionString') == '1.4.8'
            and all((candidate / 'Resources' / asset).is_file() for asset in ['Assets.car', 'AppIcon.icns'])):
        original, original_info = candidate, candidate_info
        break
if original is None:
    raise SystemExit('Install Compositor 1.4.8 (official or Chinese edition) before building this patch.')
sdk = '/Library/Developer/CommandLineTools/SDKs/MacOSX26.5.sdk'
objs=[]
for c in sorted((root/'Compositor').rglob('*.c')):
    obj=build/(c.stem+'.o')
    subprocess.run(['xcrun','clang','-target','arm64-apple-macos26.0','-isysroot',sdk,'-O3','-c',str(c),'-o',str(obj)],check=True)
    objs.append(str(obj))
(build/'localization').mkdir(exist_ok=True)
cmd=['xcrun','swiftc','-O','-whole-module-optimization','-swift-version','5','-default-isolation','MainActor','-enable-upcoming-feature','MemberImportVisibility','-enable-upcoming-feature','NonisolatedNonsendingByDefault','-enable-upcoming-feature','InferIsolatedConformances','-target','arm64-apple-macos26.0','-sdk',sdk,'-import-objc-header',str(root/'Compositor/Compositor-Bridging-Header.h'),'-Xlinker','-rpath','-Xlinker','@executable_path/../Frameworks','-emit-localized-strings','-emit-localized-strings-path',str(build/'localization'),'-o',str(build/'Compositor')]
cmd += [str(p) for p in sorted((root/'Compositor').rglob('*.swift'))]+objs
subprocess.run(cmd,check=True)

# Assemble a fresh local bundle; the original app supplies the same-version compiled artwork.
import plistlib,shutil
subprocess.run(['python3',str(root/'scripts/generate-localization.py')],check=True)
app=build/'Compositor 简体中文.app'
if app.exists():
    if app.parent!=build: raise ValueError('Unexpected build bundle path')
    shutil.rmtree(app)
contents=app/'Contents'
(contents/'MacOS').mkdir(parents=True)
(contents/'Resources').mkdir()
shutil.copy2(build/'Compositor',contents/'MacOS/Compositor')
for asset in ['Assets.car','AppIcon.icns']:
    shutil.copyfile(original/'Resources'/asset,contents/'Resources'/asset)
shutil.copytree(root/'Compositor/zh-Hans.lproj',contents/'Resources/zh-Hans.lproj')
info=original_info.copy()
info.update(CFBundleIdentifier='com.wonderassembly.compositor.zhHans',
            CFBundleName='Compositor 简体中文',CFBundleDisplayName='Compositor 简体中文',
            CFBundleShortVersionString='1.4.8',CFBundleVersion='43.2',
            CFBundleLocalizations=['en','zh-Hans'],CFBundleDevelopmentRegion='en',
            SUEnableAutomaticChecks=False,SUAutomaticallyUpdate=False,
            LSMinimumSystemVersion='26.0')
for key in ['SUFeedURL','SUPublicEDKey','SUEnableInstallerLauncherService']:info.pop(key,None)
(contents/'Info.plist').write_bytes(plistlib.dumps(info,sort_keys=False))
subprocess.run(['codesign','--force','--sign','-','--options','runtime','--entitlements',str(root/'Config/Compositor.entitlements'),str(app)],check=True)
subprocess.run(['codesign','--verify','--deep','--strict',str(app)],check=True)
print(f'BUILT: {app}')
