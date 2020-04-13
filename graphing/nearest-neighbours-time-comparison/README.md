time was calculated on a single thread, by using a random (but the same ones for all nearest neighbor methods, i.e. first we picked the random samples and then we tested each method with the same samples) sample of 100 point clouds from training subset of modelnet40. each cloud is formed of 2048 points and is normalized to fit a unit ball. test was repeated for 1000 iterations. time is process time (cpu time), which is not affected by other processes.

errorbar uses 5*std to show error bar because it was too small otherwise.

Values:
kd-tree mean: 0.18674342801100055
kd-tree std: 0.002277413432554225

ball tree mean: 0.23528463710600142
ball tree std: 0.0026603510409827064

annoy mean: 0.6780599427299913
annoy std: 0.008860050970546903

nmslib mean: 44.85518789950985
nmslib std: 0.04551729026147752

ngt mean: 4.980488702268805
ngt std: 0.014589451692886418

mrpt mean: 7.865359997375998
mrpt std: 0.03521138558884549
