import DatabaseActions as dba
import Helpers as hlp
import os

# These are configured to be used with files from maimai FiNALE version

def ReadMmMusic(conn, path):
    dataLines = []

    with open(path + r"/decrypted/mmMusic.txt", "r", encoding="UTF16") as f:
        for line in f.readlines():
            if line.startswith("MMMUSIC"):
                dataLines.append(line.replace("\n", "").replace("RST_MUSICTITLE_", "").replace("RST_MUSICARTIST_", ""))

    for line in dataLines:
        dba.InsertLineToMusic(conn, hlp.SplitMusicOrScoreLine(line))


def ReadMmMusicSingleLine(fileFullname, trackId):
    data = ""

    if os.path.isfile(fileFullname):
        with open(fileFullname, "r", encoding="UTF16") as f:
            for line in f.readlines():
                if line.startswith(f"MMMUSIC( {trackId},"):
                    data = line.replace("\n", "").replace("RST_MUSICTITLE_", "").replace("RST_MUSICARTIST_", "")
    else:
        print("File not found")
        return

    return hlp.SplitMusicOrScoreLine(data)


def ReadMmScore(conn, path):
    dataLines = []

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

    if os.path.isfile(fileFullname):
        with open(fileFullname, "r", encoding="UTF16") as f:
            for line in f.readlines():
                if f"eScore_{trackId}" in line:
                    dataLines.append(line.replace("\n", ""))
    else:
        print("File not found")
        return

    for line in dataLines:
        rows.append(hlp.SplitMusicOrScoreLine(line))

    return rows


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
