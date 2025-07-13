import os
import shutil
import datetime

def backup_files(source_dirs=["logs", "workflows"], backup_dir="backups"):
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    os.makedirs(backup_dir, exist_ok=True)
    for src in source_dirs:
        dest = os.path.join(backup_dir, f"{src}_{date_str}")
        shutil.copytree(src, dest)
    print(f"✅ Backup effectué dans {backup_dir}")

if __name__ == "__main__":
    backup_files()
