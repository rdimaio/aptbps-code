# Accuracy by number of partitions
## Description
The accuracy was calculated as the mean of the model's accuracy for the last 10 epochs (out of 1200 epochs in total).

Accuracy was measured over the test dataset; 
no validation dataset was used to maximize the amount of data used in training.

The error is presented as the standard error of the mean.

## Input
The models were trained with the training subset of the ModelNet40 dataset;
test accuracy was measured on the test subset of the same dataset.

## Data
Data is organized in 5 `.csv` files, one for each encoding method considered.
Each file 1200 rows of data (+header), one for each epoch.
`bps_mlp.csv` contains one column.
The other four files contain 19 columns, one for each n. of partitions considered (2 to 20).

The table below summarizes the data.

| Number of partitions | BPS MLP accuracy (%) | triangle-gkde MLP accuracy (%) | comp-gkde MLP accuracy (%) | triangle-fftkde accuracy (%) | comp-fftkde MLP accuracy (%) |
| --- | --- | --- | --- | --- | --- |
| 1 | 88.75 ± 0.08 | - | - | - | - |
| 2 | - | 89.06 ± 0.03 | 88.84 ± 0.05 | 83.85 ± 0.06 | 83.82 ± 0.03 |
| 3 | - | 88.31 ± 0.04 | 88.26 ± 0.04 | 85.15 ± 0.07 | 84.40 ± 0.06 |
| 4 | - | 87.54 ± 0.05 | 87.88 ± 0.04 | 85.19 ± 0.08 | 83.60 ± 0.04 |
| 5 | - | 87.78 ± 0.05 | 87.99 ± 0.03 | 84.39 ± 0.07 | 84.41 ± 0.03 |
| 6 | - | 87.71 ± 0.06 | 87.48 ± 0.07 | 84.99 ± 0.04 | 83.93 ± 0.04 |
| 7 | - | 87.37 ± 0.07 | 87.75 ± 0.06 | 84.78 ± 0.05 | 84.85 ± 0.05 |
| 8 | - | 87.10 ± 0.04 | 86.73 ± 0.06 | 85.15 ± 0.05 | 83.93 ± 0.04 | 
| 9 | - | 87.02 ± 0.06 | 86.65 ± 0.04 | 84.51 ± 0.06 | 83.36 ± 0.05 |
| 10 | - | 86.94 ± 0.10 | 86.90 ± 0.10 | 83.61 ± 0.10 | 83.67 ± 0.08 |
| 11 | - | 86.78 ± 0.05 | 86.95 ± 0.07 | 84.00 ± 0.05 | 83.97 ± 0.09 |
| 12 | - | 86.52 ± 0.03 | 85.73 ± 0.07 | 84.40 ± 0.07 | 83.51 ± 0.04 |
| 13 | - | 86.64 ± 0.05 | 86.16 ± 0.03 | 84.11 ± 0.07 | 83.36 ± 0.10 |
| 14 | - | 86.16 ± 0.07 | 85.68 ± 0.09 | 83.88 ± 0.07 | 83.12 ± 0.08 |
| 15 | - | 86.33 ± 0.04 | 85.77 ± 0.04 | 84.05 ± 0.09 | 82.91 ± 0.03 |
| 16 | - | 86.28 ± 0.05 | 85.41 ± 0.07 | 83.23 ± 0.06 | 82.79 ± 0.06 |
| 17 | - | 86.29 ± 0.06 | 86.07 ± 0.08 | 82.83 ± 0.06 | 82.87 ± 0.05 |
| 18 | - | 85.30 ± 0.06 | 85.64 ± 0.06 | 83.22 ± 0.03 | 82.81 ± 0.06 |
| 19 | - | 86.16 ± 0.04 | 85.88 ± 0.07 | 82.14 ± 0.06 | 82.79 ± 0.05 |
| 20 | - | 86.21 ± 0.06 | 85.37 ± 0.04 | 82.54 ± 0.06 | 81.94 ± 0.05 | 


## Graph
![](graphs/accuracy-by-n-partitions-all.png?raw=true)