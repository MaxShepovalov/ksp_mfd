#calculate resistance for N buttons
#  
#   +5v----#---> btn 1 <---#---->> Vout
#          |               |
#      R1 [ ]              |
#          |               |
#          #---> btn 2 <---#
#          |               |
#      R2 [ ]              |
#          |               |
#          #---> btn 3 <---#
#          |               |
#      R3 [ ]              |
#          |               |
#          #---> btn 4 <---#
#          |               |
#      R4 [ ]              |
#          |               |
#          #---> btn 5 <---#
#          |               |
#   R N-1 [ ]              |
#          |               |
#          #---> btn N <---#
#                          |
#                     Rg  [ ]
#                          |
#                      GND V
#

Vin = 5.0 #v
N = 7
Rg = 1000 #Ohm

#find target values for resulting voltages
Vstep = Vin/N
Vouts = [Vin]
for i in range(N-1):
	Vouts.append(Vouts[i]-Vstep)
#find resistance
R = []
for Vtrg in Vouts:
	Rtrg = Vin*Rg/Vtrg - Rg
	R.append(Rtrg)
#print table
for i in range(1, N):
	byteValue = int(255*Vouts[i]/Vin)
	print("R{} {:7.2f} Ohm -> {:2.2f} V (byte {:3} {})".format(i, R[i], Vouts[i], byteValue, hex(byteValue)))
print("Rg {:6.2f} Ohm".format(Rg))
