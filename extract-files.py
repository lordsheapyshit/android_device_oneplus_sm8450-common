#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    "device/oneplus/sm8450-common",
    "hardware/qcom-caf/sm8450",
    "hardware/qcom-caf/sm8450/audio/agm/ipc/HwBinders/legacy",
    "hardware/qcom-caf/wlan",
    "hardware/oplus",
    "vendor/qcom/opensource/commonsys/display",
    "vendor/qcom/opensource/commonsys-intf/display",
    "vendor/qcom/opensource/dataservices",
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f"{lib}_vendor" if partition in ["odm", "vendor"] else None


lib_fixups.update({
    (
        "com.qualcomm.qti.dpm.api@1.0",
        "libQnnHtp",
        "libQnnHtpPrepare",
        "libQnnHtpV69Stub",
        "vendor.oplus.hardware.performance-V1-ndk",
        "vendor.qti.diaghal@1.0",
        "vendor.qti.hardware.dpmservice@1.0",
        "vendor.qti.hardware.dpmservice@1.1",
        "vendor.qti.hardware.qccsyshal@1.0",
        "vendor.qti.hardware.qccsyshal@1.1",
        "vendor.qti.hardware.qccvndhal@1.0",
        "vendor.qti.hardware.wifidisplaysession@1.0",
        "vendor.qti.imsrtpservice@3.0",
    ): lib_fixup_vendor_suffix,
    (
        "libagmclient",
        "libpalclient",
        "libwpa_client",
    ): lib_fixup_remove,
})  # fmt: skip

blob_fixups: blob_fixups_user_type = {
    'odm/bin/hw/vendor.oplus.hardware.cammidasservice-V1-service': blob_fixup()
        .replace_needed('android.frameworks.stats-V1-ndk_platform.so', 'android.frameworks.stats-V2-ndk.so'),
    (
        "odm/lib64/libaps_frame_registration.so",
        "odm/lib64/libCOppLceTonemapAPI.so",
        "odm/lib64/libCS.so",
        "odm/lib64/libSuperRaw.so",
        "odm/lib64/libYTCommon.so",
        "odm/lib64/libyuv2.so",
    ): blob_fixup()
        .replace_needed('libstdc++.so', 'libstdc++_vendor.so'),
    'odm/lib64/libAlgoProcess.so': blob_fixup()
        .replace_needed('android.hardware.graphics.common-V2-ndk_platform.so', 'android.hardware.graphics.common-V5-ndk.so'),
    'odm/lib64/libextensionlayer.so': blob_fixup()
        .replace_needed('libziparchive.so', 'libziparchive_odm.so'),
    'vendor/bin/hw/vendor.qti.hardware.display.composer-service': blob_fixup()
        .replace_needed('vendor.qti.hardware.display.config-V5-ndk_platform.so', 'vendor.qti.hardware.display.config-V5-ndk.so'),
    'vendor/bin/qcc-trd': blob_fixup()
        .replace_needed('libgrpc++_unsecure.so', 'libgrpc++_unsecure_prebuilt.so'),
    'vendor/lib64/libcamximageformatutils.so': blob_fixup()
        .replace_needed('vendor.qti.hardware.display.config-V2-ndk_platform.so', 'vendor.qti.hardware.display.config-V2-ndk.so'),
    'vendor/lib64/libgrpc++_unsecure_prebuilt.so': blob_fixup()
        .fix_soname(),
    'vendor/lib64/vendor.libdpmframework.so': blob_fixup()
        .add_needed('libhidlbase_shim.so'),
    (
        'vendor/bin/hw/android.hardware.security.keymint-service-qti',
        'vendor/lib64/libqtikeymint.so'
    ): blob_fixup()
        .replace_needed('android.hardware.security.keymint-V1-ndk_platform.so', 'android.hardware.security.keymint-V1-ndk.so')
        .replace_needed('android.hardware.security.secureclock-V1-ndk_platform.so', 'android.hardware.security.secureclock-V1-ndk.so')
        .replace_needed('android.hardware.security.sharedsecret-V1-ndk_platform.so', 'android.hardware.security.sharedsecret-V1-ndk.so')
        .add_needed('android.hardware.security.rkp-V1-ndk.so'),
    'system_ext/lib64/libwfdmmsrc_system.so': blob_fixup()
        .add_needed('libgui_shim.so'),
    'system_ext/lib64/libwfdnative.so': blob_fixup()
        .replace_needed('android.hidl.base@1.0.so', 'libhidlbase.so')
        .add_needed('libinput_shim.so'),
    'system_ext/lib64/libwfdservice.so': blob_fixup()
        .replace_needed('android.media.audio.common.types-V2-cpp.so', 'android.media.audio.common.types-V3-cpp.so'),
    
    # regex
    'odm/etc/camera/CameraHWConfiguration.config': blob_fixup()
        .regex_replace('SystemCamera =  0;  0;  1;  1;  1;  1', 'SystemCamera =  0;  0;  0;  0;  0;  1'),
    'product/etc/sysconfig/com.android.hotwordenrollment.common.util.xml': blob_fixup()
        .regex_replace('/my_product', '/product'),
    (
        'vendor/etc/media_cape/video_system_specs.json',
        'vendor/etc/media_ukee/video_system_specs.json',
        'vendor/etc/media_taro/video_system_specs.json'
    ): blob_fixup()
        .regex_replace('"max_retry_alloc_output_timeout": 2000,', '"max_retry_alloc_output_timeout": 0,'),
    'vendor/etc/msm_irqbalance.conf': blob_fixup()
        .regex_replace('IGNORED_IRQ=27,23,38$', 'IGNORED_IRQ=27,23,38,115,332'),
    'vendor/lib64/sensors.ssc.so': blob_fixup()
        .binary_regex_replace(b'qti.sensor.wise_light', b'android.sensor.light\x00')
        .sig_replace('F1 E9 D3 84 52 49 3F A0 72', 'F1 A9 00 80 52 09 00 A0 72'),
    'vendor/etc/libnfc-nci.conf': blob_fixup()
        .regex_replace("NFC_DEBUG_ENABLED=1","NFC_DEBUG_ENABLED=0"),
    'vendor/etc/libnfc-nxp.conf': blob_fixup()
        .regex_replace('(NXPLOG_.*_LOGLEVEL)=0x03', '\\1=0x02')
        .regex_replace("NFC_DEBUG_ENABLED=1","NFC_DEBUG_ENABLED=0"),
    (
        'vendor/etc/media_codecs_cape.xml',
        'vendor/etc/media_codecs_cape_vendor.xml',
        'vendor/etc/media_codecs_taro.xml',
        'vendor/etc/media_codecs_taro_vendor.xml'
    ): blob_fixup()
        .regex_replace('.*media_codecs_(google_audio|google_c2|google_telephony|google_video|vendor_audio).*\n', ''),
    'vendor/etc/seccomp_policy/qwesd@2.0.policy': blob_fixup()
        .add_line_if_missing('gettid: 1')
        .add_line_if_missing('pipe2: 1'),
}  # fmt: skip

module = ExtractUtilsModule(
    "sm8450-common",
    "oneplus",
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    check_elf=True,
)
if __name__ == "__main__":
    utils = ExtractUtils.device(module)
    utils.run()
