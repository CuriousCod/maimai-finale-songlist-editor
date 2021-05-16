
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


def AffixZeroesToString(text, requiredLength):
    text = str(text)
    if len(text) < requiredLength:
        while requiredLength != len(text):
            text = "0" + text
        return text
    else:
        return text


def BoolToValue(value):
    if value:
        return "1"
    else:
        return "0"

def ValueToBool(value):
    if value == "1":
        return True
    else:
        return False

def BoolToValueReversed(value):
    if value is True:
        return "0"
    else:
        return "1"

def ValueToBoolReversed(value):
    if value == "1":
        return False
    else:
        return True


def GenreTextToFinaleValue(text):
    genres = {"Pops & Anime": "4", "niconico & Vocaloid": "5", "Touhou Project": "6", "Sega": "7", "Game & Variety": "8", "Original & Joypolis": "9"}

    for genre in genres.keys():
        if text == genre:
            return genres[genre]

    return "0"


def GenreValueToFinaleText(value):
    genres = {"Pops & Anime": "4", "niconico & Vocaloid": "5", "Touhou Project": "6", "Sega": "7", "Game & Variety": "8", "Original & Joypolis": "9"}

    for genre, id in genres.items():
        if value == id:
            return genre

    return "0"