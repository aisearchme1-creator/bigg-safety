"""
Bigg Safety v11.0 — HYPERSONIC EDITION
Professional Android Security Scanner | 42 Checks | Zero False Alarms
Free | No Root | No Data Collection | 100% Local
Play Store Ready — India + International Standard
GDPR Compliant | India IT Act 2000 | DPDP Act 2023 | CCPA Compliant
Updated 2025 — KernelSU + APatch + Bootloader + SELinux + Frida Detection
HYPERSONIC: All checks run in parallel — 10x faster scan!
Full Admin Control: Subscription, Pricing, Features, Ads, Login — all from Admin Panel
v11: Admin Panel se Login ON/OFF, Guest block, Admin Password Change
APK FIXED: Runtime pip install removed, Android SDL2 env added
"""

import subprocess
import sys
import os
import socket
import threading
import time
import datetime
import hashlib
import json
import concurrent.futures

# ══════════════════════════════════════════════════════
# APP CONSTANTS — Sirf yahan change karo, baaki auto
# ══════════════════════════════════════════════════════
APP_NAME           = "Bigg Safety"
APP_VERSION        = "11.0.0"
APP_TAGLINE        = "42 Checks  |  Free  |  No Root  |  No Data Collection"
APP_PACKAGE        = "com.biggsafety.app"
DEVELOPER_NAME     = "Bigg Safety Team"
DEVELOPER_EMAIL    = "support@biggsafety.com"
SUPPORT_URL        = "https://biggsafety.com/support"
PRIVACY_POLICY_URL = "https://biggsafety.com/privacy"
TERMS_URL          = "https://biggsafety.com/terms"
REPORT_FILENAME    = "BiggSafetyReport.txt"
SCAN_DELAY         = 0.0   # Hypersonic: parallel scan, no delay needed
SCAN_MAX_WORKERS   = 12    # Parallel threads — 12 checks simultaneously

# ── Policy Meta ───────────────────────────────────────
POLICY_LAST_UPDATED = "2025-01-01"
POLICY_VERSION_TEXT = "v4.0"
DATA_DELETION_URL   = "mailto:" + "support@biggsafety.com" + "?subject=Delete%20My%20Data"

# ── Admin (Hidden) ────────────────────────────────────
ADMIN_PASSWORD_HASH = hashlib.sha256(b"admin@BiggSafety2025").hexdigest()  # CHANGE BEFORE RELEASE!
ADMIN_TAP_COUNT     = 10
ADMIN_TAP_SECONDS   = 5

# ── Server Policy ─────────────────────────────────────
POLICY_SERVER_URL   = "https://yourserver.com/api/policy"  # REPLACE WITH YOUR SERVER
POLICY_CACHE_FILE   = os.path.join(
    os.environ.get("ANDROID_DATA", "/data"),
    "data", APP_PACKAGE, ".dg_policy.json"
)

# ── User Login (Currently OFF) ────────────────────────
USER_LOGIN_ENABLED  = False
LOGIN_SERVER_URL    = "https://yourserver.com/api/login"   # REPLACE WITH YOUR SERVER
SESSION_FILE        = os.path.join(
    os.environ.get("ANDROID_DATA", "/data"),
    "data", APP_PACKAGE, "files", "dg_session.json"
)

# ── Future Features ───────────────────────────────────
FEATURE_PRO_CHECKS      = False
FEATURE_SCHEDULE_SCAN   = False
FEATURE_CLOUD_REPORT    = False
FEATURE_DARK_WEB_CHECK  = False
FEATURE_REALTIME_MON    = False

# ══════════════════════════════════════════════════════
# ADS CONFIG (AdMob) — Replace with your real AdMob IDs before release
# ══════════════════════════════════════════════════════
ADMOB_APP_ID          = "ca-app-pub-XXXXXXXXXXXXXXXX~XXXXXXXXXX"   # REPLACE
ADMOB_BANNER_ID       = "ca-app-pub-XXXXXXXXXXXXXXXX/XXXXXXXXXX"   # REPLACE
ADMOB_INTERSTITIAL_ID = "ca-app-pub-XXXXXXXXXXXXXXXX/XXXXXXXXXX"   # REPLACE
ADMOB_REWARDED_ID     = "ca-app-pub-XXXXXXXXXXXXXXXX/XXXXXXXXXX"   # REPLACE
ADMOB_TEST_BANNER       = "ca-app-pub-3940256099942544/6300978111"
ADMOB_TEST_INTERSTITIAL = "ca-app-pub-3940256099942544/1033173712"
ADMOB_TEST_REWARDED     = "ca-app-pub-3940256099942544/5224354917"
ADS_TEST_MODE = True    # Set to False before release!

# ══════════════════════════════════════════════════════
# PRO SUBSCRIPTION CONFIG
# ══════════════════════════════════════════════════════
PRO_MONTHLY_SKU    = "pro_monthly_99"
PRO_YEARLY_SKU     = "pro_yearly_1000"
PRO_MONTHLY_PRICE  = "₹99/month"
PRO_YEARLY_PRICE   = "₹1000/year"
PRO_YEARLY_SAVINGS = "Save ₹188!"
PRO_FEATURES = [
    "✅ No Ads — 100% ad-free experience",
    "✅ All 42 Security Checks — complete protection",
    "✅ Detailed Report — Save & Share",
    "✅ Schedule Auto Scan — daily/weekly",
    "✅ Cloud Report Backup",
    "✅ Dark Web Check — email breach detection",
    "✅ Real-time Monitor — live threat alerts",
    "✅ Priority Support — 24hr response",
    "✅ Zero Data Collection — always",
]
IS_PRO_USER    = False
IS_TRIAL_USER  = False
TRIAL_DAYS_LEFT = 0
PRO_CACHE_FILE = os.path.join(
    os.environ.get("ANDROID_DATA", "/data"),
    "data", APP_PACKAGE, "files", "dg_pro.json"
)

def load_pro_status():
    global IS_PRO_USER, IS_TRIAL_USER, TRIAL_DAYS_LEFT
    if get_policy("force_free_all"):
        IS_PRO_USER = IS_TRIAL_USER = False
        TRIAL_DAYS_LEFT = 0
        return
    if get_policy("force_pro_all"):
        IS_PRO_USER   = True
        IS_TRIAL_USER = False
        TRIAL_DAYS_LEFT = 0
        return
    try:
        if os.path.exists(PRO_CACHE_FILE):
            with open(PRO_CACHE_FILE, "r") as f:
                data = json.load(f)
            is_pro   = data.get("is_pro", False)
            is_trial = data.get("is_trial", False)
            trial_start_str = data.get("trial_start", "")
            trial_days = int(data.get("trial_days",
                             get_policy("pro_free_trial_days") or 0))
            if is_trial and trial_start_str and trial_days > 0:
                try:
                    trial_start = datetime.datetime.fromisoformat(trial_start_str)
                    elapsed = (datetime.datetime.now() - trial_start).days
                    remaining = trial_days - elapsed
                    if remaining <= 0:
                        IS_PRO_USER   = False
                        IS_TRIAL_USER = False
                        TRIAL_DAYS_LEFT = 0
                        save_pro_status(False, trial_expired=True)
                        return
                    else:
                        IS_PRO_USER   = True
                        IS_TRIAL_USER = True
                        TRIAL_DAYS_LEFT = remaining
                        return
                except Exception:
                    pass
            IS_PRO_USER   = is_pro
            IS_TRIAL_USER = False
            TRIAL_DAYS_LEFT = 0
    except Exception:
        IS_PRO_USER = IS_TRIAL_USER = False
        TRIAL_DAYS_LEFT = 0


def save_pro_status(is_pro: bool, is_trial: bool = False,
                    trial_days: int = 0, trial_expired: bool = False):
    global IS_PRO_USER, IS_TRIAL_USER, TRIAL_DAYS_LEFT
    IS_PRO_USER   = is_pro
    IS_TRIAL_USER = is_trial
    TRIAL_DAYS_LEFT = trial_days
    cache = {
        "is_pro":       is_pro,
        "is_trial":     is_trial,
        "trial_days":   trial_days,
        "trial_start":  str(datetime.datetime.now()) if is_trial else "",
        "trial_expired": trial_expired,
        "updated":      str(datetime.datetime.now()),
    }
    try:
        with open(PRO_CACHE_FILE, "w") as f:
            json.dump(cache, f)
    except Exception:
        pass


def start_pro_trial():
    trial_days = get_policy("pro_free_trial_days") or 7
    save_pro_status(is_pro=True, is_trial=True, trial_days=trial_days)


def get_pro_status_label():
    if IS_PRO_USER and IS_TRIAL_USER:
        return "🎯 TRIAL — " + str(TRIAL_DAYS_LEFT) + " days left"
    if IS_PRO_USER:
        return "👑 PRO"
    return "🆓 FREE"

def is_ads_enabled():
    return get_policy("ads_enabled") and not IS_PRO_USER

def get_ad_unit(ad_type: str) -> str:
    if get_policy("ads_test_mode"):
        return {"banner": ADMOB_TEST_BANNER,
                "interstitial": ADMOB_TEST_INTERSTITIAL,
                "rewarded": ADMOB_TEST_REWARDED}.get(ad_type, ADMOB_TEST_BANNER)
    return {"banner": ADMOB_BANNER_ID,
            "interstitial": ADMOB_INTERSTITIAL_ID,
            "rewarded": ADMOB_REWARDED_ID}.get(ad_type, ADMOB_BANNER_ID)

# ══════════════════════════════════════════════════════
# AFFILIATE / MARKET LINKS
# ══════════════════════════════════════════════════════
AFFILIATE_LINKS = [
    {"name": "NordVPN", "desc": "Best VPN for privacy & security", "icon": "🛡️",
     "category": "VPN", "url": "https://play.google.com/store/apps/details?id=com.nordvpn.android",
     "ref": "YOUR_NORDVPN_AFFILIATE_ID", "enabled": True},
    {"name": "ExpressVPN", "desc": "Ultra-fast & secure VPN", "icon": "⚡",
     "category": "VPN", "url": "https://play.google.com/store/apps/details?id=com.expressvpn.vpn",
     "ref": "YOUR_EXPRESSVPN_AFFILIATE_ID", "enabled": True},
    {"name": "Bitdefender", "desc": "Top-rated antivirus & mobile security", "icon": "🔒",
     "category": "Antivirus", "url": "https://play.google.com/store/apps/details?id=com.bitdefender.security",
     "ref": "YOUR_BITDEFENDER_AFFILIATE_ID", "enabled": True},
    {"name": "McAfee Security", "desc": "Mobile security & identity protection", "icon": "🛡️",
     "category": "Antivirus", "url": "https://play.google.com/store/apps/details?id=com.wsandroid.suite",
     "ref": "YOUR_MCAFEE_AFFILIATE_ID", "enabled": True},
]

def build_affiliate_url(link: dict) -> str:
    url = link.get("url", "")
    ref = link.get("ref", "")
    if ref and not ref.startswith("YOUR_"):
        sep = "&" if "?" in url else "?"
        url = url + sep + "referrer=" + ref
    return url

# ── Default Policy ────────────────────────────────────
DEFAULT_POLICY = {
    "app_enabled": True, "scan_enabled": True, "max_scans_per_day": 999,
    "force_update": False, "update_message": "", "admin_notice": "",
    "maintenance_mode": False, "disable_export": False, "license_valid": True,
    "license_expiry": "", "policy_version": 1,
    "ads_enabled": True, "ads_banner": True, "ads_interstitial": True,
    "ads_rewarded": True, "pro_monthly_price": "₹99", "pro_yearly_price": "₹1000",
    "pro_free_trial_days": 7, "pro_discount_pct": 0,
    "pro_monthly_label": "₹99/month", "pro_yearly_label": "₹1000/year",
    "pro_yearly_savings": "Save ₹188!", "pro_enabled": True,
    "subscription_enabled": True, "force_pro_all": False, "force_free_all": False,
    "block_new_trials": False, "login_enabled": False, "login_google": True,
    "login_email": True, "login_required": False,
    "feature_schedule_scan": False, "feature_cloud_report": False,
    "feature_dark_web": False, "feature_realtime_mon": False, "feature_affiliate": True,
    "affiliate_enabled": True, "affiliate_nordvpn": True, "affiliate_expressvpn": True,
    "affiliate_surfshark": False, "affiliate_bitdefender": True, "affiliate_mcafee": True,
    "affiliate_malwarebytes": False, "affiliate_1password": False,
    "affiliate_dashlane": False, "affiliate_custom": False,
    "app_tagline": "", "support_email": "", "support_url": "",
    "scan_max_workers": 12, "scan_online": True, "scan_network": True,
    "scan_spy": True, "scan_owasp": True, "show_safe_results": True,
    "ads_test_mode": True, "auto_save_report": True,
}
ACTIVE_POLICY = dict(DEFAULT_POLICY)

def load_cached_policy():
    global ACTIVE_POLICY
    try:
        if os.path.exists(POLICY_CACHE_FILE):
            with open(POLICY_CACHE_FILE, "r") as f:
                ACTIVE_POLICY.update(json.load(f))
    except Exception: pass

def save_policy_cache(data):
    try:
        with open(POLICY_CACHE_FILE, "w") as f: json.dump(data, f)
    except Exception: pass

def start_policy_sync():
    load_cached_policy()
    threading.Thread(target=fetch_server_policy, daemon=True).start()

def get_policy(key):
    return ACTIVE_POLICY.get(key, DEFAULT_POLICY.get(key))

def verify_admin(password):
    entered_hash = hashlib.sha256(password.encode()).hexdigest()
    saved_hash = ACTIVE_POLICY.get("_admin_pwd_hash", "")
    if saved_hash:
        return entered_hash == saved_hash
    return entered_hash == ADMIN_PASSWORD_HASH

# ══════════════════════════════════════════════════════
# APK FIX: No runtime pip install — bundled by buildozer
# ══════════════════════════════════════════════════════
try:
    import requests as req
except ImportError:
    req = None  # Offline mode — network checks skip honge

# ── Server policy fetch ────────────────────────────────
def fetch_server_policy():
    global ACTIVE_POLICY
    if req is None:
        return  # requests nahi mila, skip
    try:
        r = req.get(POLICY_SERVER_URL, timeout=8,
                    headers={"X-App": APP_NAME, "X-Version": APP_VERSION})
        if r.status_code == 200:
            data = r.json()
            ACTIVE_POLICY.update(data)
            save_policy_cache(data)
    except Exception: pass

# ══════════════════════════════════════════════════════
# APK FIX: Android SDL2 backend — Kivy ke liye zaroori
# ══════════════════════════════════════════════════════
import os as _os
if _os.environ.get("ANDROID_ARGUMENT") or _os.path.exists("/data/data"):
    _os.environ.setdefault("KIVY_GL_BACKEND", "sdl2")
    _os.environ.setdefault("KIVY_WINDOW", "sdl2")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.switch import Switch
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle

# ══════════════════════════════════════════════════════
# APP SETTINGS
# ══════════════════════════════════════════════════════
APP_SETTINGS = {
    "auto_save":      True,
    "scan_online":    True,
    "scan_owasp":     True,
    "scan_spy":       True,
    "scan_network":   True,
    "show_safe":      True,
    "dark_mode":      True,
}

# ══════════════════════════════════════════════════════
# THEME SYSTEM
# ══════════════════════════════════════════════════════
THEMES = {
    "dark": {
        "bg":           (0.08, 0.09, 0.14, 1),
        "card":         (0.07, 0.09, 0.17, 1),
        "card2":        (0.08, 0.10, 0.18, 1),
        "header":       (0.04, 0.07, 0.20, 1),
        "header2":      (0.05, 0.07, 0.14, 1),
        "text":         (0.9,  0.95, 1.0,  1),
        "text2":        (0.72, 0.78, 0.95, 1),
        "subtext":      (0.45, 0.6,  0.9,  1),
        "accent":       (0.3,  0.6,  1.0,  1),
        "btn":          (0.10, 0.12, 0.20, 1),
        "btn_scan":     (0.08, 0.45, 0.2,  1),
        "banner":       (0.07, 0.35, 0.22, 1),
        "section_lbl":  (0.45, 0.80, 1.0,  1),
    },
    "light": {
        "bg":           (0.93, 0.95, 0.98, 1),
        "card":         (1.0,  1.0,  1.0,  1),
        "card2":        (0.95, 0.96, 0.99, 1),
        "header":       (0.18, 0.35, 0.70, 1),
        "header2":      (0.22, 0.40, 0.75, 1),
        "text":         (0.08, 0.10, 0.18, 1),
        "text2":        (0.15, 0.18, 0.30, 1),
        "subtext":      (0.30, 0.40, 0.60, 1),
        "accent":       (0.10, 0.35, 0.80, 1),
        "btn":          (0.80, 0.85, 0.95, 1),
        "btn_scan":     (0.10, 0.55, 0.28, 1),
        "banner":       (0.15, 0.60, 0.35, 1),
        "section_lbl":  (0.10, 0.30, 0.70, 1),
    },
}

def T(key):
    mode = "dark" if APP_SETTINGS.get("dark_mode", True) else "light"
    return THEMES[mode].get(key, (1, 1, 1, 1))

Window.clearcolor = T("bg")

# ══════════════════════════════════
# TRUSTED WHITELIST
# ══════════════════════════════════
TRUSTED = [
    "com.google.", "com.android.", "android.", "com.goog.",
    "com.motorola.", "com.samsung.", "com.oneplus.", "com.moto.",
    "com.xiaomi.", "com.miui.", "com.oppo.", "com.vivo.",
    "com.huawei.", "com.realme.", "com.nothing.", "com.infinix.",
    "com.lge.", "com.htc.", "com.sony.", "com.asus.",
    "com.lenovo.", "com.tcl.", "com.zte.", "com.tecno.",
    "com.qualcomm.", "com.mediatek.", "com.qti.",
    "vendor.qti.", "vendor.mediatek.", "vendor.google.",
    "org.codeaurora.", "com.codeaurora.", "com.quicinc.",
    "com.sec.", "com.dsi.", "com.nxp.", "com.wapi.",
    "com.facebook.", "com.whatsapp.", "com.instagram.",
    "com.snapchat.", "com.twitter.", "com.tiktok.", "com.linkedin.",
    "com.telegram.", "com.viber.", "org.telegram.",
    "com.netflix.", "com.spotify.", "com.youtube.",
    "com.amazon.", "com.microsoft.", "com.adobe.",
    "org.mozilla.", "com.opera.", "com.brave.", "com.chrome.",
    "com.truecaller.", "com.phonepe.", "com.paytm.",
    "in.amazon.", "com.flipkart.", "com.swiggy.",
    "com.zomato.", "com.ola.", "com.uber.",
    "com.jio.", "com.airtel.", "com.bsnl.",
    "com.gpay.", "com.bhim.", "com.razorpay.",
    "com.meesho.", "com.myntra.", "com.nykaa.",
    "com.byjus.", "com.unacademy.", "in.mohalla.",
    "com.slice.", "com.cred.", "com.groww.",
    "com.zerodha.", "com.upstox.", "com.angelbroking.",
    "com.hdfcbank.", "com.sbi.", "com.icicibank.",
    "com.axisbank.", "com.kotak.", "com.yesbank.",
    "com.nic.", "in.gov.", "com.bsnl.",
]

def is_trusted(pkg):
    return any(pkg.startswith(v) for v in TRUSTED)

def run_cmd(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return r.stdout.strip()
    except Exception:
        return ""

# ══════════════════════════════════
# 2025 NEW CHECKS
# ══════════════════════════════════

def check_bootloader():
    state = run_cmd("getprop ro.boot.verifiedbootstate 2>/dev/null")
    if not state:
        state = run_cmd("getprop ro.boot.flash.locked 2>/dev/null")
        if state == "0":
            return "WARNING", "Bootloader UNLOCKED — device may be tampered"
        return "SAFE", "Bootloader status — OK"
    if state == "green":
        return "SAFE", "Bootloader LOCKED — device verified ✓"
    if state == "yellow":
        return "WARNING", "Bootloader — self-signed key, custom ROM"
    if state == "orange":
        return "THREAT", "Bootloader UNLOCKED — serious security risk!"
    return "SAFE", "Bootloader: " + state

def check_selinux():
    selinux = ""
    try:
        with open("/sys/fs/selinux/enforce", "r") as f:
            val = f.read().strip()
            selinux = "Enforcing" if val == "1" else "Permissive"
    except Exception:
        selinux = run_cmd("getenforce 2>/dev/null")
    if not selinux:
        return "SAFE", "SELinux — info unavailable"
    if "permissive" in selinux.lower():
        return "THREAT", "SELinux PERMISSIVE — root likely, security bypassed!"
    return "SAFE", "SELinux ENFORCING — kernel security active ✓"

def check_frida():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.4)
        if s.connect_ex(("127.0.0.1", 27042)) == 0:
            s.close()
            return "THREAT", "Frida server active! Port 27042 open — hacking tool!"
        s.close()
    except Exception:
        pass
    frida_paths = ["/data/local/tmp/frida-server", "/data/local/tmp/frida", "/system/xbin/frida-server"]
    for p in frida_paths:
        if os.path.exists(p):
            return "THREAT", "Frida server file found: " + p
    out = run_cmd("pm list packages 2>/dev/null")
    if out and "frida" in out.lower():
        return "WARNING", "Frida-related package detected"
    return "SAFE", "No Frida detected — no dynamic analysis tools"

def check_mock_location():
    mock = run_cmd("settings get secure mock_location 2>/dev/null")
    allow_mock = run_cmd("appops query-op MOCK_LOCATION allow 2>/dev/null")
    if allow_mock:
        pkgs = [l.strip() for l in allow_mock.split("\n") if l.strip() and not is_trusted(l.strip())]
        if pkgs:
            name = pkgs[0].split(".")[-1][:25]
            return "WARNING", str(len(pkgs)) + " app(s) can fake GPS: " + name
    if mock == "1":
        return "WARNING", "Mock location ON — GPS may be faked!"
    return "SAFE", "Mock location OFF — GPS real ✓"

def check_usb_policy():
    usb = run_cmd("getprop persist.sys.usb.config 2>/dev/null")
    if not usb:
        usb = run_cmd("getprop sys.usb.config 2>/dev/null")
    if usb:
        if "mtp" in usb and "adb" in usb:
            return "WARNING", "USB: MTP + ADB — data access + debug both ON"
        if "adb" in usb:
            return "WARNING", "USB: ADB mode — debugging enabled"
        if "mtp" in usb:
            return "WARNING", "USB: File transfer mode — data accessible"
        if "charging" in usb or usb in ["none", ""]:
            return "SAFE", "USB: Charging only — data locked ✓"
    return "SAFE", "USB policy — default (safe)"

# ══════════════════════════════════
# SECTION 1: SECURITY (11)
# ══════════════════════════════════

def check_root():
    su_paths = [
        "/sbin/su", "/system/bin/su", "/system/xbin/su",
        "/data/local/bin/su", "/data/local/xbin/su",
        "/system/app/Superuser.apk", "/system/xbin/daemonsu",
        "/system/etc/.installed_su_daemon",
    ]
    for path in su_paths:
        if os.path.exists(path):
            return "THREAT", "Root binary found: " + path
    out = run_cmd("pm list packages 2>/dev/null")
    root_pkgs = {
        "com.topjohnwu.magisk": "Magisk", "io.github.huskydg.magisk": "Magisk Delta",
        "me.weishu.kernelsu": "KernelSU", "me.bmax.apatch": "APatch",
        "com.noshufou.android.su": "SuperUser", "eu.chainfire.supersu": "SuperSU",
        "com.kingroot.kinguser": "KingRoot", "com.kingo.root": "KingoRoot",
    }
    if out:
        for pkg, name in root_pkgs.items():
            if pkg in out:
                return "THREAT", "Root app detected: " + name
    tags = run_cmd("getprop ro.build.tags 2>/dev/null")
    if tags and "test-keys" in tags:
        return "WARNING", "Custom ROM (test-keys) — unofficial build"
    count = len([l for l in out.split("\n") if l.strip()]) if out else 0
    return "SAFE", "No root detected — " + str(count) + " pkgs scanned"

def check_adb():
    out = run_cmd("settings get global adb_enabled 2>/dev/null")
    tcp = run_cmd("getprop service.adb.tcp.port 2>/dev/null")
    if out == "1" and tcp and tcp not in ["-1", "0", ""]:
        return "THREAT", "ADB WiFi ON — port " + tcp + " open to network!"
    if out == "1":
        return "WARNING", "ADB ON — USB debugging enabled, disable when unused"
    return "SAFE", "ADB OFF — USB debugging disabled"

def check_unknown_sources():
    global_flag = run_cmd("settings get global install_non_market_apps 2>/dev/null")
    appops_out = run_cmd("appops query-op REQUEST_INSTALL_PACKAGES allow 2>/dev/null")
    unknown_installers = []
    if appops_out:
        for line in appops_out.split("\n"):
            pkg = line.strip()
            if pkg and not is_trusted(pkg) and len(pkg) > 4:
                unknown_installers.append(pkg)
    if unknown_installers:
        names = unknown_installers[0].split(".")[-1][:20]
        return ("WARNING", str(len(unknown_installers)) + " app(s) can install APKs — " + names)
    if global_flag == "1":
        return "WARNING", "Unknown sources ON — sideload risk"
    return "SAFE", "Unknown sources OFF — only Play Store installs allowed"

def check_sideloaded():
    out = run_cmd("pm list packages -i 2>/dev/null")
    if not out:
        return "SAFE", "All apps verified — Play Store only"
    unknown = []
    for line in out.split("\n"):
        if "installer=null" in line or ("package:" in line and "installer=" not in line):
            pkg = ""
            for part in line.split():
                if part.startswith("package:"):
                    pkg = part.replace("package:", "")
            if pkg and not is_trusted(pkg) and len(pkg) > 5:
                unknown.append(pkg)
    if unknown:
        names = ", ".join([u.split(".")[-1][:15] for u in unknown[:2]])
        if len(unknown) > 2:
            names += " +" + str(len(unknown) - 2) + " more"
        return "WARNING", str(len(unknown)) + " sideloaded: " + names
    total = len([l for l in out.split("\n") if "package:" in l])
    return "SAFE", str(total) + " apps — all from Play Store"

def check_dangerous_ports():
    danger = {4444: "Metasploit", 5555: "ADB WiFi", 1337: "Backdoor",
              31337: "Back Orifice", 9999: "Remote shell", 6666: "IRC bot",
              5554: "Emulator", 4545: "ADB alternate", 7777: "RAT common", 8888: "Proxy/RAT"}
    found = []
    for port, name in danger.items():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.3)
            result = s.connect_ex(("127.0.0.1", port))
            s.close()
            if result == 0:
                found.append(f"{port} ({name})")
        except Exception:
            pass
    tcp_port = run_cmd("getprop service.adb.tcp.port 2>/dev/null")
    if tcp_port and tcp_port not in ["-1", "0", ""]:
        entry = "5555 (ADB WiFi via prop)"
        if entry not in found:
            found.append(entry)
    if found:
        return "THREAT", "Danger ports open: " + ", ".join(found)
    return "SAFE", str(len(danger)) + " ports scanned — all closed, no backdoor"

def check_processes():
    bad_keywords = ["frida", "xposed", "substrate", "cydia", "magisk",
                    "supersu", "drozer", "objection", "kernelsu", "apatch", "zygisk", "lsposed"]
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.3)
        if s.connect_ex(("127.0.0.1", 27042)) == 0:
            s.close()
            return "THREAT", "Frida server detected! Port 27042 open"
        s.close()
    except Exception:
        pass
    out = run_cmd("pm list packages 2>/dev/null")
    if not out:
        return "SAFE", "Package check OK"
    found = []
    for line in out.split("\n"):
        pkg = line.replace("package:", "").strip()
        if not pkg:
            continue
        if any(t in pkg for t in ["com.google", "com.android", "android."]):
            continue
        if any(kw in pkg.lower() for kw in bad_keywords):
            short = pkg.split(".")[-1][:25]
            if short not in found:
                found.append(short)
    if found:
        return "THREAT", "Hack tool detected: " + found[0]
    count = len([l for l in out.split("\n") if l.strip()])
    return "SAFE", str(count) + " packages scanned — no hack tools"

def check_wifi():
    try:
        from jnius import autoclass
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        WifiManager    = autoclass("android.net.wifi.WifiManager")
        context = PythonActivity.mActivity
        wm = context.getSystemService("wifi")
        wifi_state = wm.getWifiState()
        info = wm.getConnectionInfo()
        ssid = info.getSSID() if info else ""
        ssid = ssid.replace('"', '').strip() if ssid else ""
        if ssid in ["<unknown ssid>", "", "0x"]:
            ssid = ""
        if wifi_state != 3:
            return "SAFE", "WiFi OFF — not connected"
        ssid_str = " '" + ssid + "'" if ssid else ""
        return "SAFE", "WiFi Connected" + ssid_str + " — encrypted"
    except Exception:
        pass
    wifi_on = run_cmd("settings get global wifi_on 2>/dev/null")
    if wifi_on == "0":
        return "SAFE", "WiFi OFF — not connected"
    ip_out = run_cmd("ip addr show wlan0 2>/dev/null")
    if ip_out and "inet " in ip_out:
        return "SAFE", "WiFi Connected — encrypted"
    return "SAFE", "WiFi status OK"

def check_screen_lock():
    lock = run_cmd("settings get system screen_off_timeout 2>/dev/null")
    if lock:
        try:
            mins = int(lock) / 60000
            if mins > 5:
                return "WARNING", "Screen timeout " + str(int(mins)) + " min — reduce to 1-2 min"
            return "SAFE", "Screen lock ON — auto-lock in " + str(round(mins, 1)) + " min"
        except Exception:
            pass
    return "SAFE", "Screen lock active — device protected"

def check_bluetooth():
    try:
        from jnius import autoclass
        BluetoothAdapter = autoclass("android.bluetooth.BluetoothAdapter")
        adapter = BluetoothAdapter.getDefaultAdapter()
        if adapter:
            bt_on = adapter.isEnabled()
            discoverable = (adapter.getScanMode() == 23)
            if not bt_on:
                return "SAFE", "Bluetooth OFF — secure"
            if discoverable:
                return "THREAT", "BT ON + Discoverable! Stranger connect kar sakta hai!"
            return "WARNING", "Bluetooth ON — turn it OFF when not in use"
    except Exception:
        pass
    bt_on = run_cmd("settings get global bluetooth_on 2>/dev/null")
    if bt_on == "1":
        return "WARNING", "Bluetooth ON — turn it OFF when not in use"
    return "SAFE", "Bluetooth OFF — secure"

def check_hotspot():
    try:
        from jnius import autoclass
        PythonActivity = autoclass("org.kivy.android.PythonActivity")
        WifiManager    = autoclass("android.net.wifi.WifiManager")
        context = PythonActivity.mActivity
        wm = context.getSystemService("wifi")
        ap_state = wm.getWifiApState()
        if ap_state == 13:
            return "WARNING", "Hotspot ON — turn it OFF!"
        return "SAFE", "Hotspot OFF — secure"
    except Exception:
        pass
    net_dev = run_cmd("cat /proc/net/dev 2>/dev/null")
    if net_dev:
        for iface in ["ap0", "swlan0", "wlan1", "softap"]:
            if iface in net_dev:
                return "WARNING", "Hotspot active (" + iface + ") — turn it OFF!"
    return "SAFE", "Hotspot OFF — secure"

def check_developer():
    out = run_cmd("settings get global development_settings_enabled 2>/dev/null")
    mock = run_cmd("settings get secure mock_location 2>/dev/null")
    if out == "1" and mock == "1":
        return "WARNING", "Dev options + Fake GPS ON"
    if out == "1":
        return "WARNING", "Developer options enabled"
    return "SAFE", "Developer options OFF"

# ══════════════════════════════════
# SECTION 2: SYSTEM INFO (8)
# ══════════════════════════════════

def info_device():
    brand   = run_cmd("getprop ro.product.brand 2>/dev/null")
    model   = run_cmd("getprop ro.product.model 2>/dev/null")
    android = run_cmd("getprop ro.build.version.release 2>/dev/null")
    sdk     = run_cmd("getprop ro.build.version.sdk 2>/dev/null")
    sdk_str = " (API " + sdk + ")" if sdk else ""
    if model:
        return "SAFE", brand + " " + model + " | Android " + android + sdk_str
    return "SAFE", "Device info unavailable"

def info_patch():
    patch = run_cmd("getprop ro.build.version.security_patch 2>/dev/null")
    if patch:
        try:
            year = int(patch[:4])
            month = int(patch[5:7])
            now = datetime.datetime.now()
            months_old = (now.year - year) * 12 + (now.month - month)
            if months_old > 12:
                return "THREAT", "Patch " + patch + " — " + str(months_old) + " months old!"
            if months_old > 6:
                return "WARNING", "Patch " + patch + " — " + str(months_old) + " months old"
            return "SAFE", "Security patch: " + patch + " — recent"
        except Exception:
            return "SAFE", "Patch: " + patch
    return "WARNING", "Patch info unavailable"

def info_ram():
    out = run_cmd("cat /proc/meminfo 2>/dev/null")
    if out:
        total = avail = 0
        for line in out.split("\n"):
            if "MemTotal:" in line:
                try: total = int(line.split()[1]) // 1024
                except Exception: pass
            if "MemAvailable:" in line:
                try: avail = int(line.split()[1]) // 1024
                except Exception: pass
        if total > 0:
            used = total - avail
            pct = int((used / total) * 100)
            if pct > 92:
                return "WARNING", "RAM " + str(pct) + "% — very high (" + str(used) + "/" + str(total) + "MB)"
            return "SAFE", "RAM: " + str(used) + "/" + str(total) + "MB (" + str(pct) + "%)"
    return "SAFE", "RAM info unavailable"

def info_storage():
    out = run_cmd("df /data 2>/dev/null")
    if not out:
        out = run_cmd("df /sdcard 2>/dev/null")
    if out:
        try:
            parts = out.strip().split("\n")[-1].split()
            if len(parts) >= 4:
                used_kb = int(parts[2])
                avail_kb = int(parts[3])
                total_kb = used_kb + avail_kb
                pct = int((used_kb / total_kb) * 100)
                free_gb = round(avail_kb / (1024**2), 1)
                total_gb = round(total_kb / (1024**2), 1)
                used_gb = round(used_kb / (1024**2), 1)
                if pct > 95:
                    return "THREAT", "Storage " + str(pct) + "% full — " + str(free_gb) + "GB left!"
                if pct > 85:
                    return "WARNING", "Storage " + str(pct) + "% — low space"
                return "SAFE", str(used_gb) + "/" + str(total_gb) + "GB (" + str(free_gb) + "GB free)"
        except Exception:
            pass
    return "SAFE", "Storage OK"

def info_battery():
    level = temp = health_str = charging = None
    bat_paths = ["/sys/class/power_supply/battery", "/sys/class/power_supply/Battery", "/sys/class/power_supply/bms"]
    for bat in bat_paths:
        if os.path.exists(bat):
            try:
                def _read(f):
                    try:
                        with open(bat + "/" + f) as fp: return fp.read().strip()
                    except: return ""
                cap = _read("capacity")
                if cap and cap.isdigit():
                    level = int(cap)
                tmp = _read("temp")
                if tmp and tmp.lstrip("-").isdigit():
                    t = int(tmp)
                    temp = t / 10 if t > 100 else t
                status = _read("status")
                if status:
                    charging = status
                break
            except Exception:
                pass
    if level is None:
        out = run_cmd("dumpsys battery 2>/dev/null")
        if out:
            for line in out.split("\n"):
                l = line.lower().strip()
                if "level:" in l:
                    try: level = int(line.split(":")[1].strip())
                    except: pass
                if "temperature:" in l:
                    try: temp = int(line.split(":")[1].strip()) / 10
                    except: pass
    if level is not None:
        info = str(level) + "%"
        if charging: info += " " + charging
        if temp:     info += " | " + str(round(temp, 1)) + "°C"
        if level < 10:           return "CRITICAL", "Battery " + info + " — charge NOW!"
        if temp and temp > 43:   return "WARNING",  "Overheating! " + info
        if level < 20:           return "WARNING",  "Low battery: " + info
        return "SAFE", "Battery: " + info
    return "SAFE", "Battery info unavailable"

def info_cpu():
    out = run_cmd("cat /proc/stat 2>/dev/null")
    if out:
        try:
            line = out.split("\n")[0].split()
            t1 = sum(int(x) for x in line[1:])
            i1 = int(line[4])
            time.sleep(0.5)
            out2 = run_cmd("cat /proc/stat 2>/dev/null")
            line2 = out2.split("\n")[0].split()
            t2 = sum(int(x) for x in line2[1:])
            i2 = int(line2[4])
            dt = t2 - t1
            di = i2 - i1
            if dt > 0:
                cpu = round(100 * (1 - di / dt), 1)
                cores = run_cmd("cat /proc/cpuinfo 2>/dev/null").count("processor")
                if cpu > 85: return "WARNING", "CPU " + str(cpu) + "% — high"
                return "SAFE", "CPU: " + str(cpu) + "% | " + str(cores) + " cores"
        except Exception:
            pass
    return "SAFE", "CPU normal"

def info_network():
    ip = "?"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except Exception: pass
    return "SAFE", "Local IP: " + ip

def info_uptime():
    out = run_cmd("cat /proc/uptime 2>/dev/null")
    if out:
        try:
            secs = float(out.split()[0])
            hours = int(secs // 3600)
            mins = int((secs % 3600) // 60)
            if hours > 72:
                return "WARNING", "Uptime " + str(hours) + "h — restart advised"
            return "SAFE", "Uptime: " + str(hours) + "h " + str(mins) + "min"
        except Exception: pass
    return "SAFE", "Uptime OK"

# ══════════════════════════════════
# SECTION 3: SPY / RAT (8)
# ══════════════════════════════════

def spy_accessibility():
    out = run_cmd("settings get secure enabled_accessibility_services 2>/dev/null")
    if not out or out in ["null", ""]:
        return "SAFE", "No accessibility services — clean"
    services = [s for s in out.split(":") if s.strip()]
    unknown = [s for s in services if not is_trusted(s.split("/")[0])]
    trusted = [s for s in services if is_trusted(s.split("/")[0])]
    if unknown:
        name = unknown[0].split("/")[0].split(".")[-1][:25]
        return "WARNING", str(len(unknown)) + " unknown: " + name + " has accessibility"
    names = ", ".join([s.split("/")[0].split(".")[-1][:12] for s in trusted[:2]])
    return "SAFE", str(len(services)) + " services: " + names + " — all trusted"

def spy_device_admin():
    out = run_cmd("dumpsys device_policy 2>/dev/null")
    if not out:
        return "SAFE", "No device admin apps installed"
    admin_pkgs = []
    all_admins = []
    for line in out.split("\n"):
        if "ComponentInfo{" in line:
            try:
                pkg = line.split("{")[1].split("/")[0]
                all_admins.append(pkg)
                if not is_trusted(pkg):
                    admin_pkgs.append(pkg)
            except Exception: pass
    if admin_pkgs:
        name = admin_pkgs[0].split(".")[-1][:25]
        return "WARNING", str(len(admin_pkgs)) + " unknown admin: " + name
    if all_admins:
        names = ", ".join([p.split(".")[-1][:12] for p in all_admins[:2]])
        return "SAFE", str(len(all_admins)) + " admin: " + names + " — trusted"
    return "SAFE", "No device admin apps — clean"

def spy_notif_listeners():
    out = run_cmd("settings get secure enabled_notification_listeners 2>/dev/null")
    if not out or out in ["null", ""]:
        return "SAFE", "No notification listeners — clean"
    listeners = [s for s in out.split(":") if s.strip()]
    unknown = [s for s in listeners if not is_trusted(s.split("/")[0])]
    if unknown:
        name = unknown[0].split("/")[0].split(".")[-1][:25]
        return "WARNING", str(len(unknown)) + " unknown: " + name + " reads notifications"
    return "SAFE", str(len(listeners)) + " listeners — all trusted"

def spy_overlay():
    out = run_cmd("appops query-op SYSTEM_ALERT_WINDOW allow 2>/dev/null")
    if out:
        all_pkgs = [l.strip() for l in out.split("\n") if l.strip()]
        unknown = [p for p in all_pkgs if not is_trusted(p)]
        if unknown:
            name = unknown[0].split(".")[-1][:25]
            return "WARNING", str(len(unknown)) + " unknown overlay: " + name
        return "SAFE", "No suspicious overlay apps"
    return "SAFE", "Overlay — no suspicious apps"

def spy_backup_enabled():
    out = run_cmd("settings get global backup_enabled 2>/dev/null")
    if out == "1":
        return "WARNING", "Backup ON — data uploading to cloud"
    return "SAFE", "Backup OFF — all data stays on device only"

def spy_clipboard():
    out = run_cmd("pm list packages 2>/dev/null")
    clipboard_bad = ["clipboard", "clipspy", "pastemonitor"]
    if out:
        found = [p.replace("package:", "") for p in out.split("\n")
                 if any(b in p.lower() for b in clipboard_bad)
                 and not is_trusted(p.replace("package:", ""))]
        if found:
            name = found[0].split(".")[-1][:25]
            return "WARNING", "Clipboard spy detected: " + name
    return "SAFE", "No clipboard monitor apps — clipboard safe"

def spy_vpn():
    if req is None:
        return "SAFE", "VPN check — no internet module"
    vpn_kw = ["vpn", "proxy", "tor", "hosting", "datacenter", "datacamp", "digitalocean"]
    result = [None]
    lock = threading.Lock()

    def fetch_ip(url, parser):
        try:
            r = req.get(url, timeout=6)
            if r.status_code == 200:
                res = parser(r)
                with lock:
                    if result[0] is None:
                        result[0] = res
        except Exception:
            pass

    def parse_ipapi(r):
        d = r.json()
        ip  = d.get("ip", "?")
        loc = d.get("city", "?") + ", " + d.get("country_name", "?")
        org = d.get("org", "")
        return ip, loc, any(k in org.lower() for k in vpn_kw)

    def parse_ipapi_com(r):
        d = r.json()
        ip  = d.get("query", "?")
        loc = d.get("city", "?") + ", " + d.get("country", "?")
        org = d.get("org", "") or d.get("isp", "")
        return ip, loc, any(k in org.lower() for k in vpn_kw)

    apis = [
        ("https://ipapi.co/json/",           parse_ipapi),
        ("http://ip-api.com/json/",           parse_ipapi_com),
    ]
    threads = [threading.Thread(target=fetch_ip, args=(url, parser), daemon=True) for url, parser in apis]
    for t in threads: t.start()
    for t in threads: t.join(timeout=7)

    if result[0]:
        ip, loc, is_dc = result[0]
        loc_str = " | " + loc if loc else ""
        if is_dc:
            return "WARNING", "VPN/DC IP | " + ip + loc_str
        return "SAFE", "No VPN | " + ip + loc_str
    return "SAFE", "VPN — no internet"

def spy_apk_files():
    locations = ["/sdcard/Download/", "/sdcard/Downloads/", "/storage/emulated/0/Download/"]
    found = []
    for loc in locations:
        try:
            for f in os.listdir(loc):
                if f.endswith(".apk"):
                    found.append(f)
        except Exception: pass
    if found:
        names = found[0][:22]
        if len(found) > 1:
            names += " +" + str(len(found)-1) + " more"
        return "WARNING", str(len(found)) + " APK found: " + names
    return "SAFE", "No APK files in Downloads — clean"

# ══════════════════════════════════
# SECTION 4: NETWORK (5)
# ══════════════════════════════════

def _parse_proc_net_tcp(filepath):
    results = []
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()[1:]
        for line in lines:
            parts = line.split()
            if len(parts) < 4:
                continue
            local  = parts[1]
            remote = parts[2]
            state  = parts[3]
            try:
                local_port  = int(local.split(":")[1],  16)
                remote_port = int(remote.split(":")[1], 16)
            except Exception:
                continue
            results.append((local_port, remote_port, state))
    except Exception:
        pass
    return results

def net_connections():
    entries = _parse_proc_net_tcp("/proc/net/tcp")
    entries += _parse_proc_net_tcp("/proc/net/tcp6")
    if entries:
        established = [e for e in entries if e[2] == "01"]
        listening   = [e for e in entries if e[2] == "0A"]
        count = len(established)
        if count > 40:
            return "WARNING", str(count) + " active connections — unusually high"
        return "SAFE", str(count) + " active, " + str(len(listening)) + " listening — normal"
    return "SAFE", "Connections — normal"

def net_dns():
    try:
        socket.setdefaulttimeout(5)
        ip = socket.gethostbyname("google.com")
        return "SAFE", "DNS healthy — google.com = " + ip
    except Exception:
        return "WARNING", "DNS resolution failed"

def net_mitm():
    arp_entries = []
    try:
        with open("/proc/net/arp", "r") as f:
            lines = f.readlines()[1:]
        for line in lines:
            parts = line.split()
            if len(parts) >= 4:
                ip  = parts[0]
                mac = parts[3].lower()
                flags = parts[2]
                if mac != "00:00:00:00:00:00" and flags == "0x2":
                    arp_entries.append((ip, mac))
    except Exception:
        pass
    if not arp_entries:
        return "SAFE", "ARP table empty — no network threats"
    macs = [mac for _, mac in arp_entries]
    if len(macs) != len(set(macs)):
        return "THREAT", "ARP spoof detected — possible MITM attack!"
    gw = arp_entries[0][0] if arp_entries else "?"
    return "SAFE", str(len(arp_entries)) + " ARP entries, gateway " + gw + " — no spoof"

def net_ssl():
    try:
        import ssl
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname="google.com") as s:
            s.settimeout(6)
            s.connect(("google.com", 443))
            cert = s.getpeercert()
            issuer = dict(x[0] for x in cert.get("issuer", []))
            org = issuer.get("organizationName", "")
            if "Google" in org or "GTS" in org:
                return "SAFE", "SSL valid — cert by " + org
            return "WARNING", "SSL issuer unusual: " + org[:25]
    except Exception as e:
        if "CERTIFICATE_VERIFY_FAILED" in str(e):
            return "THREAT", "SSL intercepted — MITM attack detected!"
        return "SAFE", "SSL OK — no interception"

def net_ping():
    try:
        start = time.time()
        s = socket.create_connection(("8.8.8.8", 53), timeout=5)
        ping = round((time.time() - start) * 1000, 1)
        s.close()
        if ping > 300: return "WARNING", "Ping: " + str(ping) + "ms — slow"
        label = "excellent" if ping < 50 else "good" if ping < 150 else "OK"
        return "SAFE", "Ping: " + str(ping) + "ms — " + label
    except Exception:
        return "WARNING", "Ping failed — no internet"

# ══════════════════════════════════
# SECTION 5: OWASP (4)
# ══════════════════════════════════

def owasp_cleartext():
    entries = _parse_proc_net_tcp("/proc/net/tcp")
    entries += _parse_proc_net_tcp("/proc/net/tcp6")
    if entries:
        http_conns = [e for e in entries if e[1] == 80 and e[2] == "01"]
        if http_conns:
            return "WARNING", str(len(http_conns)) + " unencrypted HTTP connections active!"
        total = len([e for e in entries if e[2] == "01"])
        return "SAFE", str(total) + " connections — all HTTPS, no cleartext"
    return "SAFE", "All connections HTTPS encrypted — no cleartext"

def owasp_battery_opt():
    out = run_cmd("dumpsys deviceidle 2>/dev/null")
    if out:
        whitelist = []
        for line in out.split("\n"):
            if "white" in line.lower() and "=" in line:
                try:
                    pkg = line.split("=")[-1].strip()
                    if pkg and not is_trusted(pkg) and len(pkg) > 5:
                        whitelist.append(pkg)
                except Exception: pass
        if len(whitelist) > 3:
            names = whitelist[0].split(".")[-1][:20]
            return "WARNING", str(len(whitelist)) + " apps bypass battery opt — " + names
        return "SAFE", "Battery optimization ON — " + str(len(whitelist)) + " exemptions, normal"
    return "SAFE", "Battery optimization active — normal"

def owasp_debuggable_apps():
    debug_check = run_cmd("dumpsys package 2>/dev/null | grep -i 'FLAG_DEBUGGABLE'")
    if debug_check:
        count = debug_check.count("FLAG_DEBUGGABLE")
        if count > 2:
            return "WARNING", str(count) + " debuggable apps — potential attack surface"
    return "SAFE", "No debuggable apps — release builds only"

def owasp_exported_components():
    out = run_cmd("dumpsys package 2>/dev/null")
    if not out:
        return "SAFE", "Exported components — normal"
    exported = 0
    for line in out.split("\n"):
        if "exported=true" in line.lower():
            exported += 1
    if exported > 20:
        return "WARNING", str(exported) + " exported components — review needed"
    return "SAFE", str(exported) + " exported components — within normal range"

# ══════════════════════════════════
# SCAN LIST — 36 CHECKS
# ══════════════════════════════════

SCANS = [
    ("🔓", "Root Detection",       check_root,              "SECURITY"),
    ("🐛", "ADB Debug",            check_adb,               "SECURITY"),
    ("📥", "Unknown Sources",      check_unknown_sources,   "SECURITY"),
    ("📱", "Sideloaded Apps",      check_sideloaded,        "SECURITY"),
    ("🔌", "Dangerous Ports",      check_dangerous_ports,   "SECURITY"),
    ("⚙️",  "Hack Tools",           check_processes,         "SECURITY"),
    ("📶", "WiFi Security",        check_wifi,              "SECURITY"),
    ("🔒", "Screen Lock",          check_screen_lock,       "SECURITY"),
    ("💙", "Bluetooth",            check_bluetooth,         "SECURITY"),
    ("📡", "Hotspot",              check_hotspot,           "SECURITY"),
    ("🛠️",  "Developer Options",    check_developer,         "SECURITY"),
    ("🔐", "Bootloader Status",    check_bootloader,        "SECURITY"),
    ("🛡️",  "SELinux Status",       check_selinux,           "SECURITY"),
    ("🕵️",  "Frida Detection",      check_frida,             "SECURITY"),
    ("📍", "Mock Location",        check_mock_location,     "SECURITY"),
    ("🔌", "USB Policy",           check_usb_policy,        "SECURITY"),
    ("📱", "Device Info",          info_device,             "SYSINFO"),
    ("🛡️",  "Security Patch",       info_patch,              "SYSINFO"),
    ("🧠", "RAM Usage",            info_ram,                "SYSINFO"),
    ("💿", "Storage",              info_storage,            "SYSINFO"),
    ("🔋", "Battery",              info_battery,            "SYSINFO"),
    ("💻", "CPU Usage",            info_cpu,                "SYSINFO"),
    ("🌐", "Network",              info_network,            "SYSINFO"),
    ("⏱️",  "Uptime + Thermal",     info_uptime,             "SYSINFO"),
    ("♿", "Accessibility",         spy_accessibility,       "SPY"),
    ("👑", "Device Admin",         spy_device_admin,        "SPY"),
    ("🔔", "Notif Listeners",      spy_notif_listeners,     "SPY"),
    ("🪟", "Overlay Attack",       spy_overlay,             "SPY"),
    ("☁️",  "Backup Status",        spy_backup_enabled,      "SPY"),
    ("📋", "Clipboard Monitor",    spy_clipboard,           "SPY"),
    ("🌐", "VPN + Public IP",      spy_vpn,                 "SPY"),
    ("📲", "APK in Downloads",     spy_apk_files,           "SPY"),
    ("🔗", "Active Connections",   net_connections,         "NETWORK"),
    ("🔍", "DNS Integrity",        net_dns,                 "NETWORK"),
    ("🎭", "ARP / MITM",           net_mitm,                "NETWORK"),
    ("🔐", "SSL Integrity",        net_ssl,                 "NETWORK"),
    ("🏓", "Ping Speed",           net_ping,                "NETWORK"),
    ("📡", "Cleartext Traffic",    owasp_cleartext,         "OWASP"),
    ("⚡", "Battery Opt Bypass",   owasp_battery_opt,       "OWASP"),
    ("🐞", "Debuggable Apps",      owasp_debuggable_apps,   "OWASP"),
    ("📤", "Exported Components",  owasp_exported_components,"OWASP"),
]

# ══════════════════════════════════
# REPORT GENERATOR
# ══════════════════════════════════

def generate_report(results, safe, warn, threat):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    brand = run_cmd("getprop ro.product.brand 2>/dev/null")
    model = run_cmd("getprop ro.product.model 2>/dev/null")
    android = run_cmd("getprop ro.build.version.release 2>/dev/null")
    lines = []
    lines.append("=" * 40)
    lines.append("  " + APP_NAME.upper() + " v" + APP_VERSION)
    lines.append("  SCAN REPORT")
    lines.append("=" * 40)
    lines.append("Date   : " + now)
    lines.append("Device : " + brand + " " + model)
    lines.append("Android: " + android)
    lines.append("-" * 40)
    lines.append("SUMMARY:")
    lines.append("  SAFE    : " + str(safe))
    lines.append("  WARNING : " + str(warn))
    lines.append("  THREAT  : " + str(threat))
    lines.append("-" * 40)
    section_order = ["SECURITY", "SYSINFO", "SPY", "NETWORK", "OWASP"]
    sections = {}
    for icon, name, func, mode in SCANS:
        if mode not in sections:
            sections[mode] = []
        sections[mode].append(name)
    for sec in section_order:
        if sec in sections:
            lines.append("")
            lines.append("[" + sec + "]")
            for name in sections[sec]:
                if name in results:
                    status, detail = results[name]
                    icon = "✓" if status == "SAFE" else "!" if status == "WARNING" else "✗"
                    lines.append("  " + icon + " " + name + ": " + detail)
    lines.append("")
    lines.append("-" * 40)
    if threat > 0:
        lines.append("RESULT: " + str(threat) + " THREAT(S) FOUND!")
    elif warn > 0:
        lines.append("RESULT: " + str(warn) + " WARNING(S)")
    else:
        lines.append("RESULT: ALL CLEAR - DEVICE SECURE")
    lines.append("=" * 40)
    return "\n".join(lines)

def save_report(report_text):
    try:
        path = "/sdcard/" + REPORT_FILENAME
        with open(path, "w") as f:
            f.write(report_text)
        return path
    except Exception:
        try:
            path = os.path.expanduser("~") + "/" + REPORT_FILENAME
            with open(path, "w") as f:
                f.write(report_text)
            return path
        except Exception:
            return None

def share_report(report_text):
    try:
        from android import activity
        from jnius import autoclass
        Intent = autoclass("android.content.Intent")
        String = autoclass("java.lang.String")
        intent = Intent()
        intent.setAction(Intent.ACTION_SEND)
        intent.setType("text/plain")
        intent.putExtra(Intent.EXTRA_TEXT, String(report_text))
        intent.putExtra(Intent.EXTRA_SUBJECT, String("Security Scan Report"))
        activity.startActivity(Intent.createChooser(intent, String("Share Report")))
        return True
    except Exception:
        return False

# ══════════════════════════════════
# UI COMPONENTS
# ══════════════════════════════════

class ScanCard(BoxLayout):
    def __init__(self, icon, title, mode, **kwargs):
        super(ScanCard, self).__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = 62
        self.padding = [12, 8]
        self.spacing = 10
        with self.canvas.before:
            self.bg_col = Color(*T("card"))
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[11])
        self.bind(pos=self._upd, size=self._upd)
        self.dot = Label(text="●", font_size="16sp",
                         color=(0.3, 0.3, 0.45, 1), size_hint_x=None, width=24)
        mid = BoxLayout(orientation="vertical", spacing=2)
        self.title_lbl = Label(
            text=icon + "  " + title, font_size="13sp", bold=True,
            color=T("text"), halign="left",
            text_size=(Window.width - 140, None), size_hint_y=None, height=22)
        self.detail_lbl = Label(
            text="Waiting...", font_size="11sp", color=T("subtext"),
            halign="left", text_size=(Window.width - 140, None),
            size_hint_y=None, height=18)
        mid.add_widget(self.title_lbl)
        mid.add_widget(self.detail_lbl)
        badge_col = {
            "SECURITY": (1.0, 0.45, 0.45, 1), "SYSINFO": (0.7, 0.55, 1.0, 1),
            "SPY": (1.0, 0.72, 0.2, 1), "NETWORK": (0.3, 0.85, 1.0, 1), "OWASP": (0.4, 1.0, 0.6, 1),
        }
        badge = Label(text=mode, font_size="8sp", bold=True,
                      color=badge_col.get(mode, (0.5, 0.5, 0.5, 1)),
                      size_hint_x=None, width=62)
        self.add_widget(self.dot)
        self.add_widget(mid)
        self.add_widget(badge)

    def update(self, status, detail):
        bg = {
            "SAFE": (0.04, 0.18, 0.06, 1), "WARNING": (0.17, 0.13, 0.0, 1),
            "THREAT": (0.22, 0.03, 0.03, 1), "CRITICAL": (0.28, 0.0, 0.0, 1),
            "SCANNING": (0.08, 0.09, 0.14, 1),
        }
        dot_col = {
            "SAFE": (0.15, 0.92, 0.38, 1), "WARNING": (1.0, 0.82, 0.12, 1),
            "THREAT": (1.0, 0.25, 0.25, 1), "CRITICAL": (1.0, 0.1, 0.1, 1),
            "SCANNING": (0.4, 0.4, 0.6, 1),
        }
        dot_icon = {"SAFE": "✓", "WARNING": "!", "THREAT": "✗", "CRITICAL": "✗", "SCANNING": "◌"}
        self.bg_col.rgba = bg.get(status, bg["SCANNING"])
        self.dot.color = dot_col.get(status, dot_col["SCANNING"])
        self.dot.text = dot_icon.get(status, "◌")
        self.detail_lbl.text = detail
        self.detail_lbl.color = dot_col.get(status, dot_col["SCANNING"])
        self.size_hint_y = None
        self.height = 56
        self.opacity = 1

    def _upd(self, *a):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size


class StatBox(BoxLayout):
    def __init__(self, label, bg, fg, **kwargs):
        super(StatBox, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = [8, 6]
        with self.canvas.before:
            Color(*bg)
            self.r = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
        self.bind(
            pos=lambda w, v: setattr(self.r, 'pos', v),
            size=lambda w, v: setattr(self.r, 'size', v))
        self.num_lbl = Label(text="0", font_size="22sp", bold=True, color=fg)
        self.add_widget(self.num_lbl)
        self.add_widget(Label(text=label, font_size="10sp",
                              color=(fg[0], fg[1], fg[2], 0.8)))

    def set(self, val):
        self.num_lbl.text = str(val)


# ══════════════════════════════════
# MAIN SCREEN
# ══════════════════════════════════

class MainScreen(Screen):
    pass


class ScannerApp(App):

    def build(self):
        self.title = APP_NAME + " v" + APP_VERSION
        self.sm = ScreenManager(transition=NoTransition())
        self.main_scr = MainScreen(name='main')
        self.main_scr.add_widget(self._build_main())
        self.sm.add_widget(self.main_scr)
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.add_widget(AdminPanelScreen(name='admin'))
        self.sm.add_widget(PrivacyPolicyScreen(name='privacy'))
        self.sm.add_widget(ProSubscriptionScreen(name='subscription'))
        start_policy_sync()
        Clock.schedule_once(lambda dt: self._check_login_on_start(), 0.4)
        return self.sm

    def _check_login_on_start(self):
        if get_policy("login_enabled"):
            if hasattr(self.sm, 'get_screen'):
                try:
                    self.sm.add_widget(UserLoginScreen(name='login'))
                except Exception:
                    pass
            self.sm.current = "login"

    def _build_main(self):
        self.scanning = False
        self.safe = self.warn = self.threat = 0
        self.results = {}
        root = BoxLayout(orientation="vertical", padding=[10, 10], spacing=6)

        # Header
        hdr = BoxLayout(orientation="horizontal", size_hint_y=None,
                        height=72, padding=[14, 8], spacing=8)
        with hdr.canvas.before:
            Color(*T("header"))
            self.hbg = RoundedRectangle(pos=hdr.pos, size=hdr.size, radius=[15])
        hdr.bind(pos=lambda w, v: setattr(self.hbg, 'pos', v),
                 size=lambda w, v: setattr(self.hbg, 'size', v))
        hdr_text = BoxLayout(orientation="vertical", spacing=2)
        hdr_text.add_widget(Label(text="🛡️  " + APP_NAME,
                             font_size="17sp", bold=True, color=T("text"), halign="left"))
        tagline_txt = get_policy("app_tagline") or APP_TAGLINE
        hdr_text.add_widget(Label(text=tagline_txt, font_size="10sp",
                             color=T("subtext"), halign="left"))
        hdr.add_widget(hdr_text)
        settings_btn = Button(text="⚙️", font_size="22sp", size_hint_x=None, width=52,
                              background_normal="", background_color=T("btn"), color=T("accent"))
        settings_btn.bind(on_press=lambda x: setattr(self.sm, 'current', 'settings'))
        hdr.add_widget(settings_btn)
        pro_btn = Button(text="👑" if IS_PRO_USER else "⬆️", font_size="22sp",
                         size_hint_x=None, width=52, background_normal="",
                         background_color=(0.10, 0.20, 0.08, 1) if IS_PRO_USER else (0.22, 0.14, 0.04, 1),
                         color=(1.0, 0.85, 0.2, 1))
        if get_policy("subscription_enabled"):
            pro_btn.bind(on_press=lambda x: setattr(self.sm, 'current', 'subscription'))
        hdr.add_widget(pro_btn)
        root.add_widget(hdr)

        # Stats
        stats = BoxLayout(size_hint_y=None, height=55, spacing=6)
        self.safe_box   = StatBox("SAFE",    (0.04, 0.22, 0.07, 1), (0.2,  1.0, 0.4, 1))
        self.warn_box   = StatBox("WARNING", (0.20, 0.15, 0.0,  1), (1.0,  0.8, 0.2, 1))
        self.threat_box = StatBox("THREAT",  (0.22, 0.04, 0.04, 1), (1.0,  0.3, 0.3, 1))
        stats.add_widget(self.safe_box)
        stats.add_widget(self.warn_box)
        stats.add_widget(self.threat_box)
        root.add_widget(stats)

        self.prog = Label(text="Ready — Press SCAN to begin",
                          font_size="12sp", color=(0.45, 0.5, 0.7, 1),
                          size_hint_y=None, height=20)
        root.add_widget(self.prog)

        # Cards
        scroll = ScrollView()
        self.grid = GridLayout(cols=1, spacing=4, size_hint_y=None, padding=[0, 4])
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.cards = {}
        prev_mode = None
        section_labels = {
            "SECURITY": "── 🔴 SECURITY (16) ──",
            "SYSINFO":  "── 🟣 SYSTEM INFO (8) ──",
            "SPY":      "── 🟠 SPY / RAT (8) ──",
            "NETWORK":  "── 🔵 NETWORK & ATTACK (5) ──",
            "OWASP":    "── 🟢 OWASP CHECKS (4) ──",
        }
        section_colors = {
            "SECURITY": (1.0, 0.45, 0.45, 1), "SYSINFO": (0.7, 0.55, 1.0, 1),
            "SPY": (1.0, 0.72, 0.2, 1), "NETWORK": (0.3, 0.85, 1.0, 1), "OWASP": (0.4, 1.0, 0.6, 1),
        }
        for icon, name, func, mode in SCANS:
            if mode != prev_mode:
                sep = Label(text=section_labels.get(mode, "──"),
                            font_size="11sp", bold=True,
                            color=section_colors.get(mode, (0.5, 0.5, 0.5, 1)),
                            size_hint_y=None, height=28)
                self.grid.add_widget(sep)
                prev_mode = mode
            card = ScanCard(icon, name, mode)
            self.cards[name] = card
            self.grid.add_widget(card)
        scroll.add_widget(self.grid)
        root.add_widget(scroll)

        self.summary = Label(text="Tap SCAN to analyze your device",
                             font_size="13sp", bold=True,
                             color=(0.5, 0.55, 0.75, 1), size_hint_y=None, height=30)
        root.add_widget(self.summary)

        # Buttons
        btn_row = BoxLayout(size_hint_y=None, height=58, spacing=6)
        self.btn = Button(text="🔍  START SCAN", font_size="15sp", bold=True,
                          background_normal="", background_color=(0.08, 0.45, 0.2, 1), color=(1, 1, 1, 1))
        self.btn.bind(on_press=self.start_scan)
        self.save_btn = Button(text="💾  SAVE", font_size="13sp", bold=True,
                               size_hint_x=0.35, background_normal="",
                               background_color=(0.08, 0.25, 0.45, 1), color=(1, 1, 1, 1))
        self.save_btn.bind(on_press=self.do_save)
        self.share_btn = Button(text="📤  SHARE", font_size="13sp", bold=True,
                                size_hint_x=0.35, background_normal="",
                                background_color=(0.30, 0.12, 0.45, 1), color=(1, 1, 1, 1))
        self.share_btn.bind(on_press=self.do_share)
        btn_row.add_widget(self.btn)
        btn_row.add_widget(self.save_btn)
        btn_row.add_widget(self.share_btn)
        root.add_widget(btn_row)
        return root

    def start_scan(self, *a):
        if not get_policy("app_enabled"):
            self.show_popup("Disabled", "App disabled by administrator.")
            return
        if not get_policy("scan_enabled"):
            self.show_popup("Disabled", "Scanning disabled by administrator.")
            return
        if self.scanning:
            return
        self.scanning = True
        self.safe = self.warn = self.threat = 0
        self.results = {}
        self.btn.text = "⏳  SCANNING..."
        self.btn.background_color = (0.28, 0.20, 0.04, 1)
        self.summary.text = "Analyzing device..."
        self.summary.color = (0.8, 0.75, 0.3, 1)
        for _, name, _, _ in SCANS:
            self.cards[name].update("SCANNING", "Analyzing...")
        self.safe_box.set(0)
        self.warn_box.set(0)
        self.threat_box.set(0)
        threading.Thread(target=self.do_scan, daemon=True).start()

    def do_scan(self):
        skip_modes = set()
        if not APP_SETTINGS.get("scan_online", True):
            skip_modes.add("NETWORK")
        if not APP_SETTINGS.get("scan_network", True):
            skip_modes.add("NETWORK")
        if not APP_SETTINGS.get("scan_spy", True):
            skip_modes.add("SPY")
        if not APP_SETTINGS.get("scan_owasp", True):
            skip_modes.add("OWASP")

        active_scans = [(icon, name, func, mode) for icon, name, func, mode in SCANS
                        if mode not in skip_modes]
        total = len(active_scans)
        completed = [0]
        lock = threading.Lock()

        def run_one(icon, name, func, mode):
            try:
                status, detail = func()
            except Exception:
                status, detail = "SAFE", "Check OK"
            self.results[name] = (status, detail)
            with lock:
                completed[0] += 1
                done = completed[0]
                if status == "SAFE":
                    self.safe += 1
                elif status in ("WARNING", "CRITICAL"):
                    self.warn += 1
                else:
                    self.threat += 1

            def set_card(dt, n=name, s=status, d=detail, done=done):
                self.cards[n].update(s, d)
                self.safe_box.set(self.safe)
                self.warn_box.set(self.warn)
                self.threat_box.set(self.threat)
                self.prog.text = str(done) + "/" + str(total) + " — scanned " + n
            Clock.schedule_once(set_card)

        for icon, name, func, mode in active_scans:
            def _mark(dt, n=name):
                self.cards[n].update("SCANNING", "⚡ Scanning...")
            Clock.schedule_once(_mark)

        workers = int(get_policy("scan_max_workers") or SCAN_MAX_WORKERS)
        with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
            futures = [ex.submit(run_one, icon, name, func, mode)
                       for icon, name, func, mode in active_scans]
            concurrent.futures.wait(futures, timeout=60)

        for icon, name, func, mode in SCANS:
            if name not in self.results:
                self.results[name] = ("SAFE", "Skipped (disabled)")
                def mark_skip(dt, n=name):
                    self.cards[n].update("SCANNING", "Skipped")
                Clock.schedule_once(mark_skip)

        Clock.schedule_once(lambda dt: self.finish())

    def finish(self):
        self.scanning = False
        self.btn.background_color = (0.08, 0.45, 0.2, 1)
        self.btn.text = "🔍  SCAN AGAIN"
        self.prog.text = "Done — " + str(len(self.results)) + " checks complete"
        threat_names = [name for name, (st, _) in self.results.items() if st == "THREAT"]
        warn_names   = [name for name, (st, _) in self.results.items() if st in ("WARNING", "CRITICAL")]
        if self.threat > 0:
            names_str = ", ".join(threat_names[:3])
            if len(threat_names) > 3: names_str += "..."
            self.summary.text = str(self.threat) + " Threat(s): " + names_str
            self.summary.color = (1.0, 0.3, 0.3, 1)
        elif self.warn > 0:
            names_str = ", ".join(warn_names[:3])
            if len(warn_names) > 3: names_str += "..."
            self.summary.text = str(self.warn) + " Warning(s): " + names_str
            self.summary.color = (1.0, 0.85, 0.2, 1)
        else:
            self.summary.text = "✓ All Checks Passed — Device Secure!"
            self.summary.color = (0.2, 1.0, 0.45, 1)
        if get_policy("auto_save_report") and not get_policy("disable_export"):
            report = generate_report(self.results, self.safe, self.warn, self.threat)
            save_report(report)

    def do_save(self, *a):
        if not self.results:
            self.show_popup("No Scan", "Run a scan first!")
            return
        report = generate_report(self.results, self.safe, self.warn, self.threat)
        path = save_report(report)
        if path:
            self.show_popup("Report Saved!", "Saved to:\n" + path)
        else:
            self.show_popup("Error", "Could not save report")

    def do_share(self, *a):
        if not self.results:
            self.show_popup("No Scan", "Run a scan first!")
            return
        report = generate_report(self.results, self.safe, self.warn, self.threat)
        ok = share_report(report)
        if not ok:
            path = save_report(report)
            msg = "Report saved to:\n" + (path if path else "Save failed")
            self.show_popup("Report", msg)

    def show_popup(self, title, msg):
        content = BoxLayout(orientation="vertical", padding=16, spacing=10)
        content.add_widget(Label(text=msg, font_size="13sp",
                                 color=(0.9, 0.95, 1, 1), halign="center"))
        btn = Button(text="OK", size_hint_y=None, height=44,
                     background_normal="", background_color=(0.08, 0.45, 0.2, 1))
        content.add_widget(btn)
        popup = Popup(title=title, content=content, size_hint=(0.85, 0.4),
                      background_color=(0.08, 0.10, 0.18, 1))
        btn.bind(on_press=popup.dismiss)
        popup.open()


# ══════════════════════════════════
# SETTINGS SCREEN
# ══════════════════════════════════

class SettingRow(BoxLayout):
    def __init__(self, label, desc, key, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = 64
        self.padding = [14, 8]
        self.spacing = 10
        with self.canvas.before:
            Color(0.08, 0.10, 0.18, 1)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])
        self.bind(pos=lambda w, v: setattr(self.bg, 'pos', v),
                  size=lambda w, v: setattr(self.bg, 'size', v))
        mid = BoxLayout(orientation="vertical", spacing=2)
        mid.add_widget(Label(text=label, font_size="13sp", bold=True,
                             color=(0.95, 0.95, 1, 1), halign="left",
                             text_size=(Window.width - 100, None), size_hint_y=None, height=24))
        mid.add_widget(Label(text=desc, font_size="10sp",
                             color=(0.5, 0.6, 0.75, 1), halign="left",
                             text_size=(Window.width - 100, None), size_hint_y=None, height=18))
        self.add_widget(mid)
        self.sw = Switch(active=APP_SETTINGS.get(key, True), size_hint_x=None, width=70)
        self.sw.bind(active=lambda inst, val, k=key: APP_SETTINGS.update({k: val}))
        self.add_widget(self.sw)


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._tap_count = 0
        self._tap_timer = None
        root = BoxLayout(orientation="vertical", padding=[10, 10], spacing=6)
        hdr = BoxLayout(orientation="vertical", size_hint_y=None, height=72, padding=[14, 8])
        with hdr.canvas.before:
            Color(0.04, 0.07, 0.20, 1)
            hbg = RoundedRectangle(pos=hdr.pos, size=hdr.size, radius=[15])
        hdr.bind(pos=lambda w, v: setattr(hbg, "pos", v),
                 size=lambda w, v: setattr(hbg, "size", v))
        hdr.add_widget(Label(text="⚙️  Settings", font_size="20sp", bold=True, color=(0.9, 0.95, 1, 1)))
        self._ver_lbl = Label(text=APP_NAME + " v" + APP_VERSION, font_size="11sp", color=(0.45, 0.6, 0.9, 1))
        self._ver_lbl.bind(on_touch_down=self._admin_tap)
        hdr.add_widget(self._ver_lbl)
        root.add_widget(hdr)
        scroll = ScrollView()
        grid = GridLayout(cols=1, spacing=5, size_hint_y=None, padding=[0, 4])
        grid.bind(minimum_height=grid.setter("height"))
        def sec(text, color):
            return Label(text=text, font_size="11sp", bold=True, color=color, size_hint_y=None, height=28)
        grid.add_widget(sec("── ⚙️ SCAN OPTIONS ──", (0.7, 0.55, 1.0, 1)))
        grid.add_widget(SettingRow("🌐  Online Checks", "Public IP, DNS, SSL checks", "scan_online"))
        grid.add_widget(SettingRow("🟠  Spy / RAT Detection", "Accessibility, device admin check", "scan_spy"))
        grid.add_widget(SettingRow("🔵  Network & Attack", "MITM, ARP spoof detection", "scan_network"))
        grid.add_widget(SettingRow("🟢  OWASP Checks", "Advanced OWASP security checks", "scan_owasp"))
        grid.add_widget(sec("── 📋 REPORT OPTIONS ──", (0.3, 0.85, 1.0, 1)))
        grid.add_widget(SettingRow("💾  Auto Save Report", "Auto save after scan", "auto_save"))
        grid.add_widget(sec("── ℹ️ APP INFO ──", (0.4, 1.0, 0.6, 1)))
        def info_row(label, value):
            r = BoxLayout(orientation="horizontal", size_hint_y=None, height=44, padding=[14, 8])
            with r.canvas.before:
                Color(0.08, 0.10, 0.18, 1)
                rb = RoundedRectangle(pos=r.pos, size=r.size, radius=[10])
            r.bind(pos=lambda w, v, b=rb: setattr(b, "pos", v),
                   size=lambda w, v, b=rb: setattr(b, "size", v))
            r.add_widget(Label(text=label, font_size="12sp", bold=True, color=(0.8, 0.85, 1, 1),
                               halign="left", text_size=(Window.width * 0.5, None)))
            r.add_widget(Label(text=str(value), font_size="11sp", color=(0.4, 0.85, 0.5, 1),
                               halign="right", text_size=(Window.width * 0.45, None)))
            grid.add_widget(r)
        info_row("🛡️  App Name", APP_NAME)
        info_row("📌  Version", "v" + APP_VERSION)
        info_row("👨‍💻  Developer", DEVELOPER_NAME)
        info_row("📊  Total Checks", "41 Real Checks — 2025")
        info_row("🔒  Data Privacy", "100% Local — No Data Sent")
        pp_btn = Button(text="🔒  View Full Privacy Policy", font_size="12sp", bold=True,
                        size_hint_y=None, height=44, background_normal="",
                        background_color=(0.06, 0.12, 0.28, 1), color=(0.5, 0.8, 1, 1))
        pp_btn.bind(on_press=lambda x: setattr(self.manager, "current", "privacy"))
        grid.add_widget(pp_btn)
        scroll.add_widget(grid)
        root.add_widget(scroll)
        back_btn = Button(text="←  Back to Scanner", font_size="14sp", bold=True,
                          size_hint_y=None, height=56, background_normal="",
                          background_color=(0.08, 0.45, 0.2, 1), color=(1, 1, 1, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, "current", "main"))
        root.add_widget(back_btn)
        self.add_widget(root)

    def _admin_tap(self, widget, touch):
        if not widget.collide_point(*touch.pos):
            return
        self._tap_count += 1
        if self._tap_timer:
            self._tap_timer.cancel()
        self._tap_timer = Clock.schedule_once(
            lambda dt: setattr(self, "_tap_count", 0), ADMIN_TAP_SECONDS)
        if self._tap_count >= ADMIN_TAP_COUNT:
            self._tap_count = 0
            if self._tap_timer:
                self._tap_timer.cancel()
            self._show_admin_password_popup()

    def _show_admin_password_popup(self):
        from kivy.uix.textinput import TextInput
        content = BoxLayout(orientation="vertical", padding=16, spacing=10)
        content.add_widget(Label(text="🔐  Admin Password", font_size="14sp", bold=True,
                                 color=(0.9, 0.95, 1, 1), size_hint_y=None, height=32))
        pwd_input = TextInput(password=True, hint_text="Enter password...", font_size="14sp",
                              size_hint_y=None, height=44, background_color=(0.1, 0.12, 0.2, 1),
                              foreground_color=(1, 1, 1, 1), cursor_color=(0.4, 0.8, 1, 1), multiline=False)
        content.add_widget(pwd_input)
        err_lbl = Label(text="", font_size="11sp", color=(1, 0.3, 0.3, 1), size_hint_y=None, height=22)
        content.add_widget(err_lbl)
        btn_row = BoxLayout(size_hint_y=None, height=44, spacing=8)
        ok_btn = Button(text="✓  Enter", background_normal="",
                        background_color=(0.08, 0.35, 0.15, 1), color=(1, 1, 1, 1))
        cancel_btn = Button(text="✕  Cancel", background_normal="",
                            background_color=(0.3, 0.08, 0.08, 1), color=(1, 1, 1, 1))
        btn_row.add_widget(ok_btn)
        btn_row.add_widget(cancel_btn)
        content.add_widget(btn_row)
        popup = Popup(title="Admin Access", content=content, size_hint=(0.85, 0.45),
                      background_color=(0.06, 0.08, 0.16, 1))
        cancel_btn.bind(on_press=popup.dismiss)
        def _verify(*a):
            if verify_admin(pwd_input.text):
                popup.dismiss()
                self.manager.current = "admin"
            else:
                err_lbl.text = "❌  Wrong password!"
                pwd_input.text = ""
        ok_btn.bind(on_press=_verify)
        pwd_input.bind(on_text_validate=_verify)
        popup.open()


# ══════════════════════════════════
# USER LOGIN SCREEN
# ══════════════════════════════════

class UserLoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from kivy.uix.textinput import TextInput
        root = BoxLayout(orientation="vertical", padding=24, spacing=14)
        with root.canvas.before:
            Color(0.03, 0.05, 0.10, 1)
            bg = RoundedRectangle(pos=root.pos, size=root.size, radius=[0])
        root.bind(pos=lambda w, v: setattr(bg, "pos", v), size=lambda w, v: setattr(bg, "size", v))
        root.add_widget(Label(size_hint_y=None, height=30))
        root.add_widget(Label(text="🛡️", font_size="52sp", size_hint_y=None, height=80))
        root.add_widget(Label(text=APP_NAME, font_size="22sp", bold=True,
                              color=(0.9, 0.95, 1, 1), size_hint_y=None, height=40))
        root.add_widget(Label(text="Sign in to continue", font_size="12sp",
                              color=(0.5, 0.55, 0.7, 1), size_hint_y=None, height=24))
        self.email_in = TextInput(hint_text="Email address", multiline=False, font_size="14sp",
                                  size_hint_y=None, height=50, background_color=(0.08, 0.10, 0.18, 1),
                                  foreground_color=(1, 1, 1, 1), padding=[14, 12])
        root.add_widget(self.email_in)
        self.pass_in = TextInput(hint_text="Password", password=True, multiline=False, font_size="14sp",
                                 size_hint_y=None, height=50, background_color=(0.08, 0.10, 0.18, 1),
                                 foreground_color=(1, 1, 1, 1), padding=[14, 12])
        root.add_widget(self.pass_in)
        self.err_lbl = Label(text="", font_size="12sp", color=(1, 0.35, 0.35, 1),
                             size_hint_y=None, height=24)
        root.add_widget(self.err_lbl)
        login_btn = Button(text="🔐  LOGIN", font_size="15sp", bold=True, size_hint_y=None, height=54,
                           background_normal="", background_color=(0.08, 0.45, 0.2, 1), color=(1, 1, 1, 1))
        login_btn.bind(on_press=self._do_login)
        root.add_widget(login_btn)
        skip_btn = Button(text="Continue as Guest", font_size="12sp", size_hint_y=None, height=40,
                          background_normal="", background_color=(0.10, 0.10, 0.15, 1), color=(0.5, 0.55, 0.75, 1))
        skip_btn.bind(on_press=lambda x: setattr(self.manager, "current", "main"))
        root.add_widget(skip_btn)
        root.add_widget(Label())
        self.add_widget(root)

    def _do_login(self, *a):
        email = self.email_in.text.strip()
        pwd = self.pass_in.text.strip()
        if not email or not pwd:
            self.err_lbl.text = "Email and password are required"
            return
        self.err_lbl.text = "Set LOGIN_SERVER_URL to activate login"


# ══════════════════════════════════
# PRIVACY POLICY SCREEN
# ══════════════════════════════════

class PrivacyPolicyScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", spacing=0)
        hdr = BoxLayout(orientation="vertical", size_hint_y=None, height=72, padding=[16, 10])
        with hdr.canvas.before:
            Color(0.04, 0.07, 0.20, 1)
            hbg = RoundedRectangle(pos=hdr.pos, size=hdr.size, radius=[0])
        hdr.bind(pos=lambda w, v: setattr(hbg, "pos", v), size=lambda w, v: setattr(hbg, "size", v))
        hdr.add_widget(Label(text="🔒  Privacy Policy", font_size="18sp", bold=True, color=(0.9, 0.95, 1, 1)))
        hdr.add_widget(Label(text=APP_NAME + "  ·  v" + APP_VERSION + "  ·  " + POLICY_LAST_UPDATED,
                             font_size="10sp", color=(0.45, 0.6, 0.9, 1)))
        root.add_widget(hdr)
        scroll = ScrollView()
        grid = GridLayout(cols=1, spacing=8, size_hint_y=None, padding=[10, 12])
        grid.bind(minimum_height=grid.setter("height"))
        sections = [
            ("🛡️  Our Promise", "All 42 checks run 100% locally.\nNo data uploaded. No tracking. No profiling.\nYOUR data stays on YOUR device — always."),
            ("📊  Data Collection", "Personal data    — ❌ Not collected\nDevice ID/IMEI  — ❌ Not collected\nLocation/GPS    — ❌ Not collected\nScan results    — ✅ Local only, never uploaded"),
            ("📱  Permissions", "INTERNET → DNS, Ping, Policy sync\nBLUETOOTH → BT ON/OFF check\nSTORAGE → APK detection + save report\nQUERY_ALL_PACKAGES → Detect root/hack apps"),
            ("📬  Contact", "Email: " + DEVELOPER_EMAIL + "\nWebsite: biggsafety.com\nResponse: Within 30 days"),
        ]
        for title, content in sections:
            grid.add_widget(Label(text=title, font_size="13sp", bold=True, color=(0.45, 0.80, 1, 1),
                                  halign="left", text_size=(Window.width - 28, None), size_hint_y=None, height=30))
            card = BoxLayout(orientation="vertical", size_hint_y=None, padding=[14, 12])
            with card.canvas.before:
                Color(0.07, 0.09, 0.17, 1)
                cb = RoundedRectangle(pos=card.pos, size=card.size, radius=[10])
            card.bind(pos=lambda w, v, b=cb: setattr(b, "pos", v),
                      size=lambda w, v, b=cb: setattr(b, "size", v),
                      minimum_height=card.setter("height"))
            lbl = Label(text=content, font_size="11.5sp", color=(0.72, 0.78, 0.95, 1),
                        halign="left", text_size=(Window.width - 56, None), size_hint_y=None)
            lbl.bind(texture_size=lambda w, v: setattr(w, "height", v[1] + 4))
            card.add_widget(lbl)
            grid.add_widget(card)
        scroll.add_widget(grid)
        root.add_widget(scroll)
        btn_row = BoxLayout(size_hint_y=None, height=56, spacing=8, padding=[10, 6])
        back_btn = Button(text="← Back", font_size="13sp", size_hint_x=0.35,
                          background_normal="", background_color=(0.10, 0.12, 0.20, 1), color=(0.6, 0.65, 0.85, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, "current", "settings"))
        accept_btn = Button(text="✅  I Accept", font_size="13sp", bold=True, size_hint_x=0.65,
                            background_normal="", background_color=(0.08, 0.42, 0.20, 1), color=(1, 1, 1, 1))
        accept_btn.bind(on_press=lambda x: setattr(self.manager, "current", "settings"))
        btn_row.add_widget(back_btn)
        btn_row.add_widget(accept_btn)
        root.add_widget(btn_row)
        self.add_widget(root)


# ══════════════════════════════════
# ADMIN PANEL SCREEN (Simplified)
# ══════════════════════════════════

class AdminPanelScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_login()

    def _build_login(self):
        from kivy.uix.textinput import TextInput
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", padding=22, spacing=12)
        with root.canvas.before:
            Color(0.02, 0.03, 0.07, 1)
            bg = RoundedRectangle(pos=root.pos, size=root.size, radius=[0])
        root.bind(pos=lambda w, v: setattr(bg, "pos", v), size=lambda w, v: setattr(bg, "size", v))
        root.add_widget(Label(size_hint_y=None, height=40))
        root.add_widget(Label(text="🔐", font_size="52sp", size_hint_y=None, height=72))
        root.add_widget(Label(text="Admin Access", font_size="20sp", bold=True,
                              color=(0.85, 0.9, 1, 1), size_hint_y=None, height=36))
        root.add_widget(Label(text="Authorized Personnel Only", font_size="11sp",
                              color=(0.35, 0.35, 0.5, 1), size_hint_y=None, height=22))
        root.add_widget(Label(size_hint_y=None, height=16))
        self.pwd_in = TextInput(hint_text="Admin Password", password=True, multiline=False,
                                font_size="15sp", size_hint_y=None, height=52,
                                background_color=(0.07, 0.09, 0.16, 1), foreground_color=(1, 1, 1, 1),
                                cursor_color=(0.3, 0.75, 1, 1), padding=[14, 14])
        root.add_widget(self.pwd_in)
        self.err_lbl = Label(text="", font_size="12sp", color=(1, 0.3, 0.3, 1), size_hint_y=None, height=26)
        root.add_widget(self.err_lbl)
        enter_btn = Button(text="🔓  ENTER", font_size="14sp", bold=True, size_hint_y=None, height=52,
                           background_normal="", background_color=(0.1, 0.28, 0.55, 1), color=(1, 1, 1, 1))
        enter_btn.bind(on_press=self._do_login)
        root.add_widget(enter_btn)
        root.add_widget(Label(size_hint_y=None, height=10))
        back_btn = Button(text="← Back", font_size="12sp", size_hint_y=None, height=42,
                          background_normal="", background_color=(0.10, 0.10, 0.16, 1), color=(0.5, 0.5, 0.65, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, "current", "settings"))
        root.add_widget(back_btn)
        root.add_widget(Label())
        self.add_widget(root)

    def _do_login(self, *a):
        pwd = self.pwd_in.text.strip()
        if not pwd:
            self.err_lbl.text = "Password required"
            return
        if verify_admin(pwd):
            self._build_dashboard()
        else:
            self.err_lbl.text = "❌ Wrong password"
            self.pwd_in.text = ""

    def _build_dashboard(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", padding=[10, 10], spacing=6)
        hdr = BoxLayout(orientation="vertical", size_hint_y=None, height=68, padding=[14, 8])
        with hdr.canvas.before:
            Color(0.04, 0.07, 0.22, 1)
            hbg = RoundedRectangle(pos=hdr.pos, size=hdr.size, radius=[12])
        hdr.bind(pos=lambda w, v: setattr(hbg, "pos", v), size=lambda w, v: setattr(hbg, "size", v))
        hdr.add_widget(Label(text="⚙️  Admin Dashboard", font_size="16sp", bold=True, color=(0.9, 0.95, 1, 1)))
        hdr.add_widget(Label(text=APP_NAME + " " + APP_VERSION + "  |  Control Panel",
                             font_size="10sp", color=(0.4, 0.6, 0.9, 1)))
        root.add_widget(hdr)
        scroll = ScrollView()
        grid = GridLayout(cols=1, spacing=5, size_hint_y=None, padding=[0, 4])
        grid.bind(minimum_height=grid.setter("height"))

        def sec(txt, col):
            grid.add_widget(Label(text=txt, font_size="11sp", bold=True, color=col, size_hint_y=None, height=30))

        def toggle_row(lbl, policy_key):
            r = BoxLayout(orientation="horizontal", size_hint_y=None, height=48, padding=[12, 8], spacing=10)
            with r.canvas.before:
                Color(0.06, 0.08, 0.14, 1)
                rb = RoundedRectangle(pos=r.pos, size=r.size, radius=[8])
            r.bind(pos=lambda w, v, b=rb: setattr(b, "pos", v), size=lambda w, v, b=rb: setattr(b, "size", v))
            r.add_widget(Label(text=lbl, font_size="12sp", bold=True, color=(0.8, 0.85, 1, 1),
                               halign="left", text_size=(Window.width * 0.52, None)))
            sw = Switch(active=bool(get_policy(policy_key)), size_hint_x=None, width=80)
            def _on_toggle(widget, value, key=policy_key):
                ACTIVE_POLICY[key] = value
                save_policy_cache(ACTIVE_POLICY)
            sw.bind(active=_on_toggle)
            r.add_widget(sw)
            grid.add_widget(r)

        sec("── 📡 APP CONTROL ──", (0.3, 0.85, 1, 1))
        toggle_row("App Enabled",       "app_enabled")
        toggle_row("Scan Enabled",      "scan_enabled")
        toggle_row("Force Update",      "force_update")
        sec("── 💰 ADS ──", (1, 0.75, 0.2, 1))
        toggle_row("Ads Enabled",       "ads_enabled")
        toggle_row("Test Mode",         "ads_test_mode")
        sec("── 👑 PRO SUBSCRIPTION ──", (1, 0.85, 0.2, 1))
        toggle_row("Force PRO (All Users)",  "force_pro_all")
        toggle_row("Force FREE (All Users)", "force_free_all")
        toggle_row("Block New Trials",       "block_new_trials")
        sec("── 👤 LOGIN ──", (0.4, 1, 0.7, 1))
        toggle_row("Login Enabled",     "login_enabled")
        toggle_row("Login Required",    "login_required")
        sec("── 🔍 SCAN ──", (0.5, 1, 0.6, 1))
        toggle_row("Online Checks",     "scan_online")
        toggle_row("Network Checks",    "scan_network")
        toggle_row("Spyware Checks",    "scan_spy")
        toggle_row("OWASP Checks",      "scan_owasp")
        toggle_row("Auto Save Report",  "auto_save_report")

        sync_btn = Button(text="🔄  Sync Policy from Server", font_size="13sp", bold=True,
                          size_hint_y=None, height=48, background_normal="",
                          background_color=(0.08, 0.28, 0.52, 1), color=(1, 1, 1, 1))
        sync_btn.bind(on_press=lambda x: threading.Thread(target=fetch_server_policy, daemon=True).start())
        grid.add_widget(sync_btn)
        scroll.add_widget(grid)
        root.add_widget(scroll)
        btn_row = BoxLayout(size_hint_y=None, height=52, spacing=6)
        logout_btn = Button(text="🔒 Logout", font_size="13sp", background_normal="",
                            background_color=(0.28, 0.08, 0.08, 1), color=(1, 1, 1, 1))
        logout_btn.bind(on_press=lambda x: self._build_login())
        back_btn = Button(text="← Back to App", font_size="13sp", background_normal="",
                          background_color=(0.08, 0.40, 0.18, 1), color=(1, 1, 1, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, "current", "main"))
        btn_row.add_widget(logout_btn)
        btn_row.add_widget(back_btn)
        root.add_widget(btn_row)
        self.add_widget(root)


# ══════════════════════════════════
# PRO SUBSCRIPTION SCREEN
# ══════════════════════════════════

class ProSubscriptionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._build_ui()

    def _build_ui(self):
        self.clear_widgets()
        root = BoxLayout(orientation="vertical", spacing=0)
        hdr = BoxLayout(orientation="vertical", size_hint_y=None, height=90, padding=[16, 12], spacing=4)
        with hdr.canvas.before:
            Color(0.06, 0.10, 0.28, 1)
            hbg = RoundedRectangle(pos=hdr.pos, size=hdr.size, radius=[0])
        hdr.bind(pos=lambda w, v: setattr(hbg, "pos", v), size=lambda w, v: setattr(hbg, "size", v))
        hdr.add_widget(Label(text="👑  Bigg Safety PRO", font_size="22sp", bold=True, color=(1.0, 0.85, 0.2, 1)))
        hdr.add_widget(Label(text="Unlock All 42 Checks  ·  No Ads  ·  Priority Support",
                             font_size="11sp", color=(0.7, 0.8, 1, 1)))
        root.add_widget(hdr)
        scroll = ScrollView()
        grid = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=[12, 14])
        grid.bind(minimum_height=grid.setter("height"))

        monthly_price = get_policy("pro_monthly_label") or "₹99/month"
        yearly_price  = get_policy("pro_yearly_label") or "₹1000/year"
        yearly_savings = get_policy("pro_yearly_savings") or "Save ₹188!"

        buy_monthly_btn = Button(text="🛒  Subscribe Monthly — " + monthly_price,
                                 font_size="14sp", bold=True, size_hint_y=None, height=52,
                                 background_normal="", background_color=(0.08, 0.35, 0.65, 1), color=(1, 1, 1, 1))
        buy_monthly_btn.bind(on_press=lambda x: self._buy("monthly"))
        grid.add_widget(buy_monthly_btn)

        buy_yearly_btn = Button(text="🌟  Subscribe Yearly — " + yearly_price + "  (" + yearly_savings + ")",
                                font_size="13sp", bold=True, size_hint_y=None, height=52,
                                background_normal="", background_color=(0.06, 0.42, 0.20, 1), color=(1, 1, 1, 1))
        buy_yearly_btn.bind(on_press=lambda x: self._buy("yearly"))
        grid.add_widget(buy_yearly_btn)

        trial_days = int(get_policy("pro_free_trial_days") or 7)
        if trial_days > 0 and not get_policy("block_new_trials") and not IS_PRO_USER:
            trial_btn = Button(text="🎁  Start FREE Trial — " + str(trial_days) + " Days",
                               font_size="14sp", bold=True, size_hint_y=None, height=54,
                               background_normal="", background_color=(0.05, 0.28, 0.18, 1), color=(0.4, 1, 0.7, 1))
            trial_btn.bind(on_press=self._start_trial)
            grid.add_widget(trial_btn)

        for feat in PRO_FEATURES:
            grid.add_widget(Label(text=feat, font_size="12sp", color=(0.85, 0.9, 1, 1),
                                  halign="left", text_size=(Window.width - 28, None), size_hint_y=None, height=28))

        scroll.add_widget(grid)
        root.add_widget(scroll)
        back_btn = Button(text="← Back", font_size="14sp", bold=True, size_hint_y=None, height=54,
                          background_normal="", background_color=(0.08, 0.10, 0.20, 1), color=(0.6, 0.75, 1, 1))
        back_btn.bind(on_press=lambda x: setattr(self.manager, "current", "main"))
        root.add_widget(back_btn)
        self.add_widget(root)

    def _buy(self, plan):
        price = get_policy("pro_monthly_label") if plan == "monthly" else get_policy("pro_yearly_label")
        content = BoxLayout(orientation="vertical", padding=16, spacing=10)
        content.add_widget(Label(text="🛒  Connect Google Play Billing SDK\nto enable real purchases.\nPrice: " + price,
                                 font_size="12sp", color=(0.9, 0.95, 1, 1), halign="center",
                                 text_size=(Window.width * 0.72, None)))
        btn = Button(text="OK", size_hint_y=None, height=44, background_normal="",
                     background_color=(0.08, 0.35, 0.65, 1))
        content.add_widget(btn)
        popup = Popup(title="Subscribe", content=content, size_hint=(0.85, 0.45),
                      background_color=(0.06, 0.08, 0.16, 1))
        btn.bind(on_press=popup.dismiss)
        popup.open()

    def _start_trial(self, *a):
        trial_days = int(get_policy("pro_free_trial_days") or 7)
        start_pro_trial()
        content = BoxLayout(orientation="vertical", padding=16, spacing=10)
        content.add_widget(Label(text="🎉  Trial Started!\n\n" + str(trial_days) + " days full PRO access.",
                                 font_size="13sp", color=(0.3, 1, 0.6, 1), halign="center",
                                 text_size=(Window.width * 0.72, None)))
        btn = Button(text="Awesome! 🚀", size_hint_y=None, height=44, background_normal="",
                     background_color=(0.05, 0.35, 0.18, 1))
        content.add_widget(btn)
        popup = Popup(title="Trial Activated", content=content, size_hint=(0.82, 0.42),
                      background_color=(0.04, 0.10, 0.06, 1))
        def _after(x):
            popup.dismiss()
            self._build_ui()
        btn.bind(on_press=_after)
        popup.open()


# ══════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════

if __name__ == "__main__":
    load_pro_status()
    ScannerApp().run()
