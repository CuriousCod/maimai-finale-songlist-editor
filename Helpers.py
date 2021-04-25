
def SplitMusicOrScoreLine(line):
    # Remove the mess from the beginning and the end of the line
    line = line[line.find(" ") + 1:line.rfind("\"") + 1]

    splitDataLine = line.split(",")
    splitDataLine = [x.replace(" ", "").replace("\"", "") for x in splitDataLine]

    return tuple(splitDataLine)


def SetSpacing(data, maxmimumSpace):
    data = str(data)
    data += ", "

    space = ""
    for i in range(maxmimumSpace):
        space += " "

    for i in range(len(data.replace(", ", ""))):
        space = space[:-1]
    data += space

    return data