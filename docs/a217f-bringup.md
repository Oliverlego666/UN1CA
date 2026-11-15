# SM-A217F bring-up: verified baseline

Status: existing A21s Android 16 source imported; local reproduction and One UI 8.5 integration pending.

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

- Recovery partition size (only if packaging requires it); boot, dtbo and cache measured
- System/vendor/product/odm mounts verified as EROFS
- Reproduce imported A21s port and pin its kernel and donor inputs
- Verify genuine One UI 8.5 donor firmware, SDK and matching patch revisions

## References

- https://github.com/BasGame1/ExtremeROM_A21s/tree/fifteen/target/a217f (older Android 15 reference only; config schema differs)
- https://github.com/salvogiangri/UN1CA/releases/tag/3.2.0 (matching donor PDA)
- https://github.com/ProjectDozG/UN1CA-8.5 (candidate, unverified donor/patch compatibility)

Do not copy old super/group sizes blindly: the historical configuration assigns equal sizes, whereas the current generator requires space for metadata. Do not flash donor bootloader/modem/boot images onto the A21s. Preserve the working baseline and verify recovery/backup paths before testing.

## Verified live logical partition metadata

Read using `adb shell su -c lpdump` on the working ROM.

- Super device: 9126805504 bytes; first sector 2048.
- Group: group_basic; maximum 5553258496 bytes.
- Metadata v10.0, 2 slots, maximum 65536 bytes.
- Extent sizes in 512-byte sectors: system 8026144, vendor 1119504, product 1627272, odm 1040.
- Existing images occupy 5516267520 bytes. The unused physical capacity is not automatically available within the current group limit.
- Use the observed group limit for baseline testing; do not enlarge it without verifying stock geometry and recovery compatibility.

## Imported baseline

- Source: https://github.com/mustvfa/UN1CA/tree/a21s at a560c6c0e257689489fa0ae50d4ade9b089f30cd.
- Kernel: https://github.com/mustvfa/android_kernel_samsung_exynos850 (upstream build script fetches latest release; not reproducibly pinned).
- Imported with original history in merge f8ac19c2487f1dae500a01af772a016e66ce44df.
- Actual upstream target identifier is a21s, not a217f.
- Upstream config deliberately builds a 5557452800-byte super image, smaller than the observed physical device; group size matches the live metadata. Preserve the upstream image geometry until packaging behavior is tested.
- Boot 37748736 bytes; dtbo 8388608; cache 6291456. No dedicated vendor_boot or init_boot in the observed layout.
- The source post identifies an OrangeFox recovery and a clean-flash install. No repartitioner required per its author.
- Baseline source has not been built or tested in this fork; do not treat merge as a flashable release.
