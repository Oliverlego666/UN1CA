#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
# Read-only baseline capture; no root, flashing, or device identifiers.
set -euo pipefail
command -v adb >/dev/null || { echo "adb is required" >&2; exit 1; }
adb get-state | grep -qx device || { echo "Connect and authorize one A21s" >&2; exit 1; }
out="${1:-a217f-baseline.txt}"
{
    echo "=== Selected properties ==="
    for prop in ro.product.vendor.device ro.product.vendor.model ro.boot.em.model ro.build.version.sdk ro.build.version.oneui ro.vendor.build.version.sdk ro.vendor.build.version.release ro.product.first_api_level ro.board.api_level ro.board.first_api_level ro.vndk.version ro.build.product ro.product.cpu.abilist ro.vendor.product.cpu.abilist ro.boot.dynamic_partitions ro.build.PDA ro.vendor.build.fingerprint; do
        printf '%s=' "$prop"
        adb shell getprop "$prop" | tr -d '\r'
    done
    echo "=== Kernel ==="
    adb shell uname -r
    echo "=== Filesystems ==="
    adb shell cat /proc/filesystems
    echo "=== Partition sizes (512-byte sectors) ==="
    adb shell 'for name in super boot dtbo recovery vendor_boot init_boot cache; do for base in /dev/block/by-name /dev/block/bootdevice/by-name; do if [ -e "$base/$name" ]; then node=$(basename "$(readlink -f "$base/$name")"); printf "%s " "$name"; cat "/sys/class/block/$node/size" 2>/dev/null || echo unavailable; break; fi; done; done'
    echo "=== Relevant mounts ==="
    adb shell 'grep -E " /(system|vendor|product|odm|system_ext|) " /proc/mounts || true'
    echo "=== Memory ==="
    adb shell 'grep "^MemTotal:" /proc/meminfo'
} > "$out"
printf 'Baseline saved to %s\n' "$out"
