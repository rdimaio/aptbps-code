# PS you may get RuntimeError after saving is done. The script still saves the animations.

import subprocess
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

import sys
import os
from scipy import stats
# local dependencies
from aptbps import aptbps
from modelnet40 import load_modelnet40
from sklearn.neighbors import NearestNeighbors

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
DATA_PATH = os.path.join(PROJECT_DIR, 'data')
BPS_CACHE_FILE = os.path.join(DATA_PATH, 'bps_mlp_data.npz')
LOGS_PATH = os.path.join(PROJECT_DIR, 'logs')

N_POINTS = 2048 # Number of input points
N_BPS_POINTS = 512 # Number of points in reference point cloud
BPS_RADIUS = 1 # Radius of reference point cloud
RANDOM_SEED = 13 # Used in reference point cloud generation

N_PARTS = 4 # Number of partitions

ELEV = 10 # Viewing angle elevation

# This is used in the animate(i) function
# Don't set this too high! I found the sweet spot to be 1.5 ~ 2.
ANIMATION_SPEED = 1.5

# Parameters to save function #
FPS = 60
# 300 dpi seems good enough.
# checking online it seems that 300 dpi = high resolution
# is considered be a rule of thumb for graphic designers;
# even though that refers to printed media, where dpi actually matters.
# Some links:
#   https://www.realspace3d.com/resources/understanding-3d-rendering-and-animation-resolution/
#   https://www.videomaker.com/community/forums/topic/resolution-for-still-photos-in-hd-video
#   https://community.adobe.com/t5/photoshop/72-dpi-or-300-dpi-which-is-better-for-web-and-print-both/td-p/9015163?page=1
# Adjust this as needed! :)
DPI = 300

# Parameters to FuncAnimation #
# How many frames to animate; 
# 360/ANIMATION_SPEED is a full rotation
FUNC_FRAMES = int(360//ANIMATION_SPEED)
INTERVAL = 0 # Delay between each frame in ms

save_1 = True # save input animation
save_2 = True # save density estimation animation
save_3 = True # save partitioning animation
save_4 = True # save reference set animation
save_5 = True # save nearest neighbours animation

# Note: the change in plot scatter order (x,z,y instead of x,y,z) only changes the viewing angle;
# it does not affect the cloud itself
# (I'm plotting a cone, animating it in its upright position seems like a good idea)

def input_cloud_plot():
    # Plot input cloud
    im = ax.scatter(x, z, y)
    fig.colorbar(im, ax=ax, shrink=0.7, label="PDF(x,y,z)")
    return fig,

def density_estimation_plot():
    # Plot input cloud, coloured with KDE PDF output
    ax.scatter(x, z, y, c=input_density, vmin=vmin, vmax=vmax)
    return fig,

def partition_plot():
    ax.scatter(x, z, y, c=input_density, vmin=vmin, vmax=vmax, alpha=0.1)
    # Plot current partition
    ax.scatter(xx, zz, yy, c=part_density, vmin=vmin, vmax=vmax)
    return fig,

def reference_set_plot():
    ax.scatter(x, z, y, c=input_density, vmin=vmin, vmax=vmax, alpha=1)

    # Current reference points
    ax.scatter(bx, bz, by, c='C1', alpha=0.4, label='fixed basis $\mathbf{B} = [\mathbf{b_1}, ..., \mathbf{b_k}]^T$')
    return fig,

def nearest_neighbours_search_plot():
    ax.scatter(x, z, y, c=input_density, vmin=vmin, vmax=vmax, alpha=0.1)
    
    # Plot current partition
    ax.scatter(xx, zz, yy, c=part_density, vmin=vmin, vmax=vmax)

    # Current reference points
    ax.scatter(bx, bz, by, c='C1', alpha=0.4, label='fixed basis $\mathbf{B} = [\mathbf{b_1}, ..., \mathbf{b_k}]^T$')

    # Quiver between reference points and input partition
    quiv = ax.quiver(bx, bz, by, dx, dz, dy, normalize=False, alpha=0.4, color='C1', linestyles='solid',  arrow_length_ratio=0.2)

    # convert density to rgba values
    density_rgba = quiv.to_rgba(part_density, norm=False)

    # get values for nearest neighbour indexes 
    # no need to use start-idx, as density_rgba comes from part_density
    c = density_rgba[npts_idx]
    c = c.reshape(-1, 4) # reshape to [n_arrows, 4] (4 because RGBA)
    c[:, 3] = 0.5 # set alpha of quivers to 0.5
                
    # The first set_color sets the colour of the arrow to match 
    # the colour of the destination point in the input partition.
    # The second one sets the arrow colours to bright, high contrast orange.              
    # Uncomment as needed.
    quiv.set_color(c=c) # set color of arrow to correspond to color of destination point
    #quiv.set_color(c='C1') # set color to bright orange

    return fig,



# The input of this function is range(FUNC_FRAMES);
# For each frame, the azim is adjusted by the number in FUNC_FRAMES.
# As azim controls the position of the viewing angle,
# the effect is that the model 'rotates' slightly each frame.
def animate(i):
    ax.view_init(elev=ELEV, azim=i*ANIMATION_SPEED)
    ax.set_xlim3d(-0.8, 0.8)
    ax.set_ylim3d(-0.8, 0.8)
    ax.set_zlim3d(-0.7, 0.7)
    return fig,

# Generate reference set
basis_set = aptbps.generate_random_basis(
                N_BPS_POINTS, n_dims=3, radius=BPS_RADIUS, random_seed=RANDOM_SEED)

xtr, ytr, xte, yte = load_modelnet40(root_data_dir=DATA_PATH)

# Normalize
xtr_normalized = aptbps.normalize(xtr)

# Point cloud to animate
XTR_ID = 31

input_cloud = xtr_normalized[XTR_ID]
values = input_cloud.T

x, y, z = values

# 1. NORMALIZED INPUT POINT CLOUD

# Create a figure and a 3D Axes
fig = plt.figure()
ax = Axes3D(fig)

# Hide grid lines
ax.grid(False)

# Hide axes ticks
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

# Make background panes invisible
ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

# make the grid lines transparent
ax.xaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
ax.yaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
ax.zaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
ax.set_axis_off()

title = "   Normalized input point cloud (" + str(N_POINTS) + " points)"

# x-offset by adding spaces before or after
ax.set_title(title, y=0.1)

if save_1:
    # Animate
    ani = animation.FuncAnimation(fig, animate, init_func=input_cloud_plot,
                                  frames=FUNC_FRAMES, interval=INTERVAL, blit=True)

    fn = '1_norm_input_cloud'
    ani.save(fn+'.mp4', writer='ffmpeg', fps=FPS, dpi=DPI)

    print(fn + " saved.")

# 2. POINT CLOUD AFTER KDE

kde = stats.gaussian_kde(values)

input_density = kde(values)

vmin = min(input_density)
vmax = max(input_density)

# Create a figure and a 3D Axes
fig = plt.figure()
ax = Axes3D(fig)

# Create colorbar
im = ax.scatter(x, z, y, c=input_density, vmin=vmin, vmax=vmax)
fig.colorbar(im, ax=ax, shrink=0.7, label="PDF(x,y,z)")

# Hide grid lines
ax.grid(False)

# Hide axes ticks
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

# Make background panes invisible
ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

# make the grid lines transparent
ax.xaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
ax.yaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
ax.zaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
ax.set_axis_off()

# x-offset by adding spaces before or after
ax.set_title("   Density estimation (Gaussian KDE)", y=0.1)

if save_2:

    # Animate
    ani = animation.FuncAnimation(fig, animate, init_func=density_estimation_plot,
                                  frames=FUNC_FRAMES, interval=INTERVAL, blit=True)

    fn = '2_density_estimation'
    ani.save(fn+'.mp4', writer='ffmpeg', fps=FPS, dpi=DPI)

    print(fn + " saved.")

# 3. PARTITIONING

# Triangle number formula for finding the partition size
part_size = (2*N_BPS_POINTS)//(N_PARTS*(N_PARTS+1))

# Concatenate density colimn
input_density_vec = input_density.reshape(-1, 1)
input_density_cat = np.concatenate([input_cloud, input_density_vec], axis=1)

# Generate partition indexes
part_idxs = []
for i in range(1, N_PARTS):
    part_idxs.append(i*N_POINTS//N_PARTS)

# Partition
input_density_cat = input_density_cat[np.argpartition(
input_density_cat[:, 3], part_idxs)]

# Plot each partition
for i in range(0, N_PARTS):
    start_idx = (N_POINTS//N_PARTS)*i
    end_idx = (N_POINTS//N_PARTS) + start_idx

    # Create a figure and a 3D Axes
    fig = plt.figure()
    ax = Axes3D(fig)

    values = input_density_cat[start_idx:end_idx, 0:3]
    part_density = kde(values.T)
    xx, yy, zz = values.T

    # Create colorbar
    im = ax.scatter(xx, zz, yy, c=part_density, vmin=vmin, vmax=vmax)
    fig.colorbar(im, ax=ax, shrink=0.7, label="PDF(x,y,z)")

    # Hide grid lines
    ax.grid(False)

    # Hide axes ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    # Make background panes invisible
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    # make the grid lines transparent
    ax.xaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
    ax.yaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
    ax.zaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
    ax.set_axis_off()

    if save_3:

        title = "   Input set partitioning\n   Partition #" + str(i+1)

        # x-offset by adding spaces before or after
        ax.set_title(title, y=0.1)

        # Animate
        ani = animation.FuncAnimation(fig, animate, init_func=partition_plot,
                                      frames=FUNC_FRAMES, interval=INTERVAL, blit=True)

        fn = '3_partition_n_' + str(i+1)
        ani.save(fn+'.mp4', writer='ffmpeg', fps=FPS, dpi=DPI)

        print(fn + " saved.")

# 4. REFERENCE SET

# Create a figure and a 3D Axes
fig = plt.figure()
ax = Axes3D(fig)

# Create colorbar
im = ax.scatter(x, z, y, c=input_density, vmin=vmin, vmax=vmax)
fig.colorbar(im, ax=ax, shrink=0.7, label="PDF(x,y,z)")

bx, by, bz = basis_set.T

# Hide grid lines
ax.grid(False)

# Hide axes ticks
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

# Make background panes invisible
ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

# make the grid lines transparent
ax.xaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
ax.yaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
ax.zaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
ax.set_axis_off()

title = "   Reference point cloud (orange) (" + str(N_BPS_POINTS) + " points, radius = " + str(BPS_RADIUS) + ")"

# x-offset by adding spaces before or after
ax.set_title(title, y=0.1)

if save_4:

    # Animate
    ani = animation.FuncAnimation(fig, animate, init_func=reference_set_plot,
                                  frames=FUNC_FRAMES, interval=INTERVAL, blit=True)

    fn = '4_reference_set'
    ani.save(fn+'.mp4', writer='ffmpeg', fps=FPS, dpi=DPI)

    print(fn + " saved.")



# 5. NEAREST NEIGHBOUR SEARCH

# Generate partition indexes for reference set
partitions = []

# Add these points to the basis points for the first partition;
# This makes sure that the encoded cloud will be of size N_BPS_POINTS.
extra = N_BPS_POINTS % part_size
tot_points = 0

for i in range (0, N_PARTS):
    tot_points = tot_points + (N_PARTS-i)*part_size
    partitions.append((N_PARTS-i)*part_size)

tot_points = tot_points + extra

if tot_points is not N_BPS_POINTS:
    extra = extra + (N_BPS_POINTS - tot_points)

# Add extra points for the first partition so that total number of bps points is reached
partitions[0] = partitions[0] + extra

bps_parts = []
bps_deltas = []
fid_dists = []

basis_start_idx = 0

# Plot each partition
for i in range(0, N_PARTS):
    start_idx = (N_POINTS//N_PARTS)*i
    end_idx = (N_POINTS//N_PARTS) + start_idx

    # For current iteration
    n_curr_basis_points = partitions[i]
            
    curr_basis_points = basis_set[basis_start_idx:basis_start_idx+n_curr_basis_points]

    # set up tree for nearest neighbors
    nbrs = NearestNeighbors(n_neighbors=1, leaf_size=16, algorithm="kd_tree").fit(
        input_density_cat[start_idx:end_idx, 0:3])

    # fid_dist, npts_ix = nbrs.kneighbors(curr_basis_points, n_neighbors=(1*n_parts-1*i), return_distance=True)
    fid_dist, npts_idx = nbrs.kneighbors(
        curr_basis_points, n_neighbors=1, return_distance=True)

    bps_parts.append(input_density_cat[start_idx+npts_idx, 0:3])

    basis_start_idx = n_curr_basis_points

    # Create a figure and a 3D Axes
    fig = plt.figure()
    ax = Axes3D(fig)

    bps_delta = bps_parts[i].squeeze() - curr_basis_points
    bps_delta = bps_delta.reshape(-1, 3)
    bps_deltas.append(bps_delta)

    values = input_density_cat[start_idx:end_idx, 0:3]
    part_density = kde(values.T)
    xx, yy, zz = values.T
    bx, by, bz = curr_basis_points.T
    dx, dy, dz = bps_delta.T # deltas between ref and input

    # Create colorbar
    im = ax.scatter(xx, zz, yy, c=part_density, vmin=vmin, vmax=vmax)
    fig.colorbar(im, ax=ax, shrink=0.7, label="PDF(x,y,z)")

    # Hide grid lines
    ax.grid(False)

    # Hide axes ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    # Make background panes invisible
    ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    # make the grid lines transparent
    ax.xaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
    ax.yaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
    ax.zaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
    ax.set_axis_off()

    if save_5:

        title = "   Nearest neighbour search\n   Partition #" + str(i+1) + ": " + str(n_curr_basis_points) + " reference points"

        # x-offset by adding spaces before or after
        ax.set_title(title, y=0.1)

        # Animate
        ani = animation.FuncAnimation(fig, animate, init_func=nearest_neighbours_search_plot,
                                      frames=FUNC_FRAMES, interval=INTERVAL, blit=True)

        fn = '5_nearneigh_n_' + str(i+1)
        ani.save(fn+'.mp4', writer='ffmpeg', fps=FPS, dpi=DPI)

        print(fn + " saved.")


'''
sys.exit()

# --- PARTITIONS

input_density = input_density.reshape(-1, 1)

input_density_cat = np.concatenate([input_cloud, input_density], axis=1)

num_points = input_density_cat.shape[0]
#num_points = x[fid].shape[0]

part_idxs = []
basis_part_idxs = []

for i in range(1, N_PARTS):
    part_idxs.append(i*num_points//N_PARTS)

# partition in N_PARTS
input_density_cat = input_density_cat[np.argpartition(
input_density_cat[:, 3], part_idxs)]

x, y, z = values

# Create a figure and a 3D Axes
fig = plt.figure()
ax = Axes3D(fig)

# Hide grid lines
ax.grid(False)

# Hide axes ticks
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])

# Make background panes invisible
ax.xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
ax.zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

# make the grid lines transparent
ax.xaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
ax.yaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
ax.zaxis._axinfo["grid"]['color'] = (1, 1, 1, 0)
ax.set_axis_off()

# x-offset by adding spaces before or after
ax.set_title("   Input point cloud", y=0.1)

# Animate
ani = animation.FuncAnimation(fig, animate, init_func=init,
                              frames=10, interval=0, blit=True)

fn = 'rotate_azimuth_angle_3d_surf'
ani.save(fn+'.mp4', writer='ffmpeg', fps=60, dpi=100)

# --- FINAL ENCODED ARRAY
'''
