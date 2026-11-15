SET_PROP_IF_DIFF "vendor" "ro.oem_unlock_supported" "0"

# Better device/model detection in CoreRune
SMALI_PATCH "system" "system/framework/framework.jar" \
    "smali_classes6/com/samsung/android/rune/CoreRune.smali" "replace" \
    '<clinit>()V' \
    'ro.product.model' \
    'ro.product.vendor.model'
SMALI_PATCH "system" "system/framework/framework.jar" \
    "smali_classes6/com/samsung/android/rune/CoreRune.smali" "replace" \
    '<clinit>()V' \
    'ro.product.device' \
    'ro.product.vendor.device'

# shellcheck disable=SC2016
# Disable RescueParty
SMALI_PATCH "system" "system/framework/services.jar" \
    "smali/com/android/server/RescueParty.smali" "return" \
    '-$$Nest$smisDisabled()Z' \
    'true'

# Better model detection in FreecessController
SMALI_PATCH "system" "system/framework/services.jar" \
    "smali/com/android/server/am/FreecessController.smali" "replace" \
    '<clinit>()V' \
    'ro.product.model' \
    'ro.product.vendor.model'

# Preserve the mismatch warning on the experimental A21s 8.5 port.
# It is useful during bring-up and the legacy dialog patch is not compatible.
if [[ "$TARGET_CODENAME" == "a21s" && "$SOURCE_FIRMWARE" == SM-S711B/* ]]; then
    LOG "- Retaining vendor mismatch warning for One UI 8.5 bring-up"
else
    APPLY_PATCH "system" "system/framework/services.jar" \
        "$MODPATH/vendor_mismatch/services.jar/0001-Disable-vendor-mismatch-warning.patch"
fi
