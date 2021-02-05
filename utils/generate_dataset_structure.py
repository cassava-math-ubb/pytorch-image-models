import os
import shutil
import pandas as pd
import random
from pathlib import Path
from glob import glob


dataset_path = Path.cwd() / "../datasets/cassava-dataset"
train_folder = "train_images"
train_csv = "train.csv"


def update_dataset_structure(output_path, mode='all'):
    train_data = pd.read_csv(str(dataset_path / train_csv))

    if mode == 'all':
        output_folder_names = ['0', '1', '2', '3', '4']
    elif mode == '3-vs-all':
        output_folder_names = ['0', '1']
    else:
        output_folder_names = ['0', '1', '2', '3']

    for name in output_folder_names:
        if not os.path.exists(str(output_path / "train" / name)):
            os.makedirs(str(output_path / "train" / name))

    for index, row in train_data.iterrows():
        image_name = row['image_id']
        label = row['label']

        if mode == 'all':
            shutil.copyfile(str(dataset_path / train_folder / image_name),
                            str(output_path / "train" / f"{label}" / image_name))
        elif mode == '3-vs-all':
            shutil.copyfile(str(dataset_path / train_folder / image_name),
                            str(output_path / "train" / f"{0 if label == 3 else 1}" / image_name))
        else:
            shutil.copyfile(str(dataset_path / train_folder / image_name),
                            str(output_path / "train" / f"{label if label in [0, 1, 2] else label - 1}" / image_name))

    return output_folder_names


def create_validation_split(dataset_root, output_folder_names):
    for name in output_folder_names:
        source_path = dataset_root / "train" / name
        current_path = dataset_root / "validation" / name
        if not os.path.exists(str(current_path)):
            os.makedirs(str(current_path))

        images = glob(f"{str(source_path)}/*.jpg")
        nr_files = len(images)
        validation_split = int(0.2 * nr_files)
        random.shuffle(images)

        for id_x, name in enumerate(images[:validation_split]):
            shutil.move(name, str(current_path / f"{id_x}.jpg"))
