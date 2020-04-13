import os
import sys
import subprocess
import urllib.request

DIR_PATH = os.path.dirname(__file__)
DATA_PATH = os.path.join(DIR_PATH, 'data')
TRAIN_PATH = os.path.join(DATA_PATH, 'train')
TEST_PATH_REDUCED = os.path.join(DATA_PATH, 'test', 'reduced-8')
TEST_PATH_SEMANTIC = os.path.join(DATA_PATH, 'test', 'semantic-8')

# e.g.: 'http://www.semantic3d.net/data/point-clouds/training1/bildstein_station1_xyz_intensity_rgb.7z'
train_url_prefix = 'http://www.semantic3d.net/data/point-clouds/training1/'
train_label_url_prefix = 'http://www.semantic3d.net/data/'

test_semantic_url_prefix = 'http://www.semantic3d.net/data/point-clouds/testing1/'
test_reduced_url_prefix = 'http://www.semantic3d.net/data/point-clouds/testing2/'

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

# semantic-8
test_files_semantic = [
    "birdfountain_station1_xyz_intensity_rgb",
    "castleblatten_station1_intensity_rgb",
    "castleblatten_station5_xyz_intensity_rgb",
    "marketplacefeldkirch_station1_intensity_rgb",
    "marketplacefeldkirch_station4_intensity_rgb",
    "marketplacefeldkirch_station7_intensity_rgb",
    "sg27_station10_intensity_rgb",
    "sg27_station3_intensity_rgb",
    "sg27_station6_intensity_rgb",
    "sg27_station8_intensity_rgb",
    "sg28_station2_intensity_rgb",
    "sg28_station5_xyz_intensity_rgb",
    "stgallencathedral_station1_intensity_rgb",
    "stgallencathedral_station3_intensity_rgb",
    "stgallencathedral_station6_intensity_rgb"
]

# reduced-8
# Note: the reduced files have the .txt extension, unlike semantic-8
test_files_reduced = [
    "MarketplaceFeldkirch_Station4_rgb_intensity-reduced.txt",
    "StGallenCathedral_station6_rgb_intensity-reduced.txt",
    "sg27_station10_rgb_intensity-reduced.txt",
    "sg28_Station2_rgb_intensity-reduced.txt"
]

def download_data(name, data_dir, url_prefix):

    # Display status bar for download
    def _download_reporthook(blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 1e2 / totalsize
            s = "\r%5.1f%% %*d / %d" % (
                percent, len(str(totalsize)), readsofar, totalsize)
            sys.stderr.write(s)
            if readsofar >= totalsize:  # near the end
                sys.stderr.write("\n")
        else:  # total size is unknown
            sys.stderr.write("read %d\n" % (readsofar,))

    def _make_url(url_prefix, zip_path):
        return url_prefix + zip_path

    def _unzip_data(zip_path, target_path):
        out_arg = '-o' + target_path + '/' + name
        # 7zip output can be annoying; add stdout=subprocess.DEVNULL parameter to subprocess.run if you want to suppress the output
        # (disadvantage: if you suppress the output, you can't see the unzipping status)
        subprocess.run(['7z','x',zip_path,out_arg])

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    zip_path = name + '.7z'
    url = _make_url(url_prefix, zip_path)
    download_path = os.path.join(data_dir, zip_path)

    folder_path = os.path.join(data_dir, name)
    # Ensure folder_path exists before attempting os.listdir
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if not os.listdir(folder_path):
        # Only download .7z if not already downloaded
        if not os.path.exists(download_path):
            urllib.request.urlretrieve(url, download_path, _download_reporthook)
        else:
            print(zip_path + "already exists; skipping download")

        print('Unzipping ' + zip_path + '..')
        _unzip_data(download_path, data_dir)
    else:
        print(folder_path + "is not empty; skipping unzipping process.\nIf you are trying to redownload this file, please delete " + folder_path + " and try again.")

    if os.path.exists(download_path):
        # Delete .7z file when done
        os.remove(download_path)

    return

print("Downloading Semantic3D training data!")
for i, f in enumerate(train_files):
    print("[" + str(i+1) + "/" + str(len(train_files)) + "]: Downloading " + f)
    download_data(f, TRAIN_PATH, train_url_prefix)
print("Training data download finished.")


print("Downloading Semantic3d training labels!")
labels_file = 'sem8_labels_training'
download_data(labels_file, TRAIN_PATH, train_label_url_prefix)
print("Training data labels download finished.")

# Toggle whether to test on semantic-8 or reduced-8
#test_semantic = False
#if test_semantic:
#    print("Downloading Semantic3D test data! (semantic-8)")
#    for i, f in enumerate(test_files_semantic):
#        print("[" + str(i+1) + "/" + str(len(test_files_semantic)) + "]: Downloading " + f)
#        download_data(f, TEST_PATH_SEMANTIC, test_semantic_url_prefix)
#else:
#    print("Downloading Semantic3D test data! (reduced-8)")
#    for i, f in enumerate(test_files_reduced):
#        print("[" + str(i+1) + "/" + str(len(test_files_reduced)) + "]: Downloading " + f)
#        download_data(f, TEST_PATH_REDUCED, test_reduced_url_prefix)
#
#print("Testing data download finished.")