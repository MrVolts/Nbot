import os
import shutil
from huggingface_hub import snapshot_download

repo_id = "MrVolts/Nomads"
repo_type = "dataset"  # Since this is a dataset repository
current_directory = os.getcwd()

local_path = snapshot_download(repo_id=repo_id, repo_type=repo_type, cache_dir=current_directory)
print(f"The repository has been downloaded to: {local_path}")

# Define the source and destination directories
source_dir = local_path
destination_dir = current_directory

# Copy the contents of the source directory to the destination directory
for item in os.listdir(source_dir):
    if item == ".gitattributes":
        continue  # Skip copying the .gitattributes file
    s = os.path.join(source_dir, item)
    d = os.path.join(destination_dir, item)
    
    if os.path.isdir(s):
        shutil.copytree(s, d, dirs_exist_ok=True)
    else:
        shutil.copy2(s, d)

# Remove the original directory
shutil.rmtree(os.path.join(current_directory, "datasets--MrVolts--Nomads"))
