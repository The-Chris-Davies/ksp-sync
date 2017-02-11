#!usr/bin/python
loadData = open("persistent.sfs")

for line in loadData:
	if line == "\tFLIGHTSTATE\n":
		for line in loadData:
			if line == "\t\tVESSEL\n":
				#do something here to the vessel
				for line in loadData:
					print line,
					if line == "\t\t}\n":
						break

			elif line == "	}\n":
				break

loadData.close()