encoding time was calculated on a single thread, by encoding a random (but the same ones for all encoding types, i.e. first we picked the random samples and then we tested each method with the same samples) sample of 100 point clouds from training subset of modelnet40. each cloud is formed of 2048 points and is normalized to fit a unit ball. test was repeated for 1000 iterations. time is process time (cpu time), which is not affected by other processes.

errorbarr uses 5*std to show error bar because it was too small otherwise.

Values:
bps mean: 0.18784678974599925
bps std: 0.0019620951073589525
gkde aptbps mean: 17.71632170351896
gkde aptbps std: 0.09248776022151502
bps mean: 0.6485394895859975
bps std: 0.017205025944769876
