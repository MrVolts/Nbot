import os
from datasets import load_dataset

os.environ['HF_API_KEY'] = os.getenv('HF_API_KEY')

dataset = load_dataset(
    'https://huggingface.co/datasets/MrVolts/Nomads',
    name='user1', # Change this to the desired user's folder name
    split='train',
    streaming=True
)