import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import math

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

#orbit
ells.append(getEllipse(A=Ap, P=Pe, e=ec))
#atmosphere
ells.append(getEllipse(A=Atm, P=Atm, faceColor='blue', alpha=0.4))
#surface
ells.append(getEllipse(A=Gnd, P=Gnd, alpha=0.5))

fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
for e in ells:
	ax.add_artist(e)
ax.set_xlim(-SYS_screen_size, SYS_screen_size)
ax.set_ylim(-SYS_screen_size, SYS_screen_size)
ax.set_facecolor(SYS_background_clr)
ax.spines['bottom'].set_color(SYS_ui_clr)
ax.spines['top'].set_color(SYS_ui_clr)
ax.spines['left'].set_color(SYS_ui_clr)
ax.spines['right'].set_color(SYS_ui_clr)
ax.xaxis.label.set_color(SYS_ui_clr)
ax.yaxis.label.set_color(SYS_ui_clr)
ax.tick_params(axis='x', colors=SYS_ui_clr)
ax.tick_params(axis='y', colors=SYS_ui_clr)
ax.minorticks_on()
fig.set_edgecolor('White')
fig.set_facecolor(SYS_background_clr)

ax.text(s=orbitParams, x=-0.95*SYS_screen_size/2, y=-0.95*SYS_screen_size/2, color=SYS_ui_clr, fontfamily='monospace')

plt.show()