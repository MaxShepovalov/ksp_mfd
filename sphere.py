import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from math import sin, cos
import time

resolutionX = 5 # angle between horizontal dots
resolutionY = 5 # angle between vertical dots

topSphere = None
btmSphere = None

def rotate(craftOrientation, x, y, z):
	pitch, yaw, roll = craftOrientation
	t = np.transpose(np.array([x,y,z]), (1,2,0))
	#rotate by yaw
	yr = np.radians(-yaw)
	mY = [[cos(yr), -sin(yr), 0],[sin(yr),cos(yr),0],[0,0,1]]
	t = np.dot(t, mY)
	#rotate by pitch
	pr = np.radians(-pitch)
	mP = [[cos(pr), 0, sin(pr)],[0,1,0],[-sin(pr), 0, cos(pr)]]
	t = np.dot(t, mP)
	#rotate by roll
	rr = np.radians(roll)
	mR = [[1, 0, 0],[0, cos(rr), -sin(rr)],[0,sin(rr),cos(rr)]]
	return np.transpose(np.dot(t, mR), (2,0,1))

def drawShape(ax, craftOrientation, uS, vS, R, color, z):
	x = R * np.outer(np.cos(uS), np.sin(vS))
	y = R * np.outer(np.sin(uS), np.sin(vS))
	z = R * np.outer(np.ones(np.size(uS)), np.cos(vS))
	
	x,y,z = rotate(craftOrientation, x, y, z)
	return ax.plot_surface(x, y, z,  rstride=1, cstride=1, color=color, linewidth=0, alpha=1,zorder=z,shade=False)

# def drawCircularOrbit(ax, craftOrientation, R, incl, latitude, color):
# 	pitch, yaw, roll = craftOrientation
# 	#make equator
# 	u = np.linspace(0, 2 * np.pi, int(360/resolutionX))
# 	x = R * np.outer(np.cos(u), np.ones(np.size(u)))
# 	y = R * np.outer(np.sin(u), np.ones(np.size(u)))
# 	z = R * np.outer(np.ones(np.size(u)), np.ones(np.size(u)))

# 	# rotate to real angle
# 	x,y,z = rotate((incl, latitude, 0), x, y, z)

# 	# rotate to view
# 	x,y,z = rotate(craftOrientation, x, y, z)

# 	ax.plot_surface(x,y,z, color='k',zorder=0.3)

def createPlanet(ax, craftOrientation):
	global topSphere
	global btmSphere
	if topSphere != None:
		topSphere.remove()
	if btmSphere != None:
		btmSphere.remove()
	# raw angles
	viewPitch, viewYaw, _ = craftOrientation
	u = np.linspace(np.radians(-viewYaw)-np.pi/2, np.radians(-viewYaw)+np.pi/2, int(90/resolutionX))
	vSky = np.linspace(0, np.pi/2, int(90/resolutionY))
	vGnd = np.linspace(np.pi/2, np.pi, int(90/resolutionY))
	#sky
	topSphere = drawShape(ax, craftOrientation, uS=u, vS=vSky, R=1, color='cyan', z=1+viewPitch>0)
	#ground
	btmSphere = drawShape(ax, craftOrientation, uS=u, vS=vGnd, R=1, color='brown', z=1+viewPitch<0)

def additionalLines(ax, craftOrientation):
	#equator
	drawCircularOrbit(ax, craftOrientation, 1.01, 0, 0, 'white')
	# x = np.linspace(0, 2, 2)
	# y = np.zeros(np.size(x))
	# z = np.zeros(np.size(x))
	# x,y,z = rotate(craftOrientation, x, y, z)
	# ax.plot(y, x, z, color='r')

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
	plt.axis('off')
	# additionalLines(ax)
	return fig, ax

if __name__ == "__main__":
	fig, ax = makePlot()
	craftOrientationPYR = (15, 90, 20)
	createPlanet(ax, craftOrientationPYR)
	#additionalLines(ax, craftOrientationPYR)
	ax.view_init(0, 0)
	plt.show()
	timer = 5 #seconds
	frames = 5*20
	#while plt.fignum_exists(fig.number):
	for angle in range(0, 45, 1):
		if not plt.fignum_exists(fig.number):
			break
		print("yaw {}".format(angle))
		craftOrientationPYR = (15, angle, 20)
		createPlanet(ax, craftOrientationPYR)
		additionalLines(ax, craftOrientationPYR)
		plt.draw()
		plt.pause(timer/frames)
	for angle in range(15, -10, -1):
		if not plt.fignum_exists(fig.number):
			break
		print("pitch {}".format(angle))
		craftOrientationPYR = (angle, 45, 5+angle)
		createPlanet(ax, craftOrientationPYR)
		additionalLines(ax, craftOrientationPYR)
		plt.draw()
		plt.pause(timer/frames)
	print("stopped")