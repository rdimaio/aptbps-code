# Misc files
Some extra files that you may find useful.

- `semantic3d-downloader.py`: script to download and unzip the Semantic3D dataset
    - Always downloads the training subset by default 
    - Uncomment the last part of the script as needed to download either the reduced-8 or semantic-8 test subset

- `semantic3d-label-counter.py`: logs the label distribution of the Semantic3D training subset

- `semantic3d-csv-to-h5.ipynb`: converts unzipped Semantic3D files from `.csv` to `.h5`

- `semantic3d-processing-and-encoding.ipynb`: tests with encoding Semantic3D files

- `density-estimation-test.ipynb`: testing and visualizing kernel density estimation (KDE) output on clouds from ModelNet40

- `encoding-test.ipynb`: testing early aptbps version