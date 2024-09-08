
import re

source = "A"
destination = "C"
auxilary = "B"


def toh(size, source, destination, auxilary):
    if size==1:
        print("Move 1 from {} tower to {} tower".format(source,destination))
        return 

    toh(size-1,source,auxilary,destination)
    print ("Move size {} disk from {} tower to {} tower".format(size,source,destination))
    toh(size-1,auxilary,destination,source)
    return


n=3
toh(n,source,destination,auxilary)