import os
from huggingface_hub import snapshot_download

repo_id = "MrVolts/Nomads"
repo_type = "dataset"  # Since this is a dataset repository
current_directory = os.getcwd()

local_path = snapshot_download(repo_id=repo_id, repo_type=repo_type, cache_dir=current_directory)
print(f"The repository has been downloaded to: {local_path}")