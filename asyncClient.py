#!usr/bin/python
loadData = open("persistent.sfs")
for line in loadData:
	if line == "	FLIGHTSTATE\n":
		for line in loadData:
			if line == "		VESSEL\n":
				#do something here to the vessel


			elif line == "	}\n":
				break