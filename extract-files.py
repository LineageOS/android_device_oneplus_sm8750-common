#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024-2025 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/oneplus/sm8750-common',
    'hardware/qcom-caf/sm8750',
    'hardware/qcom-caf/wlan',
    'hardware/oplus',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'vendor.qti.ImsRtpService-V1-ndk',
        'vendor.qti.diaghal-V1-ndk',
        'vendor.qti.hardware.dpmaidlservice-V1-ndk',
        'vendor.qti.hardware.wifidisplaysession_aidl-V1-ndk',
        'vendor.qti.qccsyshal_aidl-V1-ndk',
        'vendor.qti.qccvndhal_aidl-V1-ndk',
    ): lib_fixup_vendor_suffix,
    (
        'libagm',
        'libagmclient',
        'libar-acdb',
        'libar-gsl',
        'libats',
        'libaudioserviceexampleimpl',
        'liblx-osal',
        'libvui_intf',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    'odm/bin/hw/vendor.oplus.hardware.biometrics.fingerprint@2.1-service_uff': blob_fixup()
        .add_needed('libshims_aidl_fingerprint_v3.oplus.so'),
    'odm/etc/init/init.network.rc': blob_fixup()
        .regex_replace(r'/\* (Huo\.Chen@SYSTEM\.RF, 2024/09/06, Add for ICC) \*/', r'# \1'),
    'product/etc/sysconfig/com.android.hotwordenrollment.common.util.xml': blob_fixup()
        .regex_replace('/my_product', '/product'),
    'vendor/bin/system_dlkm_modprobe.sh': blob_fixup()
        .regex_replace(r'.*\bzram or zsmalloc\b.*\n', '')
        .regex_replace(r'-e "zram" -e "zsmalloc"', ''),
    'vendor/bin/vendor_modprobe.sh': blob_fixup()
        .regex_replace(r'\n.*OPLUS_FEATURE_WIFI_FTM[\s\S]*?OPLUS_FEATURE_WIFI_FTM.*\n', ''),
    'vendor/etc/clstc_config_library.xml': blob_fixup()
        .regex_replace(r'\n.*OPLUS_FEATURE_DSIPLAY[\s\S]*?OPLUS_FEATURE_DSIPLAY.*\n', ''),
    'vendor/etc/media_codecs_sun.xml': blob_fixup()
        .regex_replace('.*media_codecs_(google_audio|google_c2|google_telephony|google_video|vendor_audio).*\n', ''),
    'vendor/etc/seccomp_policy/gnss@2.0-qsap-location.policy': blob_fixup()
        .add_line_if_missing('sched_get_priority_min: 1')
        .add_line_if_missing('sched_get_priority_max: 1'),
    'vendor/lib64/hw/libaudiocorehal.qti.so': blob_fixup()
        .replace_needed('android.hardware.audio.core.sounddose-V1-ndk.so', 'android.hardware.audio.core.sounddose-V2-ndk.so')
        .replace_needed('android.hardware.audio.common-V1-ndk.so', 'android.hardware.audio.common-V3-ndk.so')
        .replace_needed('libaudio_aidl_conversion_common_ndk.so', 'libaudio_aidl_conversion_common_ndk_prebuilt.so'),
    (
        'vendor/lib64/hw/android.hardware.bluetooth.audio_sw.so',
        'vendor/lib64/libaudioserviceexampleimpl.so',
    ): blob_fixup()
        .replace_needed('android.media.audio.common.types-V4-ndk.so', 'android.media.audio.common.types-V3-ndk.so')
        .replace_needed('android.hardware.bluetooth.audio-impl.so', 'android.hardware.bluetooth.audio-impl_prebuilt.so')
        .replace_needed('libbluetooth_audio_session_aidl.so', 'libbluetooth_audio_session_aidl_prebuilt.so')
        .replace_needed('libaudio_aidl_conversion_common_ndk.so', 'libaudio_aidl_conversion_common_ndk_prebuilt.so'),
    'vendor/lib64/android.hardware.bluetooth.audio-impl_prebuilt.so': blob_fixup()
        .replace_needed('libbluetooth_audio_session_aidl.so', 'libbluetooth_audio_session_aidl_prebuilt.so'),
    'vendor/lib64/libaudio_aidl_conversion_common_ndk_prebuilt.so': blob_fixup()
        .replace_needed('android.media.audio.common.types-V4-ndk.so', 'android.media.audio.common.types-V3-ndk.so'),
    (
        'vendor/lib64/soundfx/libbundleaidl.so',
        'vendor/lib64/soundfx/libdownmixaidl.so',
        'vendor/lib64/soundfx/libdynamicsprocessingaidl.so',
        'vendor/lib64/soundfx/libloudnessenhanceraidl.so',
        'vendor/lib64/soundfx/libreverbaidl.so',
        'vendor/lib64/soundfx/libvisualizeraidl.so',
    ): blob_fixup()
        .replace_needed('android.media.audio.common.types-V4-ndk.so', 'android.media.audio.common.types-V3-ndk.so')
        .replace_needed('libaudio_aidl_conversion_common_ndk.so', 'libaudio_aidl_conversion_common_ndk_prebuilt.so'),
    (
        'vendor/lib64/libapengine.so',
        'vendor/lib64/libqti-perfd.so',
    ): blob_fixup()
        .replace_needed('vendor.qti.hardware.display.config-V5-ndk.so', 'vendor.qti.hardware.display.config-V12-ndk.so'),
    (
        'vendor/lib64/libcwb_qcom_aidl.so',
        'vendor/lib64/libsdmclient.so',
    ): blob_fixup()
        .replace_needed('vendor.qti.hardware.display.config-V11-ndk.so', 'vendor.qti.hardware.display.config-V12-ndk.so'),
    (
        'vendor/lib64/libloc_api_v02.so',
        'vendor/lib64/libloc_core.so',
    ): blob_fixup()
        .add_needed('libbase.so'),
    'vendor/lib64/libwfdmmsrc_proprietary.so': blob_fixup()
        .replace_needed('android.media.audio.common.types-V2-ndk.so', 'android.media.audio.common.types-V3-ndk.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sm8750-common',
    'oneplus',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

module.add_proprietary_file('proprietary-files-phone.txt').add_copy_files_guard(
    'TARGET_IS_TABLET', 'true', invert=True
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
