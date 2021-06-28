import krpc

defurl = "192.168.2.3"
c = None

def connect(url):
	global c
	print("connecting")
	c = krpc.connect(address=url)
	print("connected")

def ls(a):
	for method in dir(a):
		if method[0] !="_":
			print(method)

def res():
	if isFlight():
		av = c.space_center.active_vessel
		print("Vessel: {}".format(av.name))
		for name in av.resources.names:
			print(" {}: {}/{}".format(name, av.resources.amount(name), av.resources.max(name)))
	else:
		print("not in flight")

def drop(conn):
	conn.close()
	print("disconnected")
	exit()

def parts():
	if isFlight():
		av = c.space_center.active_vessel
		root = av.parts.root
		stack = [(root, 1)]
		while stack:
			part, depth = stack.pop()
			print("{}{}{} - {}".format('|'*(depth-1), '\\'*(depth>1), part.tag, part.title))
			for child in part.children:
				stack.append((child, depth+1))
	else:
		print("not in flight")

def hint():
	if isFlight():
		av = c.space_center.active_vessel
		prevhl = None
		while True:
			for part in av.parts.all:
				if part.highlighted and prevhl != part:
					prevhl = part
					for module in part.modules:
						print(" m> {} {}".format(module.name, module.actions))
	else:
		print("not in flight")

def getOrbit():
	if isFlight():
		av = c.space_center.active_vessel
		return av.orbit
	else:
		print("not in flight")

def isFlight():
	return c.krpc.current_game_scene == c.krpc.GameScene.flight


if __name__ == "__main__":
	connect(defurl)