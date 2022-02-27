from src.Database import DatabaseActions as dba
import src.Helpers as hlp
import os

# These are configured to be used with files from maimai FiNALE version

def ReadMmMusic(conn, path):
    dataLines = []

    if not os.path.isfile(path + r"/decrypted/mmMusic.txt"):
        print("Couldn't find mmMusic.txt\nPlease decrypt the files before creating a database")
        return

    with open(path + r"/decrypted/mmMusic.txt", "r", encoding="UTF16") as f:
        for line in f.readlines():
            if line.startswith("MMMUSIC"):
                dataLines.append(line.replace("\n", "").replace("RST_MUSICTITLE_", "").replace("RST_MUSICARTIST_", ""))

    for line in dataLines:
        dba.InsertLineToMusic(conn, hlp.SplitMusicOrScoreLine(line))


def ReadMmMusicSingleLine(fileFullname, trackId):
    data = ""

    if not os.path.isfile(fileFullname):
        print("File not found")
        return
    try:
        with open(fileFullname, "r", encoding="UTF16") as f:
            for line in f.readlines():
                if line.startswith(f"MMMUSIC( {trackId},"):
                    data = line.replace("\n", "").replace("RST_MUSICTITLE_", "").replace("RST_MUSICARTIST_", "")
    except Exception as e:
        print(e)
        return None

    return hlp.SplitMusicOrScoreLine(data)


def ReadMmScore(conn, path):
    dataLines = []

    if not os.path.isfile(path + r"/decrypted/mmScore.txt"):
        print("Couldn't find mmScore.txt\nPlease decrypt the files before creating a database")
        return

    with open(path + r"/decrypted/mmScore.txt", "r", encoding="UTF16") as f:
        for line in f.readlines():
            if line.startswith("MMSCORE"):
                dataLines.append(line.replace("\n", ""))

    for line in dataLines:
        dba.InsertLineToScore(conn, hlp.SplitMusicOrScoreLine(line))


# Grabs all lines with the track id
def ReadMmScoreLinesWithTrackId(fileFullname, trackId):
    trackId = hlp.AffixZeroesToString(trackId, 3)

    dataLines = []
    rows = []

    if not os.path.isfile(fileFullname):
        print("File not found")
        return None

    try:
        with open(fileFullname, "r", encoding="UTF16") as f:
            for line in f.readlines():
                if f"eScore_{trackId}" in line:
                    dataLines.append(line.replace("\n", ""))

        for line in dataLines:
            rows.append(hlp.SplitMusicOrScoreLine(line))

    except Exception as e:
        print(e)
        return None

    return rows


def ReadMmTextoutLineWithId(fileFullname, trackId, type):
    types = hlp.CommonData
    trackId = hlp.AffixZeroesToString(trackId, 4)

    if not os.path.isfile(fileFullname):
        print("File not found")
        return None

    try:
        with open(fileFullname, "r", encoding="UTF16") as f:
            for line in f.readlines():
                if type == types.artist:
                    if f"RST_MUSICARTIST_{trackId}" in line:
                        line = line.replace("\n", "")
                        line = line[line.rfind("L\"") + 2:line.rfind("\" )")]
                        return line
                elif type == types.track:
                    if f"RST_MUSICTITLE_{trackId}" in line:
                        line = line.replace("\n", "")
                        line = line[line.rfind("L\"") + 2:line.rfind("\" )")]
                        return line
                elif type == types.designer:
                    if f"RST_SCORECREATOR_{trackId}" in line:
                        line = line.replace("\n", "")
                        line = line[line.rfind("L\"") + 2:line.rfind("\" )")]
                        return line
                else:
                    print("Could not find data")
                    return None
    except Exception as e:
        print(e)
        return None

def ReadSoundBgmLineWithId(fileFullname, trackId):
    trackId = hlp.AffixZeroesToString(trackId, 3)

    if not os.path.isfile(fileFullname):
        print("File not found")
        return None

    with open(fileFullname, "r", encoding="UTF8") as f:
        for line in f.readlines():
            if trackId in line:
                line = line.replace("\n", "")
                return line.split(",")

# def ReadMmScoreLine(fileFullname, trackId):
#     dataLines = []
#
#     with open(fileFullname, "r", encoding="UTF16") as f:
#         for line in f.readlines():
#             if line.startswith("MMSCORE"):
#                 dataLines.append(line.replace("\n", ""))
#
#     for line in dataLines:
#         dba.InsertLineToScore(conn, hlp.SplitMusicOrScoreLine(line))


# Designer name is same in jp and ex
def ReadTextOutEx(conn, path):
    dataLinesArtist = []
    dataLinesTrack = []
    dataLinesDesigner = []

    if not os.path.isfile(path + r"/decrypted/mmtextout_ex.txt"):
        print("Couldn't find mmtextout_ex.txt\nPlease decrypt the files before creating a database")
        return

    with open(path + r"/decrypted/mmtextout_ex.txt", "r", encoding="UTF16") as f:
        for line in f.readlines():
            if line.startswith("MMTEXTOUT( L\"RST_MUSICARTIST"):
                dataLinesArtist.append(line.replace("\n", ""))
            if line.startswith("MMTEXTOUT( L\"RST_MUSICTITLE"):
                dataLinesTrack.append(line.replace("\n", ""))
            if line.startswith("MMTEXTOUT( L\"RST_SCORECREATOR"):
                dataLinesDesigner.append(line.replace("\n", ""))

    for line in dataLinesArtist:
        splitDataLine = []
        id = line[line.find("ARTIST_") + 7:line.find("\" ,")]

        # Remove the mess from the beginning and the end of the line
        line = line[line.rfind("L\"") + 2:line.rfind("\" )")]
        splitDataLine.append(id)
        splitDataLine.append(line)
        dba.InsertLineToTextOutExArtist(conn, splitDataLine)

    for line in dataLinesTrack:
        splitDataLine = []
        id = line[line.find("TITLE_") + 6:line.find("\" ,")]

        # Remove the mess from the beginning and the end of the line
        line = line[line.rfind("L\"") + 2:line.rfind("\" )")]
        splitDataLine.append(id)
        splitDataLine.append(line)
        dba.InsertLineToTextOutExTrack(conn, splitDataLine)

    for line in dataLinesDesigner:
        splitDataLine = []
        id = line[line.find("CREATOR_") + 8:line.find("\" ,")]

        # Remove the mess from the beginning and the end of the line
        line = line[line.rfind("L\"") + 2:line.rfind("\" )")]
        splitDataLine.append(id)
        splitDataLine.append(line)
        dba.InsertLineToTextOutExDesigner(conn, splitDataLine)


def ReadTextOutJp(conn, path):
    dataLinesArtist = []
    dataLinesTrack = []
    dataLinesDesigner = []

    if not os.path.isfile(path + r"/decrypted/mmtextout_jp.txt"):
        print("Couldn't find mmtextout_jp.txt\nPlease decrypt the files before creating a database")
        return

    with open(path + r"/decrypted/mmtextout_jp.txt", "r", encoding="UTF16") as f:
        for line in f.readlines():
            if line.startswith("MMTEXTOUT( L\"RST_MUSICARTIST"):
                dataLinesArtist.append(line.replace("\n", ""))
            if line.startswith("MMTEXTOUT( L\"RST_MUSICTITLE"):
                dataLinesTrack.append(line.replace("\n", ""))
            if line.startswith("MMTEXTOUT( L\"RST_SCORECREATOR"):
                dataLinesDesigner.append(line.replace("\n", ""))

    for line in dataLinesArtist:
        splitDataLine = []
        id = line[line.find("ARTIST_") + 7:line.find("\" ,")]

        # Remove the mess from the beginning and the end of the line
        line = line[line.rfind("L\"") + 2:line.rfind("\" )")]
        splitDataLine.append(line)
        splitDataLine.append(id)
        dba.UpdateLineToTextOutJpArtist(conn, splitDataLine)

    for line in dataLinesTrack:
        splitDataLine = []
        id = line[line.find("TITLE_") + 6:line.find("\" ,")]

        # Remove the mess from the beginning and the end of the line
        line = line[line.rfind("L\"") + 2:line.rfind("\" )")]
        splitDataLine.append(line)
        splitDataLine.append(id)
        dba.UpdateLineToTextOutJpTrack(conn, splitDataLine)

    for line in dataLinesDesigner:
        splitDataLine = []
        id = line[line.find("CREATOR_") + 8:line.find("\" ,")]

        # Remove the mess from the beginning and the end of the line
        line = line[line.rfind("L\"") + 2:line.rfind("\" )")]
        splitDataLine.append(line)
        splitDataLine.append(id)
        dba.UpdateLineToTextOutJpDesigner(conn, splitDataLine)


def ReadSoundBgm(conn, path):
    dataLines = []

    if not os.path.isfile(path + r"/SoundBGM.txt"):
        print("Couldn't find SoundBGM.txt\nPlease decrypt the files before creating a database")
        return

    with open(path + r"/SoundBGM.txt", "r", encoding="UTF8") as f:
        for line in f.readlines():
            # if not line.startswith("TUTORIAL") and not line.startswith("OMAKASE") and line != "\n":
            if line != "\n":
                dataLines.append(line.replace("\n", ""))

    for line in dataLines:
        # SoundBGM has special bgm tracks on the top of the file that contains an extra comma at the end of the line
        # Also there's an extra space after the first comma <_<
        if line.startswith("TUTORIAL") or line.startswith("OMAKASE"):
            line = line[:-1]
            splitDataLine = line.split(", ")
        else:
            splitDataLine = line.split(",")

        dba.InsertLineToSoundBgm(conn, splitDataLine)
