import os
import shutil
from tqdm import tqdm

with open("image_copier_script.sh", "r") as f:
    lines = f.readlines()

for line in tqdm(lines):
    _, src, dest = line[:-1].split(" ")
    shutil.copy2(src, dest)
