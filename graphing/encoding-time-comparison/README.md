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

## Values
Values:
bps mean: 0.18784678974599925
bps std: 0.0019620951073589525
gkde aptbps mean: 17.71632170351896
gkde aptbps std: 0.09248776022151502
bps mean: 0.6485394895859975
bps std: 0.017205025944769876

## Graph
![](graphs/encoding-time-comparison.svg?raw=true)