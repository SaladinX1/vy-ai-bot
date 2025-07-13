import shutil, datetime

def backup_logs():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy("logs/system.log", f"backups/system_{timestamp}.log")


def backup():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    shutil.copy("logs/system.log", f"backup/log_{timestamp}.log")

# schedule.every().day.at("23:00").do(backup)