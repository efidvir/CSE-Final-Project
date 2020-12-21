import numpy as np
import scipy as sc
from scipy import io, interpolate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

mat = sc.io.loadmat(r'scene_512_120620.mat')
mat = mat['scene_512']


## Parameters
c = float(299792458);          # speed of light, in m/s

# Antenna array parameters

n_ant_x = 8;
n_ant_y = 8;
delta_x = 6.25e-2
delta_y = 6.25e-2

# RF system parameters

f_carrier = 5e9;       # units are Hz
bandwidth = 750e6;        # from 10 GHz to 12 GHz
#chirp_duration = 4e-6;  # units are seconds
n_samps = float(mat.shape[2]);
delta_f = bandwidth / n_samps;
#delta_f = 250e6
# Scene parameters

range_max = 6;          # maximum range to target, in metres

Dx = delta_x;
Dy = delta_y;
f0 = float(f_carrier);
Df = delta_f;
Z1 = 1;


def SAR(s):
    # Compute A
    #A  = np.zeros(s.shape)    
    A  = np.fft.fft2(s,axes=(0,1))
    print(np.linalg.norm(A[:,0,0]))
    Nx = A.shape[0] 
    Ny = A.shape[1]
    N  = A.shape[2]
    print('FFT Done')
    kx = 2*np.pi*np.append(np.arange(0,int((Nx)/2)),  -Nx + np.arange(int((Nx)/2),Nx))/(Nx * Dx)
    ky = 2*np.pi*np.append(np.arange(0,int((Ny)/2)),  -Ny + np.arange(int((Ny)/2),Ny))/(Ny * Dy)
    # Compute D
    def D_Compute(i,j,n):
        if i < Nx/2:
            kx = i/Nx * 2*np.pi/Dx;
        else:
            kx = (i-Nx)/Nx * 2*np.pi/Dx;
        if j < Ny/2:
            ky = j/Ny * 2*np.pi/Dy;
        else:
            ky = (j-Ny)/Ny * 2*np.pi/Dy;       
               
        k = 2*np.pi*(f0 + n*Df)/c;        
        kz = np.sqrt(0j + 4*np.power(k,2) - np.power(kx,2) - np.power(ky,2))
        return A[i,j,n] * np.exp(-1j * kz * Z1)
    
    # Equation from SAR Seismic paper    
    # t0 = abs(2*Z1/c);
    # Dijn = exp(-1j * (c*t0*k^2/2 - kz*abs(Z1))) * kz/k;
    # Dijn = exp(-1j * (- kz*abs(Z1)));% * abs(kz/k);        
    
    Nxx, Nyy, NN = np.meshgrid(np.arange(Nx),np.arange(Ny),np.arange(N))
    D = np.vectorize(D_Compute)(Nxx, Nyy, NN)
    D = np.transpose(D, (1,0,2))

    print("D computed");
    
    f_max = f0 + (N-1)*Df;
    k_min = 2*np.pi*f0/c;
    k_max = 2*np.pi*f_max/c;
    kx_max = (Nx-1)/Nx * 2*np.pi/Dx / 2;
    ky_max = (Ny-1)/Ny * 2*np.pi/Dy / 2;    
    kz_min = np.sqrt(0j + 4*k_min**2 - kx_max**2 - ky_max**2)
    kz_max = np.sqrt(0j + 4*k_max**2 - 0 - 0)
    
    kz = np.linspace(np.real(kz_min), np.real(kz_max), N);    
    Nxx, Nyy = np.meshgrid(np.arange(Nx),np.arange(Ny))
    def E_compute_row(i,j):                
        _k = 0.5*np.sqrt(0j + np.power(kx[i],2) + np.power(ky[j],2) + np.power(kz,2));
        w = c*_k;
        f = w / (2*np.pi)
        n = ((c*_k)/(2*np.pi) - f0)/Df;            
        return n    
    EE  = np.vectorize(E_compute_row, signature='(),()->(m)')(Nxx, Nyy)        
    EE = np.transpose(EE, (1,0,2))
    E = np.zeros(EE.shape)*1j
    def interp1(i,j):
        data = D[i,j,:].reshape((1,1,N))        
        return sc.interpolate.interp1d(np.arange(N)+1, data[:],  kind='linear', bounds_error=False,fill_value=(0))(EE[i,j,:] + 1) +0j;
    E = np.vectorize(interp1, signature='(),()->(m)')(Nxx, Nyy)
    print("E Computed")  
    # IFFT
    E = np.transpose(E, (0,1,2))
    R = np.fft.ifftn(E, axes=(2,1,0))
    R = np.flip(R, axis=0)
    print("R Computed")
    return R;
    
R = SAR(mat)
scene = np.linalg.norm(R, axis=(2))
X, Y = np.meshgrid(np.arange(scene.shape[0]),np.arange(scene.shape[1]))
plt.pcolormesh(X, Y, scene)
plt.show()
'''
Nxx, Nyy, NN = np.meshgrid(np.arange(scene.shape[0]),np.arange(scene.shape[1]),np.arange(scene.shape[2]))
fig = go.Figure(data=go.Isosurface(
    x=Nxx.flatten(), y=Nyy.flatten(), z=NN.flatten(), value=scene.flatten(), opacity=0.3, isomin=scene.min(), isomax=scene.max()))
fig.show()
'''
