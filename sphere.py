import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time

resolutionX = 5 # angle between horizontal dots
resolutionY = 5 # angle between vertical dots

topSphere = None
btmSphere = None

def drawShape(ax, uS, vS, R, color, z):
	x = R * np.outer(np.cos(uS), np.sin(vS))
	y = R * np.outer(np.sin(uS), np.sin(vS))
	z = R * np.outer(np.ones(np.size(uS)), np.cos(vS))
	return ax.plot_surface(x, y, z,  rstride=1, cstride=1, color=color, linewidth=0, alpha=1,zorder=z,shade=False)

def drawCircularOrbit(ax, R, incl, latitude, color):
	u = np.linspace(0, 2 * np.pi, int(360/resolutionX))
	ax.plot(R*np.sin(u), R*np.cos(u), 0,color='k',zorder=0.3)

def createPlanet(ax, viewV):
	global topSphere
	global btmSphere
	if topSphere != None:
		topSphere.remove()
	if btmSphere != None:
		btmSphere.remove()
	u = np.linspace(0, 2*np.pi, int(180/resolutionX))
	vSky = np.linspace(0, np.pi/2, int(90/resolutionY))
	vGnd = np.linspace(np.pi/2, np.pi, int(90/resolutionY))
	#sky
	topSphere = drawShape(ax, uS=u, vS=vSky, R=1, color='cyan', z=1+viewV>0)
	#ground
	btmSphere = drawShape(ax, uS=u, vS=vGnd, R=1, color='brown', z=1+viewV<0)

def additionalLines(ax):
	#equator
	# drawCircularOrbit(ax, 1.01, 0, 0, 'black')
	x = np.linspace(0, 2, 2)
	y = np.zeros(np.size(x))
	z = np.zeros(np.size(x))
	ax.plot(y, x, z, color='r')

	# angle = np.linspace(0, 4*np.pi, 720) # 1 dot per degree
	# x = np.outer(np.cos(angle), np.ones(np.size(angle)))
	# y = np.outer(np.sin(angle), np.ones(np.size(angle)))
	# s = np.outer(np.ones(np.size(angle)), angle)
	# ax.plot_surface(x, y, s)

	#meridian
	# drawCircularOrbit(ax, 1.1, 90, 0, 'red')

def makePlot():
	plt.ion()
	fig = plt.figure(figsize=(6,6), dpi=150, facecolor='black')
	ax = fig.add_subplot(111, projection='3d')
	ax.grid(False)
	ax.xaxis.pane.set_edgecolor('b')
	ax.yaxis.pane.set_edgecolor('b')
	ax.zaxis.pane.set_edgecolor('b')
	ax.w_xaxis.pane.fill = False
	ax.w_yaxis.pane.fill = False
	ax.w_zaxis.pane.fill = False
	ax.set_facecolor('black')
	ax.set_zlim3d(-1, 1)
	ax.set_xlim(-1, 1)
	ax.set_ylim(-1, 1)
	# plt.axis('off')
	# additionalLines(ax)
	return fig, ax

if __name__ == "__main__":
	fig, ax = makePlot()
	viewU = 0
	viewV = 0
	createPlanet(ax, viewV)
	ax.view_init(viewU, viewV)
	plt.show()
	while plt.fignum_exists(fig.number):
	# for viewV in range(0, 90, 5):
		if not plt.fignum_exists(fig.number):
			break
		print("{} azim {}; elev {}".format(viewV, ax.azim, ax.elev))
		# createPlanet(ax, viewV)
		# ax.view_init(viewV, 0)
		plt.draw()
		plt.pause(.25)
	print("stopped")