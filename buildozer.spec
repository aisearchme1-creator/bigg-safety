[app]

title = BiggSafety
package.name = biggsafety
package.domain = org.bigg

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 11.0.0

requirements = python3,kivy==2.2.0,requests,cython==0.29.33  # Cython फिक्स, kivy 2.2 stable

orientation = portrait
fullscreen = 1

android.permissions = INTERNET,BLUETOOTH,WRITE_EXTERNAL_STORAGE,QUERY_ALL_PACKAGES

android.api = 33
android.minapi = 21
android.ndk_api = 21
android.ndk = 25b

p4a.bootstrap = sdl2

android.debug_artifact = apk

log_level = 2  # ज्यादा logs के लिए
