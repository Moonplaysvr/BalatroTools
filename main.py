import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import json
import webbrowser
import shutil
from datetime import datetime
import subprocess
import zipfile

CONFIG_PATH = "balatrotool_config.json"

dark_colors = {
    "bg": "#2e2e2e",
    "fg": "#dcdcdc",
    "entry_bg": "#3e3e3e",
    "button_bg": "#444444",
    "highlight": "#57a0ff"
}
light_colors = {
    "bg": "#f0f0f0",
    "fg": "#000000",
    "entry_bg": "#ffffff",
    "button_bg": "#e0e0e0",
    "highlight": "#1a73e8"
}

ABOUT_YT_URL = "https://www.youtube.com/@moonplaysvr"

class ModSlot:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.locked = False
        self.tags = []
        self.description = ""
        self.creation_date = None
        self.mod_count = 0
        self.loaded = False

    def save_metadata(self):
        meta_path = os.path.join(self.path, "metadata.json")
        meta = {
            "name": self.name,
            "locked": self.locked,
            "tags": self.tags,
            "description": self.description,
            "creation_date": self.creation_date,
            "mod_count": self.mod_count
        }
        with open(meta_path, "w") as f:
            json.dump(meta, f, indent=2)

    def load_metadata(self):
        meta_path = os.path.join(self.path, "metadata.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r") as f:
                meta = json.load(f)
                self.name = meta.get("name", self.name)
                self.locked = meta.get("locked", False)
                self.tags = meta.get("tags", [])
                self.description = meta.get("description", "")
                self.creation_date = meta.get("creation_date", None)
                self.mod_count = meta.get("mod_count", 0)

    def count_mod_files(self):
        count = 0
        for root, _, files in os.walk(self.path):
            for f in files:
                if not f.lower().endswith('.exe'):
                    count += 1
        self.mod_count = count
        self.save_metadata()

class BalatroToolApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("BalatroTool")
        self.geometry("750x520")
        self.minsize(700, 480)
        if os.path.exists("icon.ico"):
            self.iconbitmap("icon.ico")

        self.dark_mode = True
        self.load_config()

        self.style = ttk.Style()
        self.style.theme_use('default')

        self.create_widgets()
        self.apply_theme()

    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r") as f:
                    cfg = json.load(f)
                    self.dark_mode = cfg.get("dark_mode", True)
            except:
                self.dark_mode = True
        else:
            self.dark_mode = True

    def save_config(self):
        cfg = {"dark_mode": self.dark_mode}
        with open(CONFIG_PATH, "w") as f:
            json.dump(cfg, f, indent=2)

    def apply_theme(self):
        colors = dark_colors if self.dark_mode else light_colors

        self.configure(bg=colors["bg"])

        self.style.configure("TFrame", background=colors["bg"])
        self.style.configure("TLabel", background=colors["bg"], foreground=colors["fg"])
        self.style.configure("TButton",
                             background=colors["button_bg"],
                             foreground=colors["fg"],
                             borderwidth=0)
        self.style.map("TButton",
                       background=[('active', colors["highlight"])],
                       foreground=[('active', colors["fg"])])

        self.style.configure("TEntry",
                             fieldbackground=colors["entry_bg"],
                             foreground=colors["fg"])

        # Status bar config
        self.status_bar.configure(background=colors["bg"], foreground=colors["fg"])

        # Update all widgets recursively
        self.update_widgets_colors(self, colors)

    def update_widgets_colors(self, widget, colors):
        for child in widget.winfo_children():
            try:
                cls_name = child.winfo_class()
                if cls_name == "Label":
                    child.configure(bg=colors["bg"], fg=colors["fg"])
                elif cls_name == "Button":
                    child.configure(bg=colors["button_bg"], fg=colors["fg"], activebackground=colors["highlight"])
                elif cls_name == "Entry":
                    child.configure(bg=colors["entry_bg"], fg=colors["fg"])
                elif cls_name == "Text":
                    child.configure(bg=colors["entry_bg"], fg=colors["fg"], insertbackground=colors["fg"])
                elif cls_name == "Frame" or cls_name == "TFrame":
                    child.configure(bg=colors["bg"])
                self.update_widgets_colors(child, colors)
            except:
                pass

    def create_widgets(self):
        # Main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons frame (top)
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        # Load button
        self.load_btn = ttk.Button(btn_frame, text="<--- Load Slot", command=self.load_mod_slot)
        self.load_btn.pack(side=tk.LEFT, padx=3)

        # Save button
        self.save_btn = ttk.Button(btn_frame, text="[__] Save Slot", command=self.save_mod_slot)
        self.save_btn.pack(side=tk.LEFT, padx=3)

        # Delete button
        self.del_btn = ttk.Button(btn_frame, text="X Delete Slot", command=self.delete_mod_slot)
        self.del_btn.pack(side=tk.LEFT, padx=3)

        # Import Zip button
        self.import_btn = ttk.Button(btn_frame, text="⬆ Import ZIP", command=self.import_zip_slot)
        self.import_btn.pack(side=tk.LEFT, padx=3)

        # Export Zip button
        self.export_btn = ttk.Button(btn_frame, text="⬇ Export ZIP", command=self.export_zip_slot)
        self.export_btn.pack(side=tk.LEFT, padx=3)

        # Update loader button
        self.update_loader_btn = ttk.Button(btn_frame, text="Update Loader", command=self.update_loader)
        self.update_loader_btn.pack(side=tk.RIGHT, padx=3)

        # Settings button
        self.settings_btn = ttk.Button(btn_frame, text="Settings ⚙", command=self.open_settings)
        self.settings_btn.pack(side=tk.RIGHT, padx=3)

        # Launch Game button
        self.launch_btn = ttk.Button(btn_frame, text="Launch Game ▶", command=self.launch_game)
        self.launch_btn.pack(side=tk.RIGHT, padx=3)

        # Mod Slots Listbox + scrollbar
        list_frame = ttk.Frame(self.main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.mod_slots_var = tk.StringVar(value=[])
        self.mod_slots_listbox = tk.Listbox(list_frame, listvariable=self.mod_slots_var, height=15)
        self.mod_slots_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.mod_slots_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.mod_slots_listbox.configure(yscrollcommand=scrollbar.set)

        self.mod_slots_listbox.bind('<<ListboxSelect>>', self.on_slot_select)

        # Info Button
        self.info_btn = ttk.Button(self.main_frame, text="Info ℹ", command=self.show_slot_info)
        self.info_btn.pack(pady=5)

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        self.status_bar = tk.Label(self, textvariable=self.status_var, anchor="w", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Bottom left About Button
        about_btn = ttk.Button(self, text="About moonplaysvr", command=self.show_about)
        about_btn.place(x=5, y=self.winfo_height()-30)
        self.after(100, lambda: about_btn.place(x=5, y=self.winfo_height()-30))  # reposition after window draws

        # Load mod slots folder
        self.mod_slots_folder = os.path.join(os.getcwd(), "mod_slots")
        if not os.path.exists(self.mod_slots_folder):
            os.makedirs(self.mod_slots_folder)

        self.mod_slots = []
        self.load_mod_slots()

    def toast(self, message):
        # Simple toast message that disappears
        toast = tk.Toplevel(self)
        toast.overrideredirect(True)
        toast.configure(bg="#222")
        label = tk.Label(toast, text=message, fg="white", bg="#222", padx=10, pady=5)
        label.pack()
        x = self.winfo_x() + self.winfo_width()//2 - toast.winfo_reqwidth()//2
        y = self.winfo_y() + self.winfo_height()//2 - toast.winfo_reqheight()//2
        toast.geometry(f"+{x}+{y}")
        toast.after(1500, toast.destroy)

    def load_mod_slots(self):
        self.mod_slots = []
        for fname in os.listdir(self.mod_slots_folder):
            path = os.path.join(self.mod_slots_folder, fname)
            if os.path.isdir(path):
                slot = ModSlot(fname, path)
                slot.load_metadata()
                slot.count_mod_files()
                self.mod_slots.append(slot)
        self.refresh_mod_slots_listbox()

    def refresh_mod_slots_listbox(self):
        display_names = []
        for slot in self.mod_slots:
            prefix = "● " if getattr(slot, "loaded", False) else "  "
            display_names.append(f"{prefix}{slot.name}")
        self.mod_slots_var.set(display_names)

    def on_slot_select(self, event):
        # Could update UI based on selection if needed
        pass

    def load_mod_slot(self):
        idx = self.mod_slots_listbox.curselection()
        if not idx:
            messagebox.showwarning("Load Slot", "No mod slot selected.")
            return
        slot = self.mod_slots[idx[0]]
        # Here: implement the actual loading logic (copy files, unzip, etc)
        # For now just mark loaded
        for s in self.mod_slots:
            s.loaded = False
        slot.loaded = True
        self.refresh_mod_slots_listbox()
        self.status_var.set(f"Loaded slot '{slot.name}'")
        self.toast(f"Loaded slot '{slot.name}'")

    def save_mod_slot(self):
        # Prompt for name
        name = simpledialog.askstring("Save Slot", "Enter name for this slot:")
        if not name:
            return
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).rstrip()
        slot_path = os.path.join(self.mod_slots_folder, safe_name)
        if os.path.exists(slot_path):
            if not messagebox.askyesno("Overwrite Slot", f"Slot '{safe_name}' exists. Overwrite?"):
                return
            shutil.rmtree(slot_path)
        os.makedirs(slot_path)
        # TODO: Copy current mod files to slot_path - user logic needed
        # For demo, just create metadata file
        slot = ModSlot(safe_name, slot_path)
        slot.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        slot.mod_count = 0
        slot.save_metadata()
        self.mod_slots.append(slot)
        self.refresh_mod_slots_listbox()
        self.status_var.set(f"Saved slot '{safe_name}'")
        self.toast(f"Saved slot '{safe_name}'")

    def delete_mod_slot(self):
        idx = self.mod_slots_listbox.curselection()
        if not idx:
            messagebox.showwarning("Delete Slot", "No mod slot selected.")
            return
        slot = self.mod_slots[idx[0]]
        if slot.locked:
            messagebox.showinfo("Delete Slot", "Cannot delete a locked slot.")
            return
        if not messagebox.askyesno("Delete Slot", f"Are you sure you want to delete slot '{slot.name}'?"):
            return
        shutil.rmtree(slot.path)
        self.mod_slots.pop(idx[0])
        self.refresh_mod_slots_listbox()
        self.status_var.set(f"Deleted slot '{slot.name}'")
        self.toast(f"Deleted slot '{slot.name}'")

    def show_slot_info(self):
        idx = self.mod_slots_listbox.curselection()
        if not idx:
            messagebox.showwarning("Slot Info", "No mod slot selected.")
            return
        slot = self.mod_slots[idx[0]]

        info_win = tk.Toplevel(self)
        info_win.title(f"Info - {slot.name}")
        info_win.geometry("400x350")

        ttk.Label(info_win, text=f"Slot Name: {slot.name}", font=("Segoe UI", 14, "bold")).pack(pady=5)
        locked_str = "Yes" if slot.locked else "No"
        ttk.Label(info_win, text=f"Locked: {locked_str}").pack()
        ttk.Label(info_win, text=f"Creation Date: {slot.creation_date or 'Unknown'}").pack()
        ttk.Label(info_win, text=f"Number of mods (excluding .exe): {slot.mod_count}").pack()

        # Tags
        ttk.Label(info_win, text="Tags (comma separated):").pack(pady=(10,0))
        tags_var = tk.StringVar(value=",".join(slot.tags))
        tags_entry = ttk.Entry(info_win, textvariable=tags_var)
        tags_entry.pack(fill=tk.X, padx=10)

        # Description
        ttk.Label(info_win, text="Description:").pack(pady=(10,0))
        desc_text = tk.Text(info_win, height=6, wrap=tk.WORD)
        desc_text.pack(fill=tk.BOTH, padx=10, pady=5)
        desc_text.insert("1.0", slot.description)

        def save_info():
            if slot.locked:
                messagebox.showinfo("Locked Slot", "This slot is locked and cannot be edited.")
                return
            slot.tags = [t.strip() for t in tags_var.get().split(",") if t.strip()]
            slot.description = desc_text.get("1.0", "end").strip()
            slot.save_metadata()
            self.load_mod_slots()
            self.toast(f"Saved info for '{slot.name}'")
            info_win.destroy()

        ttk.Button(info_win, text="Save", command=save_info).pack(pady=10)
        ttk.Button(info_win, text="< Back", command=info_win.destroy).pack(side=tk.BOTTOM, pady=5)

    def update_loader(self):
        messagebox.showinfo("Update Loader", "This feature will update Lovely and Steammodded automatically.\n(Implementation needed)")
        self.status_var.set("Updating loader... (stub)")

    def open_settings(self):
        settings_win = tk.Toplevel(self)
        settings_win.title("Settings")
        settings_win.geometry("300x150")

        ttk.Label(settings_win, text="Settings", font=("Segoe UI", 14, "bold")).pack(pady=10)

        # Dummy auto-update toggle
        auto_update_var = tk.BooleanVar(value=False)
        def toggle_auto_update():
            val = auto_update_var.get()
            self.status_var.set(f"Auto-update on startup set to {val}")
            self.toast(f"Auto-update set to {val}")
        ttk.Checkbutton(settings_win, text="Auto-update loader on startup", variable=auto_update_var, command=toggle_auto_update).pack(pady=10)

        # Light mode toggle (checkbox checked = use light mode)
        light_mode_var = tk.BooleanVar(value=not self.dark_mode)
        def toggle_light_mode():
            self.dark_mode = not light_mode_var.get()
            self.apply_theme()
            self.save_config()
            self.toast(f"{'Light' if not self.dark_mode else 'Dark'} mode enabled")
        ttk.Checkbutton(settings_win, text="Use Light Mode", variable=light_mode_var, command=toggle_light_mode).pack(pady=10)

        ttk.Button(settings_win, text="Close", command=settings_win.destroy).pack(pady=10)

    def show_about(self):
        about_win = tk.Toplevel(self)
        about_win.title("About BalatroTool")
        about_win.geometry("450x400")

        text = (
            "About BalatroTool\n\n"
            "This is a Community made tool that is opensource if you wanna contribute "
            "and made to make it easier to mod the game and Give people your mods and .exe if you have modified the .exe and stuff like that.\n\n"
            "Who made this?\n"
            "A solo developer that makes Random stuff that I think is cool aka moonplaysvr\n\n"
            "Isn't this piracy?\n"
            "No, It's not. You still need a DRM, a License to the game, and The other game files to even play the game. "
            "If the developer's of Balatro (LocalThunk/Playstack) wanna take it down. I'll change it and see if they think it's okay "
            "to put back up by negotiating.\n\n"
            "Why the hell is this even Good?\n"
            "It updates your Lovely and Smodded for you. Even though modding Balatro is literally the easiest thing ever, Unless you're on Linux like me, "
            "But I used Windows because I use arch btw and It was pissing me off just trying to mod the game.\n\n"
            "Note: I'm not trying to promote piracy. PIRACY IS ILLEGAL!\n"
            "\n"
            "----\n"
            "This tool lets you import and export ZIPs with your modded Balatro.exe and appdata for easy sharing with friends.\n"
            "It does NOT include full game files, only your modded executable and data.\n"
            "ONLY SHARE IF YOU OWN THE GAME!"
        )

        label = tk.Label(about_win, text=text, wraplength=420, justify="left")
        label.pack(padx=10, pady=10)

        yt_btn = ttk.Button(about_win, text="moonplaysvr YouTube Channel", command=lambda: webbrowser.open(ABOUT_YT_URL))
        yt_btn.pack(pady=5)

        ttk.Button(about_win, text="Close", command=about_win.destroy).pack(pady=10)

    def launch_game(self):
        import platform
        exe_path = None

        # Try to load last saved exe path
        config_file = "balatrotool_config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, "r") as f:
                    cfg = json.load(f)
                    exe_path = cfg.get("balatro_exe_path", None)
            except:
                exe_path = None

        if not exe_path or not os.path.exists(exe_path):
            messagebox.showinfo("Select Executable", "Please select your Balatro.exe file.")
            exe_path = filedialog.askopenfilename(
                title="Select Balatro.exe",
                filetypes=[("Executable files", "*.exe")]
            )
            if not exe_path:
                self.status_var.set("Game launch cancelled.")
                return
            # Save for next time
            try:
                with open(config_file, "r") as f:
                    cfg = json.load(f)
            except:
                cfg = {}
            cfg["balatro_exe_path"] = exe_path
            with open(config_file, "w") as f:
                json.dump(cfg, f, indent=2)

        try:
            subprocess.Popen([exe_path])
            self.status_var.set(f"Launched game: {os.path.basename(exe_path)}")
            self.toast(f"Launched game: {os.path.basename(exe_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch game.\n{e}")
            self.status_var.set("Failed to launch game.")

    def import_zip_slot(self):
        zip_path = filedialog.askopenfilename(
            title="Select ZIP file to import",
            filetypes=[("ZIP archives", "*.zip")]
        )
        if not zip_path:
            return
        # Ask for slot name
        name = simpledialog.askstring("Import ZIP", "Enter name for this imported slot:")
        if not name:
            return
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '_', '-')).rstrip()
        slot_path = os.path.join(self.mod_slots_folder, safe_name)
        if os.path.exists(slot_path):
            if not messagebox.askyesno("Overwrite Slot", f"Slot '{safe_name}' exists. Overwrite?"):
                return
            shutil.rmtree(slot_path)
        os.makedirs(slot_path)

        # Extract ZIP
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(slot_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract ZIP.\n{e}")
            shutil.rmtree(slot_path)
            return

        # Save metadata
        slot = ModSlot(safe_name, slot_path)
        slot.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        slot.count_mod_files()
        slot.save_metadata()
        self.mod_slots.append(slot)
        self.refresh_mod_slots_listbox()
        self.status_var.set(f"Imported ZIP as slot '{safe_name}'")
        self.toast(f"Imported ZIP as slot '{safe_name}'")

    def export_zip_slot(self):
        idx = self.mod_slots_listbox.curselection()
        if not idx:
            messagebox.showwarning("Export ZIP", "No mod slot selected.")
            return
        slot = self.mod_slots[idx[0]]

        # Ask where to save
        export_path = filedialog.asksaveasfilename(
            title="Export slot as ZIP",
            defaultextension=".zip",
            filetypes=[("ZIP archives", "*.zip")],
            initialfile=f"{slot.name}.zip"
        )
        if not export_path:
            return

        try:
            with zipfile.ZipFile(export_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Walk slot folder recursively
                for root, dirs, files in os.walk(slot.path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Include everything inside the slot folder (exe + mod files)
                        arcname = os.path.relpath(file_path, slot.path)
                        zipf.write(file_path, arcname)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export ZIP.\n{e}")
            return
        self.status_var.set(f"Exported slot '{slot.name}' as ZIP")
        self.toast(f"Exported slot '{slot.name}' as ZIP")

if __name__ == "__main__":
    app = BalatroToolApp()
    app.mainloop()
