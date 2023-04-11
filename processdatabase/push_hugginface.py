from huggingface_hub import HfApi
api = HfApi()

api.upload_folder(
    folder_path="/home/ubuntu/NomadsAI/processdatabase",
    repo_id="MrVolts/Nomads",
    repo_type="dataset",
    ignore_patterns=["*.py", ".*"],
    delete_patterns=["*.py", ".*"]
)