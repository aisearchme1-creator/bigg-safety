[app]
title = Bigg Safety
package.name = biggsafety
package.domain = com.biggsafety
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,ttf
version = 11.0.0
requirements = python3,kivy==2.3.0,requests,urllib3,certifi,charset-normalizer,idna
orientation = portrait
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,BLUETOOTH,BLUETOOTH_CONNECT,BLUETOOTH_SCAN,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_PHONE_STATE,QUERY_ALL_PACKAGES,POST_NOTIFICATIONS
android.minapi = 26
android.ndk = 25b
android.api = 33
android.sdk = 33
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.manifest.package = com.biggsafety.app
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1
