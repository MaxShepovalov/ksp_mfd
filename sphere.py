import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

resolution = 36 # sections in 1 circle

def drawShape(ax, uS, vS, R, color):
	x = R * np.outer(np.cos(uS), np.sin(vS))
	y = R * np.outer(np.sin(uS), np.sin(vS))
	z = R * np.outer(np.ones(np.size(uS)), np.cos(vS))
	ax.plot_surface(x, y, z,  rstride=1, cstride=1, color=color, linewidth=0, alpha=1,zorder=0.3)

def drawCircularOrbit(ax, R, incl, latitude, color):
	u = np.linspace(0, 2 * np.pi, resolution)
	ax.plot(R*np.sin(u), R*np.cos(u), 0,color='k',zorder=0.5)

def createPlanet(ax):
	u = np.linspace(0, 2 * np.pi, resolution)
	vSky = np.linspace(0, np.pi/2, int(resolution/2))
	vGnd = np.linspace(np.pi/2, np.pi, int(resolution/2))
	#sky
	drawShape(ax, u, vSky, 1, 'cyan')
	#ground
	drawShape(ax, u, vGnd, 1, 'brown')
	#equator
	drawCircularOrbit(ax, 1.01, 0, 0, 'black')
	#meridian
	# drawCircularOrbit(ax, 1.1, 90, 0, 'red')

def makePlot():
	fig = plt.figure(figsize=(6,6), dpi=150, facecolor='black')
	ax = fig.add_subplot(111, projection='3d')
	return fig, ax

if __name__ == "__main__":
	fig, ax = makePlot()
	createPlanet(ax)
	plt.show()