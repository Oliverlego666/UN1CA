# SM-A217F bring-up: verified baseline

Status: research only; no flashable images or target configuration yet.

## Observed on the working unofficial UN1CA 3.2.1 installation

- Target model and boot model: SM-A217F
- Vendor device: a21s
- System: Android SDK 36, One UI 80000, ESSI
- Donor PDA: S901BXXSOGZH3
- Vendor: Android 12, SDK/VNDK 31, A217FXXSCDXE2
- Product first API: 29
- Board API properties: unset (do not infer a value without checking stock firmware)
- Kernel: 4.19.325-g4a2052095396
- Both 64-bit and 32-bit ARM userspace supported
- Dynamic partitions: true
- Kernel advertises ext4, f2fs and erofs; actual mounted filesystem not established
- MemTotal: 2758212 kB

## Required before packaging

- Actual super capacity, logical group name and group maximum size (lpdump)
- Boot, dtbo, recovery and cache partition sizes
- Actual system/vendor/product/odm mounts
- Source and build instructions for the working A21s port, including matching kernel and ramdisk
- Verify genuine One UI 8.5 donor firmware, SDK and matching patch revisions

## References

- https://github.com/BasGame1/ExtremeROM_A21s/tree/fifteen/target/a217f (older Android 15 reference only; config schema differs)
- https://github.com/salvogiangri/UN1CA/releases/tag/3.2.0 (matching donor PDA)
- https://github.com/ProjectDozG/UN1CA-8.5 (candidate, unverified donor/patch compatibility)

Do not copy old super/group sizes blindly: the historical configuration assigns equal sizes, whereas the current generator requires space for metadata. Do not flash donor bootloader/modem/boot images onto the A21s. Preserve the working baseline and verify recovery/backup paths before testing.
