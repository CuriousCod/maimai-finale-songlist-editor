import DatabaseActions as dba
import Helpers as hlp


def ReadMmMusic(conn, path):
    dataLines = []

    with open(path + r"/decrypted/mmMusic.txt", "r", encoding="UTF16") as f:
        for line in f.readlines():
            if line.startswith("MMMUSIC"):
                dataLines.append(line.replace("\n", "").replace("RST_MUSICTITLE_", "").replace("RST_MUSICARTIST_", ""))

    for line in dataLines:
        dba.InsertLineToMusic(conn, hlp.SplitMusicOrScoreLine(line))


def ReadMmScore(conn, path):
    dataLines = []

    with open(path + r"/decrypted/mmScore.txt", "r", encoding="UTF16") as f:
        for line in f.readlines():
            if line.startswith("MMSCORE"):
                dataLines.append(line.replace("\n", ""))

    for line in dataLines:
        dba.InsertLineToScore(conn, hlp.SplitMusicOrScoreLine(line))

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
            if not line.startswith("TUTORIAL") and not line.startswith("OMAKASE") and line != "\n":
                dataLines.append(line.replace("\n", ""))

    for line in dataLines:
        splitDataLine = line.split(",")
        dba.InsertLineToSoundBgm(conn, splitDataLine)
