import os, sys
import TableFormat
import sqlite3 as sq
import Templates as tmpl
import Convert as cvrt
import MaiCrypt
from sqlite3 import Error
import DatabaseActions as dba
import Helpers as hlp


def CreateConnection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sq.connect(db_file)
        print(sq.sqlite_version)
        return conn
    except Error as e:
        print(e)
        sys.exit(1)


def CreateTable(conn, table):
    try:
        c = conn.cursor()
        c.execute(table)
    except Error as e:
        print(e)


def InitDb(conn):
    for table in TableFormat.Tables:
        CreateTable(conn, table)


def ReadMmMusic(conn, path):
    dataLines = []

    with open(path + r"\_software\Coco_ver0.0\decrypted_files\mmMusic", "r", encoding="UTF16") as f:
        for line in f.readlines():
            if line.startswith("MMMUSIC"):
                dataLines.append(line.replace("\n", "").replace("RST_MUSICTITLE_", "").replace("RST_MUSICARTIST_", ""))

    for line in dataLines:
        dba.InsertLineToMusic(conn, hlp.SplitMusicOrScoreLine(line))


def ReadMmScore(conn, path):
    dataLines = []

    with open(path + r"\_software\Coco_ver0.0\decrypted_files\mmScore", "r", encoding="UTF16") as f:
        for line in f.readlines():
            if line.startswith("MMSCORE"):
                dataLines.append(line.replace("\n", ""))

    for line in dataLines:
        dba.InsertLineToScore(conn, hlp.SplitMusicOrScoreLine(line))


def ReadTextOutEx(conn, path):
    dataLinesArtist = []
    dataLinesTrack = []

    with open(path + r"\_software\Coco_ver0.0\decrypted_files\mmtextout_ex", "r", encoding="UTF16") as f:
        for line in f.readlines():
            if line.startswith("MMTEXTOUT( L\"RST_MUSICARTIST"):
                dataLinesArtist.append(line.replace("\n", ""))
            if line.startswith("MMTEXTOUT( L\"RST_MUSICTITLE"):
                dataLinesTrack.append(line.replace("\n", ""))

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


def ReadTextOutJp(conn, path):
    dataLinesArtist = []
    dataLinesTrack = []

    with open(path + r"\_software\Coco_ver0.0\decrypted_files\mmtextout_jp", "r", encoding="UTF16") as f:
        for line in f.readlines():
            if line.startswith("MMTEXTOUT( L\"RST_MUSICARTIST"):
                dataLinesArtist.append(line.replace("\n", ""))
            if line.startswith("MMTEXTOUT( L\"RST_MUSICTITLE"):
                dataLinesTrack.append(line.replace("\n", ""))

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


def ReadSoundBgm(conn, path):
    dataLines = []

    with open(path + r"\maimai\data\SoundBGM.txt", "r", encoding="UTF8") as f:
        for line in f.readlines():
            if not line.startswith("TUTORIAL") and not line.startswith("OMAKASE") and line != "\n":
                dataLines.append(line.replace("\n", ""))

    for line in dataLines:
        splitDataLine = line.split(",")
        dba.InsertLineToSoundBgm(conn, splitDataLine)


def LoadFilesIntoDb(conn, path):
    ReadMmMusic(conn, path)
    ReadMmScore(conn, path)
    ReadTextOutEx(conn, path)
    ReadTextOutJp(conn, path)
    ReadSoundBgm(conn, path)


def GenerateMmMusicFromDb(conn):
    rows = dba.SelectMmMusic(conn)
    lines = []

    for row in rows:
        lines.append(GenerateMmMusicRow(row))

    return lines


def GenerateMmMusicRow(row):
    row = list(row)

    # Add affix to title and artist
    row[22] = f"RST_MUSICTITLE_{row[22]}"
    row[23] = f"RST_MUSICARTIST_{row[23]}"

    # Set row spacings
    row[0] = hlp.SetSpacing(row[0], 3)
    row[3] = hlp.SetSpacing(row[3], 2)
    row[4] = hlp.SetSpacing(row[4], 7)
    row[10] = hlp.SetSpacing(row[10], 8)
    row[12] = hlp.SetSpacing(row[12], 6)
    row[13] = hlp.SetSpacing(row[13], 6)
    row[14] = hlp.SetSpacing(row[14], 3)
    row[15] = hlp.SetSpacing(row[15], 2)
    row[16] = hlp.SetSpacing(row[16], 2)
    row[17] = hlp.SetSpacing(row[17], 8)
    row[24] = hlp.SetSpacing(row[24], 6)
    row[25] = hlp.SetSpacing(row[25], 6)

    # Calculate the space between filename and ) symbol
    lastRowSpacing = 25 - len(row[26]) - 2  # "" marks

    space = ""
    for i in range(lastRowSpacing):
        space += " "  # Add the proper amount of spacing

    completeLine = f"MMMUSIC( {row[0]}{row[1]}, {row[2]}, {row[3]}{row[4]}{row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9]}, {row[10]}{row[11]}, " \
           f"{row[12]}{row[13]}{row[14]}{row[15]}{row[16]}{row[17]}{row[18]}, {row[19]}, {row[20]}, {row[21]}, {row[22]}, {row[23]}, " \
           f"{row[24]}{row[25]}\"{row[26]}\"{space}) ///< {row[1].replace(' ', '').replace(',', '')}"

    # print(completeLine)

    """
    lines.append(
        f"MMMUSIC( {row[0]}{row[1]}, {row[2]}, {row[3]}{row[4]}{row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9]}, {row[10]}"
        f"{row[11]}, {row[12]}{row[13]}{row[14]}{row[15]}{row[16]}{row[17]}{row[18]}, {row[19]}, {row[20]}, {row[21]}, {row[22]}, "
        f"{row[23]}, {row[24]}{row[25]}\"{row[26]}\"{space}) ///< {row[1].replace(' ', '').replace(',', '')}\n")"""

    """ Without dynamic row adjustment
    print(
        f"MMMUSIC( {row[0]},   {row[1]}, {row[2]}, {row[3]}, {row[4]},     {row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9]}, {row[10]},        "
        f"{row[11]}, {row[12]},     {row[13]},     {row[14]},   {row[15]},  {row[16]},  {row[17]}, {row[18]}, {row[19]}, {row[20]}, {row[21]}, {row[22]}, "
        f"{row[23]}, {row[24]}, {row[25]}, \"{row[26]}\"{space}) ///< {row[1]}")"""

    return completeLine


def GenerateMmScoreFromDb(conn):
    rows = dba.SelectMmScore(conn)
    lines = []

    for row in rows:
        lines.append(GenerateMmScoreRow(row))

    return lines


def GenerateMmScoreRow(row):
    row = list(row)

    # Set row spacings
    row[0] = hlp.SetSpacing(row[0], 5)
    row[1] = hlp.SetSpacing(row[1], 36)
    row[2] = hlp.SetSpacing(row[2], 4)
    row[3] = hlp.SetSpacing(row[3], 2)

    # Calculate the space between filename and ) symbol
    lastRowSpacing = 32 - len(row[5]) - 2  # "" marks

    space = ""
    for i in range(lastRowSpacing):
        space += " "  # Add the proper amount of spacing

    # print( f"MMSCORE( {row[0]}{row[1]}{row[2]}{row[3]}{row[4]}, \"{row[5]}\"{space}) ///< {row[1].replace(' ',
    # '').replace(',', '')}")

    return f"MMSCORE( {row[0]}{row[1]}{row[2]}{row[3]}{row[4]}, \"{row[5]}\"{space}) ///< {row[1].replace(' ', '').replace(',', '')}"


def GenerateMmTextoutExFromDb(conn):
    artists = []
    tracks = []

    rows = dba.SelectMmTextoutArtist(conn)

    for row in rows:
        artists.append(f"MMTEXTOUT( L\"RST_MUSICARTIST_{row[0]}\" ,L\"{row[1]}\" )")

    rows = dba.SelectMmTextoutTrack(conn)

    for row in rows:
        tracks.append(f"MMTEXTOUT( L\"RST_MUSICTITLE_{row[0]}\" ,L\"{row[1]}\" )")

    return artists + tracks


def GenerateMmTextoutJpFromDb(conn):
    artists = []
    tracks = []

    rows = dba.SelectMmTextoutArtist(conn)

    for row in rows:
        artists.append(f"MMTEXTOUT( L\"RST_MUSICARTIST_{row[0]}\" ,L\"{row[2]}\" )")

    rows = dba.SelectMmTextoutTrack(conn)

    for row in rows:
        tracks.append(f"MMTEXTOUT( L\"RST_MUSICTITLE_{row[0]}\" ,L\"{row[2]}\" )")

    return artists + tracks

def GenerateSoundBgmFromDb(conn):
    rows = dba.SelectSoundBgm(conn)
    lines = []

    for row in rows:
        # print(f"{row[0]},{row[1]}")
        lines.append(f"{row[0]},{row[1]}")

    return lines


def EncryptFilesInOutput():
    with open(f"{os.getcwd()}/key.txt", "r") as f:
        key = f.readline()

    crypt = MaiCrypt.MaiFinaleCrypt(key)

    if not os.path.isdir(f"{os.getcwd()}/output/encrypted"):
        os.mkdir(f"{os.getcwd()}/output/encrypted")

    for file in os.listdir(f"{os.getcwd()}/output"):
        if file != "SoundBGM.txt" and not os.path.isdir(f"{os.getcwd()}/output/{file}"):
            print(f"{os.getcwd()}/output/{file}")
            cipher_text = crypt.convert_to_bin(f"{os.getcwd()}/output/{file}")
            with open(f"{os.getcwd()}/output/encrypted/{file.replace('.txt', '')}", "wb") as f:
                f.write(cipher_text)


if __name__ == '__main__':

    db = f"{os.getcwd()}/test.db"
    conn = CreateConnection(db)
    InitDb(conn)

    path = r"L:\Games\SDEY_1.99"
    LoadFilesIntoDb(conn, path)
    # GenerateMmMusicFromDb(conn)
    # GenerateMmScoreFromDb(conn)
    # GenerateMmTextoutExFromDb(conn)
    # GenerateMmTextoutJpFromDb(conn)
    # GenerateSoundBgmFromDb(conn)

    # dba.InsertLineToMusic(conn, cvrt.ConvertMmMusicLineFromGreentoFinale(340))
    # dba.InsertLineToScore(conn, cvrt.ConvertMmScoreLineFromGreentoFinale(34001))
    # dba.InsertLineToSoundBgm(conn, cvrt.ConvertSoundBgmLineFromGreentoFinale(164))
    # dba.InsertLineToTextOutArtist(conn, cvrt.ConvertMmTextOutArtistFromGreenToFinale(20))
    # dba.InsertLineToTextOutArtist(conn, cvrt.ConvertMmTextOutArtistFromGreenToFinale(20))

    tmpl.CreateMmMusicFromTemplate(GenerateMmMusicFromDb(conn))
    tmpl.CreateMmScoreFromTemplate(GenerateMmScoreFromDb(conn))
    tmpl.CreateSoundBgmFromTemplate(GenerateSoundBgmFromDb(conn))
    tmpl.CreateMmTextOutEx(GenerateMmTextoutExFromDb(conn))
    tmpl.CreateMmTextOutJp(GenerateMmTextoutJpFromDb(conn))
    EncryptFilesInOutput()

    # dba.InsertLineToTextOutExTrack(conn, ["0020", "love circulation"])
    # dba.UpdateLineToTextOutJpTrack(conn, ["恋愛サーキュレーション", "0020"])

