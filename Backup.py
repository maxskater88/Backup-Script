import os
import zipfile
import time
from pathlib import Path

# ===== Configuration =====
SOURCE_DRIVE = Path(r"D:\Temp\test in")
DEST_DRIVE = Path(r"D:\Temp\test out")
BATCH_SIZE = 10             # Not really necessary
PAUSE_BETWEEN_BATCHES = 5   # seconds to wait
COMPRESSION = zipfile.ZIP_DEFLATED
# ==========================

def get_existing_folder(DEST_DRIVE):
    pass

def compress_folder(source_folder: Path, destination_folder: Path):
    """Compress a single folder into a zip file."""
    zip_name = destination_folder / f"{source_folder.name}.zip"
    print(f"Compressing {source_folder} -> {zip_name}")
    with zipfile.ZipFile(zip_name, "w", compression=COMPRESSION, compresslevel=9) as zipf:
        for root, _, files in os.walk(source_folder):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(source_folder.parent)
                zipf.write(file_path, arcname)
    print(f"✅ Completed: {zip_name}")

def get_folders(source_drive: Path):
    """Return all top-level folders from the source drive."""
    directory, name = list(), list()
    for entry in os.scandir(source_drive):
        if entry.is_dir():
            directory.append(entry)
            name.append(entry.name)  
    return directory, name

def get_zipped(source_drive: Path):
    """Return all zipped files in destination"""
    return [item.name[:-4] for item in os.scandir(source_drive) if item.name.endswith('.zip')]

def remove_zipped(DEST_DRIVE: Path, folders: list, names: list):
    check = list()
    exists = get_zipped(DEST_DRIVE)
    for i in range(len(names)):
        if names[i] in exists:
            check.append(i)
    return [folder for index, folder in enumerate(folders) if index not in check]
            
def ensure_dest(dest_drive: Path):
    """Create the destination folder if it doesn't exist."""
    if not dest_drive.exists():
        dest_drive.mkdir(parents=True, exist_ok=True)

def main():
    start_time = time.time()
    ensure_dest(DEST_DRIVE)
    
    all_folders, names = get_folders(SOURCE_DRIVE)
    folders = remove_zipped(DEST_DRIVE, all_folders, names)
    
    print(f"Found {len(folders)} folder(s) in {SOURCE_DRIVE}")
    print(f"Batches to run: {len(folders)//BATCH_SIZE+1}")

    # Process in batches
    for i in range(0, len(folders), BATCH_SIZE):
        batch = folders[i:i + BATCH_SIZE]
        print(f"\n=== Starting batch {i//BATCH_SIZE + 1} ({len(batch)} folders) ===")

        for entry in batch:
            src_folder = Path(entry.path)
            compress_folder(src_folder, DEST_DRIVE)

        print(f"=== Batch {i//BATCH_SIZE + 1} complete ===")

        if PAUSE_BETWEEN_BATCHES > 0 and i + BATCH_SIZE < len(folders):
            print(f"...Waiting {PAUSE_BETWEEN_BATCHES} seconds before next batch...")
            time.sleep(PAUSE_BETWEEN_BATCHES)

    end_time = time.time()
    print(f"\n🎉 Finished! Completed in approx {(end_time-start_time//60)} minutes")

if __name__ == "__main__":
    main()