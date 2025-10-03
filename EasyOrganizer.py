"""
EasyOrganizer - Windows
Author: Withness

Description:
- Automatically organizes the Downloads folder.
- Compatible only with Windows.
- Categories detect all common file extensions.
- Console with clear messages.
- Creates subfolders only if files of the corresponding type exist.
- Logs moved files inside Logs_Organizer.
"""

import os
import shutil
from pathlib import Path
import platform
from datetime import datetime

# --- File types ---
TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff", ".ico"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".xlsx", ".xls", ".ppt", ".pptx", ".odt", ".csv"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a"],
    "Installers": [".exe", ".msi", ".cmd", ".vbs", ".appx", ".msix"],
    "Compressed": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "ISOs": [".iso", ".img", ".bin", ".cue"],
    "Shortcuts": [".lnk"],
    "Code": [".py", ".js", ".html", ".css", ".php", ".sh", ".ps1", ".bat", ".reg"]
}

def detect_downloads():
    """Automatically detects the Downloads folder in Windows"""
    home = Path.home()
    possible = [home / "Downloads", home / "Descargas"]
    for p in possible:
        if p.exists() and p.is_dir():
            return p
    return None

def organize(folder):
    moved = 0

    # Create logs folder inside Downloads
    logs_dir = folder / "Logs_Organizer"
    logs_dir.mkdir(exist_ok=True)

    # Log with date and time
    log_path = logs_dir / f"log_organizer_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    log_created = False

    print("\n🔍 Starting to organize files...\n")

    created_folders = {}

    for item in folder.iterdir():
        if not item.is_file():
            continue
        name = item.name
        ext = item.suffix.lower()
        dest_name = None

        for folder_name, extensions in TYPES.items():
            if ext in extensions:
                dest_name = folder_name
                break

        if not dest_name:
            dest_name = "Others"

        dest_folder = folder / dest_name
        if dest_name not in created_folders and not dest_folder.exists():
            dest_folder.mkdir(parents=True, exist_ok=True)
            created_folders[dest_name] = True

        dest_path = dest_folder / name
        counter = 1
        base_stem = item.stem
        while dest_path.exists():
            dest_path = dest_folder / f"{base_stem} ({counter}){item.suffix}"
            counter += 1

        try:
            shutil.move(str(item), str(dest_path))
            print(f"[OK] {name} → {dest_name}\\")

            # Create log only if the first file is moved
            if not log_created:
                with open(log_path, "a", encoding="utf-8") as log:
                    log.write(f"=== Organization log: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
                log_created = True

            if log_created:
                with open(log_path, "a", encoding="utf-8") as log:
                    log.write(f"{name} → {dest_name}\n")
            
            moved += 1
        except Exception as e:
            print(f"[ERROR] Could not move {name}: {e}")

    return moved

def main():
    # Professional header in console
    print("""
========================================
      EasyOrganizer
      Author: Withness
========================================

Description:

EasyOrganizer automatically organizes your Downloads folder

Features:
- Compatible exclusively with Windows.
- Console interface with clear and easy-to-understand messages.
- Fast and automatic organization.
- Subfolders are created only when necessary.

""")

    if platform.system() != "Windows":
        print("This script only works on Windows.")
        return

    print("="*50)
    print("EasyOrganizer - Windows")
    print("="*50)

    downloads_folder = detect_downloads()
    if downloads_folder:
        print(f"\nUsing Downloads folder: {downloads_folder}")
    else:
        downloads_folder = Path(input("\nDownloads folder not found. Enter the path manually:\n> "))
        while not downloads_folder.exists() or not downloads_folder.is_dir():
            downloads_folder = Path(input("Invalid path. Try again:\n> "))

    moved = organize(downloads_folder)

    print("\n" + "-"*50)
    if moved > 0:
        print(f"Organization completed. {moved} files moved.")
    else:
        print("No files found to organize.")
    print("-"*50)
    print("Your Downloads folder is now organized!")
    print("Thanks for using EasyOrganizer <3")
    print("If you found it useful and want to support my projects, you can do so here: https://ko-fi.com/withness")


if __name__ == "__main__":
    main()
    input("\nPress Enter to close the console...")
