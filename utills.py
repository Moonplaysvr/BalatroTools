import os
import shutil
import sys

def safe_filename(name):
    # Remove characters invalid in filenames, keep alphanumerics and _-.
    return "".join(c for c in name if c.isalnum() or c in (" ", "_", "-")).rstrip().replace(" ", "_")

def find_balatro_appdata():
    # Find the Balatro appdata folder based on platform
    if sys.platform.startswith("win"):
        appdata = os.getenv('APPDATA')
        if not appdata:
            return None
        balatro_path = os.path.join(appdata, "Balatro")
        if os.path.exists(balatro_path):
            return balatro_path
    else:
        # For Linux, Mac etc, try home config folders - adjust as needed
        home = os.path.expanduser("~")
        candidates = [
            os.path.join(home, ".config", "Balatro"),
            os.path.join(home, ".balatro"),
            os.path.join(home, "Balatro"),
        ]
        for p in candidates:
            if os.path.exists(p):
                return p
    return None

def copy_mods_and_exe(src, dst):
    """
    Copies all files and folders from src to dst.
    Overwrites existing files.
    Returns True on success, False on failure.
    """
    try:
        if not os.path.exists(dst):
            os.makedirs(dst)

        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d)
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)
        return True
    except Exception as e:
        print(f"Error copying mods: {e}")
        return False
