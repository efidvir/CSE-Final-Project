import scipy as sc
from scipy import io
import numpy as np
import matplotlib.pyplot as plt

R = sc.io.loadmat('reco_rectangle.mat')
R = R['scene_512']
#R = np.transpose(R, (2,0,1))

print(R.shape)
Rs = []
n = 64
sn = 8
vmin = np.linalg.norm(R,axis=2).min()/64
vmax = np.linalg.norm(R,axis=2).max()/64
for i in range(n):
	if i == n - 1:
		Rs += [np.linalg.norm(R[:,:,i*int(R.shape[2]/n)::], axis=2)]
	else:
		Rs += [np.linalg.norm(R[:,:,i*int(R.shape[2]/n):(i+1)*int(R.shape[2]/n)], axis=(2))]
	if vmin > Rs[i].min():
		vmin = Rs[i].min();
	if vmax < Rs[i].max():
		vmax = Rs[i].max();
fig, ax =plt.subplots(sn,sn)
#print(len(Rs))
for i in range(sn):
	for j in range(sn):
		#print(i*4 +j)
		ax[i,j].pcolormesh(Rs[i*sn + j], vmin=vmin, vmax=vmax)
plt.show()
