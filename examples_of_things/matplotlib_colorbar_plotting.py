import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

#make data
mask_arr=np.random.rand(100,100)
distance=mask_arr*2
extent=[0,100,0,100]

#create figure
fig=plt.figure()

###############
# plot distance
ax=fig.add_subplot(211)

plt.imshow(distance, extent=extent)

# make new axis in which to put the colorbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

#create colorbar which will be added to the new axis (now the current axis)
cb = plt.colorbar(cax=cax)

###############
# plot mask_array
ax2=fig.add_subplot(212) # sets curent axis - can use plt calls to modify current axis

plt.imshow(mask_arr, cmap='afmhot_r', extent=extent)

# make a new axis - same as where colorbar was above (to ensure main part of the plot is in the same location)
divider = make_axes_locatable(ax2)
cax = divider.append_axes("right", size="5%", pad=0.1)

# make stuff in axis invisible
cax.set_axis_bgcolor('none')
for axis in ['top','bottom','left','right']:
    cax.spines[axis].set_linewidth(0)
cax.set_xticks([])
cax.set_yticks([])

#plt.show()
plt.savefig("colorbars_tobe_ornot.png", dpi=300, transparent=True)