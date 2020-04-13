library(ggplot2)
library(tcltk)

aptbps2 <- read.csv(file = 'density-accuracy.csv', header = TRUE)

# Linux
X11() # Use windows() or quartz() if on Windows or MacOS.

# Accuracy needs to be passed in as factors to be compatible with cdplot
# change to either "bps" or "aptbps" to obtain the relevant data
accuracy <- factor(aptbps2[,"bps"])

density <- aptbps2[,"density"]

# Cube transform (only passing density glitches cdplot)
# Source: https://rcompanion.org/handbook/I_12.html
norm_density <- sign(density) * abs(density)^(1/3)

# Uncomment to save to file in the working directory
# pdf('aptbps.pdf')

cdplot(accuracy ~ norm_density, xlab="variance in density", data = aptbps2, col = c("darksalmon", "darkseagreen1"))

prompt  <- "click to close plot"
capture <- tk_messageBox(message = prompt)