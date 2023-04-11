import os
import shutil
from huggingface_hub import snapshot_download

def delete_directory_contents(dir_path):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

repo_id = "MrVolts/Nomads"
repo_type = "dataset"  # Since this is a dataset repository
current_directory = os.getcwd()

local_path = snapshot_download(repo_id=repo_id, repo_type=repo_type, cache_dir=current_directory)

# Find the latest snapshot
snapshots_dir = os.path.join(local_path, "snapshots")
latest_snapshot = max(os.listdir(snapshots_dir), key=lambda x: os.path.getmtime(os.path.join(snapshots_dir, x)))
latest_snapshot_path = os.path.join(snapshots_dir, latest_snapshot)

# Copy the contents of the latest snapshot to the current directory
for filename in os.listdir(latest_snapshot_path):
    file_path = os.path.join(latest_snapshot_path, filename)
    if os.path.isfile(file_path):
        shutil.copy(file_path, current_directory)

print(f"The contents of the 'snapshots' folder have been copied to: {current_directory}")

# Delete other downloaded files and directories
delete_directory_contents(local_path)

# Delete the parent directory
shutil.rmtree(local_path)