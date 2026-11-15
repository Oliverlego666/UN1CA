#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
# Build a separate WSL host kernel; never touches Android firmware or WSL config.
set -euo pipefail
TAG=linux-msft-wsl-6.18.58.1
DIR="$HOME/wsl-kernel-un1ca-6.18.58.1"
JOBS="${JOBS:-8}"
if [[ ! -d "$DIR" ]]; then
    git clone --depth 1 --branch "$TAG" https://github.com/microsoft/WSL2-Linux-Kernel.git "$DIR"
fi
cd "$DIR"
[[ "$(git rev-parse HEAD)" == "$(git rev-parse "$TAG^{commit}")" ]] || { echo 'Unexpected kernel revision' >&2; exit 1; }
cp Microsoft/config-wsl .config
scripts/config --set-str LOCALVERSION '-microsoft-standard-WSL2-un1ca' \
    -e F2FS_FS -e F2FS_FS_XATTR -e F2FS_FS_POSIX_ACL -e F2FS_FS_SECURITY \
    -e F2FS_FS_COMPRESSION -e F2FS_FS_LZO -e F2FS_FS_LZORLE \
    -e F2FS_FS_LZ4 -e F2FS_FS_LZ4HC -e F2FS_FS_ZSTD \
    -e EROFS_FS -e EROFS_FS_XATTR -e EROFS_FS_SECURITY -e EROFS_FS_ZIP \
    -e EROFS_FS_ZIP_ZSTD
make olddefconfig
for opt in F2FS_FS F2FS_FS_SECURITY F2FS_FS_COMPRESSION F2FS_FS_LZ4 F2FS_FS_ZSTD EROFS_FS; do
    grep -qx "CONFIG_${opt}=y" .config || { echo "Missing CONFIG_${opt}" >&2; exit 1; }
done
make -j"$JOBS"
make INSTALL_MOD_PATH="$PWD/modules" modules_install
make headers_install INSTALL_HDR_PATH="$PWD/headers"
# perf is not needed for the ROM build; retain WSL's expected artifact directory.
mkdir -p "$PWD/perf"
if [[ ! -e modules.vhdx ]]; then
    bash Microsoft/scripts/gen_artifacts_vhdx.sh "$PWD/modules" "$PWD/headers" "$PWD/perf" "$(make -s kernelrelease)" modules.vhdx
fi
printf '\nKernel: %s/arch/x86/boot/bzImage\nModules: %s/modules.vhdx\n' "$PWD" "$PWD"
