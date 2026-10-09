#!/usr/bin/env python3
"""Package the already-built Chinese application for public distribution."""
from pathlib import Path
import plistlib
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parent.parent
APP_NAME = "Compositor 简体中文.app"
BUNDLE_ID = "com.wonderassembly.compositor.zhHans"


def run(*args):
    subprocess.run(args, check=True)


def main():
    source = ROOT / "build" / APP_NAME
    info = plistlib.loads((source / "Contents/Info.plist").read_bytes())
    if info.get("CFBundleIdentifier") != BUNDLE_ID or info.get("CFBundleShortVersionString") != "1.4.8":
        raise SystemExit("Build the Compositor 1.4.8 Chinese app before packaging.")
    run("codesign", "--verify", "--deep", "--strict", str(source))
    staging = ROOT / "build/release-package"
    if staging.exists():
        # Only this script's disposable staging directory is replaced.
        if staging.parent != ROOT / "build":
            raise ValueError("Unexpected staging directory")
        shutil.rmtree(staging)
    payload = staging / "payload"
    payload.mkdir(parents=True)
    app = payload / APP_NAME
    run("ditto", str(source), str(app))
    resources = app / "Contents/Resources"
    shutil.copyfile(ROOT / "LICENSE", resources / "LICENSE.txt")
    shutil.copyfile(ROOT / "NOTICE", resources / "NOTICE.txt")
    shutil.copyfile(ROOT / "docs/INSTALL.zh-CN.md", resources / "INSTALL.zh-CN.md")
    info["CFBundleVersion"] = "43.1"
    (app / "Contents/Info.plist").write_bytes(plistlib.dumps(info, sort_keys=False))
    run("codesign", "--force", "--sign", "-", "--options", "runtime", "--entitlements", str(ROOT / "Config/Compositor.entitlements"), str(app))
    run("codesign", "--verify", "--deep", "--strict", str(app))
    component_plist = staging / "components.plist"
    run("pkgbuild", "--analyze", "--root", str(payload), str(component_plist))
    components = plistlib.loads(component_plist.read_bytes())
    if len(components) != 1 or components[0]["RootRelativeBundlePath"] != APP_NAME:
        raise SystemExit("Unexpected installer payload")
    components[0].update(BundleIsRelocatable=False, BundleHasStrictIdentifier=True,
                         BundleIsVersionChecked=True, BundleOverwriteAction="upgrade")
    component_plist.write_bytes(plistlib.dumps(components))
    component = staging / "Compositor-zh-Hans-component.pkg"
    run("pkgbuild", "--root", str(payload), "--component-plist", str(component_plist),
        "--identifier", "io.github.urtinylee.compositor.zhHans", "--version", "1.4.8.1",
        "--install-location", "/Applications", "--ownership", "recommended", "--scripts",
        str(ROOT / "packaging/scripts"), str(component))
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    package = dist / "Compositor-1.4.8-zh-Hans.pkg"
    run("productbuild", "--distribution", str(ROOT / "packaging/Distribution.xml"),
        "--package-path", str(staging), "--resources", str(ROOT / "packaging/resources"), str(package))
    archive = dist / "Compositor-1.4.8-zh-Hans-app.zip"
    # Standard UTF-8 names and Unix executable permissions; no AppleDouble metadata.
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(app, APP_NAME + "/")
        for path in sorted(app.rglob("*")):
            if path.is_symlink():
                raise ValueError("Unexpected symlink in standalone app")
            z.write(path, APP_NAME + "/" + str(path.relative_to(app)))
    shutil.copyfile(ROOT / "docs/INSTALL.zh-CN.md", dist / "INSTALL.zh-CN.md")
    shutil.copyfile(ROOT / "LICENSE", dist / "LICENSE.txt")
    print(f"INSTALLER: {package}")


if __name__ == "__main__":
    main()
