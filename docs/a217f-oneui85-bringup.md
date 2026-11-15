# Experimental A21s One UI 8.5 bring-up

Donor: SM-S711B EUX S711BXXSJGZI6, Android 16 SDK 36, One UI 80500.
Baseline: SM-S901B EUX S901BXXSOGZH3, Android 16 SDK 36, One UI 80000.
Both use ESSI and group_basic. The new donor's product first API is 33, board first API 31.
A21s target vendor, boot, DTBO and partition geometry remain unchanged.
Keep the extracted S22 firmware: the A21s audio, Bluetooth, SNAP and vendor compatibility
blob sets remain sourced from it deliberately. Nine SNAP files are absent from the 8.5 donor.
No repartitioning or flashing is authorized by this change.

The A21s donor override is experimental. Inherited S22 configuration values and the
optical fingerprint framework string require verification against the S23 FE DEX files.
Existing framework/smali and binary patches may fail and need rebasing; equal SDK does not
guarantee compatibility. Do not weaken patch error handling or skip a failed patch merely to compile.

First test: source buildenv.sh a21s, then unica make_rom -x.
This creates the patched workspace without building target-files or a flashable zip.
Only proceed to packaging after patch failures have been resolved and metadata reviewed.
The baseline build completed but has not been flashed or boot-tested.
