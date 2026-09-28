[app]
title = NAKI
package.name = naki
package.domain = com.naki.app

source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0
version.regex = __version__ = ['"]([^'"]+)['"]
version.filename = %(source.dir)s/main.py

requirements = python3,kivy,kivymd,requests,certifi,charset-normalizer,urllib3,idna

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
p4a.port =

[app:android]
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license_agreement = True
android.ant = auto
android.archs = arm64-v8a, armeabi-v7a

# (str) If you need source to compile go to specific directory
p4a.source_dir =

# (bool) If True, then skip trying to update the Android ant, android, sdk, etc. If False, then it is updated automatically
p4a.skip_update = False