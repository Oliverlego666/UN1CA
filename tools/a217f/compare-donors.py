#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Read-only comparison of the extracted S22 and S23 FE donor firmware."""
from pathlib import Path
import hashlib
import xml.etree.ElementTree as ET
import re
import shutil

root = Path(__file__).resolve().parents[2]
fw = root / "out/fw"
old, new = (fw / name for name in ("SM-S901B_EUX", "SM-S711B_EUX"))
for donor in (old, new):
    if not (donor / ".extracted").is_file():
        raise SystemExit(f"Missing extraction marker: {donor}")
    print(f"{donor.name}: {(donor / '.extracted').read_text().strip()}")
    print((donor / "os_partitions_metadata.txt").read_text().strip())

def props(donor):
    result = {}
    for rel in ("system/system/build.prop", "product/etc/build.prop",
                "vendor/build.prop", "odm/etc/build.prop", "system_ext/etc/build.prop",
                "system/system/system_ext/etc/build.prop"):
        path = donor / rel
        if path.is_file() and not path.is_symlink():
            print(f"  {rel}:")
            for line in path.read_text(errors="replace").splitlines():
                if re.match(r"^ro\.(build\.(product|version\.(sdk|oneui|release))|product\.(first_api_level|[^.]+\.(device|name))|board\.(api_level|first_api_level)|vendor\.api_level|product\.cpu\.abilist.*|camerax\.extensions\.enabled)=", line):
                    print("    " + line)
def features(donor):
    path = donor / "system/system/etc/floating_feature.xml"
    if not path.is_file():
        raise SystemExit(f"Missing floating feature XML: {path}")
    return {child.tag: (child.text or "").strip() for child in ET.parse(path).getroot()}
for donor in (old, new):
    print(f"\nPROPERTIES {donor.name}")
    props(donor)
a,b = features(old),features(new)
print("\nCHANGED HARDWARE FLOATING FEATURES")
for key in sorted(a.keys() | b.keys()):
    if a.get(key) != b.get(key) and re.search(r"AUDIO|BLUETOOTH|CAMERA|COMMON|DISPLAY|FINGERPRINT|LCD|RIL|SECURITY|WLAN|SYSTEM_CONFIG_SIOP", key):
        print(f"{key}: {a.get(key, '<absent>')} -> {b.get(key, '<absent>')}")
print("\nA21S DONOR BLOB REFERENCES")
for script in sorted((root / "target/a21s/patches").glob("*/customize.sh")):
    for line in script.read_text(errors="replace").splitlines():
        match = re.search(r'ADD_TO_WORK_DIR\s+"\$SOURCE_FIRMWARE"\s+"([^"]+)"\s+"([^"$]+)"', line)
        if match:
            rel = "/".join(match.groups())
            print(f"{script.parent.name}: {rel}: S22={(old / rel).exists()} S23FE={(new / rel).exists()}")
print("\nCORE FRAMEWORK AND UI FILES")
for rel in ("system/system/framework/framework.jar", "system/system/framework/services.jar",
            "system/system/framework/ssrm.jar", "system/system/priv-app/SystemUI/SystemUI.apk",
            "system/system/priv-app/SecSettings/SecSettings.apk",
            "vendor/bin/hw/vendor.samsung.hardware.vibrator-service",
            "vendor/lib64/vendor.samsung.hardware.vibrator-V5-ndk_platform.so"):
    values = []
    for donor in (old, new):
        path = donor / rel
        values.append(str(path.stat().st_size) if path.is_file() else "missing")
    print(f"{rel}: {values[0]} -> {values[1]} bytes")
print("\nWindows free GiB:", round(shutil.disk_usage("/mnt/c").free / 2**30, 1))
