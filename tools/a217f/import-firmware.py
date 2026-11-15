#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Import the two pinned One UI 8.0 baseline Odin ZIPs without re-downloading."""
import argparse
import hashlib
from pathlib import Path
import re
import shutil
import tempfile
import zipfile

FIRMWARE = {
    "s22": ("SM-S901B_EUX", "S901BXXSOGZH3/S901BOXMOGZH3/S901BXXSOGZH3"),
    "a21s": ("SM-A217F_EGY", "A217FXXSCDXE2/A217FOJMCDXE3/A217FXXSCDXE1"),
}

def verify_odin(path):
    # Same appended md5sum format checked by scripts/download_fw.sh.
    trailer_size = 32 + 2 + len(path.name.removesuffix(".md5").encode()) + 1
    with path.open("rb") as f:
        remaining = path.stat().st_size - trailer_size
        if remaining <= 0:
            raise ValueError(f"Invalid Odin package: {path.name}")
        f.seek(remaining)
        trailer = f.read()
        expected = trailer[:32].decode("ascii")
        if not re.fullmatch(r"[0-9a-fA-F]{32}", expected):
            raise ValueError(f"No valid Odin MD5 trailer: {path.name}")
        f.seek(0)
        h = hashlib.md5()
        while remaining:
            chunk = f.read(min(8 * 1024 * 1024, remaining))
            if not chunk:
                raise ValueError(f"Truncated package: {path.name}")
            h.update(chunk)
            remaining -= len(chunk)
        if h.hexdigest() != expected.lower():
            raise ValueError(f"MD5 mismatch: {path.name}")

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("device", choices=FIRMWARE)
    parser.add_argument("zip", type=Path)
    args = parser.parse_args()
    folder, version = FIRMWARE[args.device]
    pda, csc, modem = version.split("/")
    dest = Path(__file__).resolve().parents[2] / "out" / "odin" / folder
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        raise SystemExit(f"Destination already exists; not overwriting: {dest}")
    with zipfile.ZipFile(args.zip) as archive:
        members = {}
        for entry in archive.infolist():
            name = Path(entry.filename).name
            if not entry.is_dir() and re.match(r"^(AP|BL|CP|CSC|HOME_CSC)_", name) and name.endswith(".tar.md5"):
                if name in members:
                    raise ValueError(f"Duplicate package: {name}")
                members[name] = entry
        for prefix, build in (("AP_", pda), ("BL_", pda), ("CP_", modem)):
            if sum(name.startswith(prefix + build) for name in members) != 1:
                raise ValueError(f"Expected exactly one {prefix}{build} package")
        if not any(name.startswith(("CSC_", "HOME_CSC_")) and csc in name for name in members):
            raise ValueError(f"Expected CSC build {csc}")
        with tempfile.TemporaryDirectory(prefix=".import-", dir=dest.parent) as temp:
            staging = Path(temp) / "odin"
            staging.mkdir()
            for name, entry in members.items():
                print(f"Extracting and verifying {name}", flush=True)
                with archive.open(entry) as src, (staging / name).open("wb") as dst:
                    shutil.copyfileobj(src, dst, length=8 * 1024 * 1024)
                verify_odin(staging / name)
            (staging / ".downloaded").write_text(version, encoding="ascii")
            if dest.exists():
                raise ValueError(f"Destination appeared during import: {dest}")
            staging.rename(dest)
    print(f"Imported {version} into {dest}")

if __name__ == "__main__":
    main()
