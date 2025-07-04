===============================
           BalatroTool
===============================

===============================
 Quick Start (Bundled Python)
===============================

1. Double-click the Python installer included in this folder:
   > python-3.11.4-amd64.exe

   ✅ IMPORTANT: During installation, make sure to check:
   [✔] Add Python to PATH

2. After Python installs, follow the instructions below for your platform to install required packages and run BalatroTool.


===============================
 Windows Installation
===============================

1. Open Command Prompt (Win+R > type "cmd" > press Enter)

2. Navigate to the folder containing BalatroTool:
   cd path\to\BalatroTool

3. Install required Python packages:
   python -m pip install --upgrade pip
   python -m pip install urllib3 tk requests

4. Run the tool:
   python balatrotool.py


===============================
 Linux Installation (Debian/Ubuntu)
===============================

1. Open Terminal.

2. Install Python and pip:
   sudo apt update
   sudo apt install -y python3 python3-pip python3-tk

3. Navigate to the BalatroTool folder:
   cd /path/to/BalatroTool

4. Install required packages:
   python3 -m pip install --upgrade pip
   python3 -m pip install urllib3 requests

5. Run the tool:
   python3 balatrotool.py


===============================
 Linux Installation (Arch/SteamOS)
===============================

This section applies to:
- Arch Linux
- SteamOS (Steam Deck)
- Bazzite
- HoloISO
- ChimeraOS
- Nobara
- Other Arch-based gaming distros and handhelds

1. Open Terminal (Desktop Mode or Konsole)

2. Install Python and pip:
   sudo pacman -Sy python python-pip tk

3. Navigate to the BalatroTool folder:
   cd /path/to/BalatroTool

4. Install required Python packages:
   python -m pip install --upgrade pip
   python -m pip install urllib3 requests

5. Run the tool:
   python balatrotool.py

6. (Optional) On Steam Deck:
   - Switch to Desktop Mode
   - Right-click in the folder > "Open Terminal"
   - Run commands above
   - Create a `.desktop` shortcut to launch BalatroTool from Gaming Mode


===============================
 Mod Loader System (New!)
===============================

🔁 Manage your mod setups with save/load slots:
- 📦 Save your current EXE and mods as a slot (`ZIP`)
- ↩️ Load saved mod slots into your game setup
- ❌ Delete slots with confirmation
- 📝 Rename slots anytime
- 🟢 Green dot = currently loaded slot
- ⓘ Info button shows:
   - Mod count (excludes `.exe`)
   - Tags & descriptions
   - Creation date
   - `@` Lock button (makes the slot read-only when shared)
   - `<` Back button

🧩 Mod slots saved to:  
> BalatroTool/mod_slots/

🧷 Bonus:
- 📤 Export & 📥 Import slot metadata via `.json`
- 🖱️ Reorder slots by dragging
- 🪄 Progress bar and toast popup when saving, loading, importing, etc.


===============================
 Loader Update Tools
===============================

📥 Update your mod loader:
- Update **Lovely**, **Steammodded**, or both
- Auto-detects version.dll
- Option to launch the game for Lovely to install
- ⚙️ Enable auto-update on startup from Settings


===============================
 Core Tool Features
===============================

🛠️ BalatroTool lets you:
- Copy mods + EXE from your install into a zip
- Share it with a friend who legally owns the game
- Auto-detect your AppData and game folders
- Install Lovely/SteamModded automatically
- Work across Windows, Linux, Steam Deck, and VMs
- Clean UI with settings and status bar


===============================
 Troubleshooting Tips
===============================

- If 'python' doesn’t work, try 'python3'
- If tkinter fails to load, install `tk` or `python3-tk` from your OS’s package manager
- Test tkinter with:
     python -m tkinter
- If pip isn't found, reinstall Python and make sure to check “Add Python to PATH”


===============================
 About BalatroTool
===============================

BalatroTool is a utility made by a solo developer (moonplaysvr) for the Balatro modding community.

🎬 YouTube: https://www.youtube.com/@moonplaysvr

❓ What is this for?
- Makes modding easier
- Lets you zip + share your mods and EXE (minus saves and DRM)
- Installs mod loaders for you
- Supports Linux + Steam Deck users too

🧨 Isn't this piracy?
No — BalatroTool does **not** bypass DRM or give you the game.  
Your friend still needs a legal copy to play.  
If the devs (LocalThunk/Playstack) ask us to take this down, we’ll work with them to comply.

📛 Note:
> This is NOT a piracy tool. You still need a valid license to play the game.  
> Please support the devs if you enjoy the game!
