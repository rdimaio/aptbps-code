# Counts labels for each training point cloud, logs to a fileg
from collections import Counter
import os
from tqdm import tqdm

DIR_PATH = os.path.dirname(__file__)
DATA_PATH = os.path.join(DIR_PATH, 'data')
LOGS_PATH = os.path.join(DIR_PATH, 'logs')
TRAIN_PATH = os.path.join(DATA_PATH, 'train')
LABELS_PATH = os.path.join(TRAIN_PATH, 'train-labels')

# Same files for both reduced-8 and semantic-8
train_files = [
    "bildstein_station1_xyz_intensity_rgb",
    "bildstein_station3_xyz_intensity_rgb",
    "bildstein_station5_xyz_intensity_rgb",
    "domfountain_station1_xyz_intensity_rgb",
    "domfountain_station2_xyz_intensity_rgb",
    "domfountain_station3_xyz_intensity_rgb",
    "neugasse_station1_xyz_intensity_rgb",
    "sg27_station1_intensity_rgb",
    "sg27_station2_intensity_rgb",
    "sg27_station4_intensity_rgb",
    "sg27_station5_intensity_rgb",
    "sg27_station9_intensity_rgb",
    "sg28_station4_intensity_rgb",
    "untermaederbrunnen_station1_xyz_intensity_rgb",
    "untermaederbrunnen_station3_xyz_intensity_rgb",
]

log_file = os.path.join(LOGS_PATH, 'balance.log')

if not os.path.exists(LOGS_PATH):
    os.makedirs(LOGS_PATH)

for f in tqdm(train_files):
    print("Counting labels in " + f)
    file_name = f + '.labels'
    f_path = os.path.join(LABELS_PATH, file_name)
    # Open file and count occurences of each label
    c = Counter()
    for line in tqdm(open(f_path, 'r')):
        c.update(line.split())

    print("Writing count of labels to " +log_file)
    with open(log_file, 'a') as log:
        log.write(str(c))
