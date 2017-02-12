
from kspLib import *
f1 = open('persistent.sfs')
lines = f1.read()
t1 = fillTree(lines)
f2 = open('test.sfs', 'w')
f2.write(unTree(t1))