#Download Ordner sortieren 2.0

import os
import shutil
from datetime import datetime, timedelta

# Pfad zum Download-Ordner für Windows
download_path = os.path.expanduser("~\\Downloads")

# Heutiges Datum und das Datum von vor 2 Tagen ermitteln
today = datetime.now()
two_days_ago = today - timedelta(days=2)

# Neuen Archivordner-Namen erstellen
archive_folder_name = "Archiv_" + today.strftime('%Y-%m-%d')
archive_path = os.path.join(download_path, archive_folder_name)

# Wenn der Archivordner noch nicht existiert, erstellen
if not os.path.exists(archive_path):
    os.makedirs(archive_path)

# Durch alle Dateien im Download-Ordner gehen
for file_name in os.listdir(download_path):
    file_path = os.path.join(download_path, file_name)
    
    # Prüfen, ob es sich um eine Datei handelt und ob sie älter als 2 Tage ist
    if os.path.isfile(file_path):
        file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
        if file_mtime < two_days_ago:
            # Datei in den Archivordner verschieben
            shutil.move(file_path, archive_path)

print(f"Dateien, die älter als 2 Tage sind, wurden in den Ordner '{archive_folder_name}' verschoben.")
