LOG "- Applying left camera cutout patch"
if [[ "$SOURCE_FIRMWARE" == SM-S711B/* ]]; then
    APPLY_PATCH "system_ext" "priv-app/SystemUI/SystemUI.apk" \
        "$MODPATH/cutout/SystemUI.apk/0001-Add-left-cutout-support-8.5.patch"
else
    APPLY_PATCH "system_ext" "priv-app/SystemUI/SystemUI.apk" \
        "$MODPATH/cutout/SystemUI.apk/0001-Add-left-cutout-support.patch"
fi
