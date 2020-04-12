# Encoding time
## Description
Encoding time was calculated on a single thread, 
calculating the process time (CPU time), 
meaning  that  it  is  not  affected  by  other processes.

Test was repeated for 1000 iterations.

The error bar is shown as 5*std to better display it (too small otherwise).

### Input
The input is made up of 100 point clouds randomly sampled
from the training subset of the [ModelNet40](https://modelnet.cs.princeton.edu/) dataset.

Each cloud is formed of 2048 points and is normalize to fit a unit ball.

## Data
Data is organized in 3 `.csv` files, one for each encoding method. 
Each file 1000 rows of data, one for each test iteration.

This table summarizes the data:

| Encoding method | Time (s) |
| --- | --- |
| GKDE APTBPS | 17.7163 ± 0.0925 |
| FFTKDE APTBPS | 0.6485 ± 0.0172 |
| BPS | 0.1879 ± 0.0020 |


## Graph
![](graphs/encoding-time-comparison.png?raw=true)