#ui speed test
import time
start = time.time()
prev = start

logs = []
def log(msg):
	global prev
	now = time.time()
	logs.append("{}, {}: {}".format(now - start, now - prev, msg))
	prev = now
#===============================

log("start")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import math
log("imports")

SYS_screen_size = 100 #km
SYS_background_clr = 'black'
SYS_ui_clr = 'white'

ells = []

#Kerbin
Gnd = 30 #km
Atm = 70+Gnd #km

Ap = 60+Gnd #km
Pe = 31+Gnd #km
ec = 0.7

orbitParams = 'Ap {}\nPe {}\nEc {}'.format(Ap,Pe,ec)

log("default values")

def getEllipse(A, P, e=0, alpha=1.0, edgeColor=SYS_ui_clr, faceColor=None):
	x = (A-P)/2
	a = A+P
	b = a*pow(1-e*e, 0.5)
	print("for A={} P={} e={} : x={} a={} b={}".format(A,P,e,x,a,b))
	return Ellipse(
		xy=(x, 0),
		width=a,
		height=b,
		angle=0,
		fill=faceColor!=None,
		edgecolor=edgeColor,
		facecolor=faceColor,
		alpha=alpha)

log("def getEllipse")

#orbit
ells.append(getEllipse(A=Ap, P=Pe, e=ec))
log("math orbit")
#atmosphere
ells.append(getEllipse(A=Atm, P=Atm, faceColor='blue', alpha=0.4))
log("math atmosphere")
#surface
ells.append(getEllipse(A=Gnd, P=Gnd, alpha=0.5))
log("math surface")

fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
log("plt subplots")

for e in ells:
	ax.add_artist(e)
	log("add ellipse")
ax.set_xlim(-SYS_screen_size, SYS_screen_size)
log("xlim")
ax.set_ylim(-SYS_screen_size, SYS_screen_size)
log("ylim")
ax.set_facecolor(SYS_background_clr)
log("facecolor")
ax.spines['bottom'].set_color(SYS_ui_clr)
log("spine bottom")
ax.spines['top'].set_color(SYS_ui_clr)
log("spines top")
ax.spines['left'].set_color(SYS_ui_clr)
log("spines left")
ax.spines['right'].set_color(SYS_ui_clr)
log("spines right")
ax.xaxis.label.set_color(SYS_ui_clr)
log("x axis color")
ax.yaxis.label.set_color(SYS_ui_clr)
log("y axis color")
ax.tick_params(axis='x', colors=SYS_ui_clr)
log("tick x")
ax.tick_params(axis='y', colors=SYS_ui_clr)
log("tick y")
ax.minorticks_on()
log("minorticks")
fig.set_edgecolor('White')
log("edgecolor")
fig.set_facecolor(SYS_background_clr)
log("facecolor")

ax.text(s=orbitParams, x=-0.95*SYS_screen_size/2, y=-0.95*SYS_screen_size/2, color=SYS_ui_clr, fontfamily='monospace')
log("text")

plt.show()
log("show")

#===============================

#print result
print("\n".join(logs))