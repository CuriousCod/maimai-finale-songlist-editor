import os, sys
import DatabaseFormat
import sqlite3 as sq
import datetime
import Templates as tmpl
import Convert as cvrt
import ReadData as readDat
import GenerateData as genDat
import MaiCrypt
import tkinter
import shutil
from tkinter import filedialog
from sqlite3 import Error
import DatabaseActions as dba
import Helpers as hlp
from dearpygui import core, simple


def CreateConnection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sq.connect(db_file)
        # print(sq.sqlite_version)
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
    for table in DatabaseFormat.Tables:
        CreateTable(conn, table)


def LoadFilesIntoDb(path):
    conn = CreateConnection(db)

    readDat.ReadMmMusic(conn, path)
    readDat.ReadMmScore(conn, path)
    readDat.ReadTextOutEx(conn, path)
    readDat.ReadTextOutJp(conn, path)
    readDat.ReadSoundBgm(conn, path)

    conn.close()


def GenerateFilesFromDb(conn):
    tmpl.CreateMmMusicFromTemplate(genDat.GenerateMmMusicFromDb(conn))
    tmpl.CreateMmScoreFromTemplate(genDat.GenerateMmScoreFromDb(conn))
    tmpl.CreateSoundBgmFromTemplate(genDat.GenerateSoundBgmFromDb(conn))
    tmpl.CreateMmTextOutEx(genDat.GenerateMmTextoutExFromDb(conn))
    tmpl.CreateMmTextOutJp(genDat.GenerateMmTextoutJpFromDb(conn))


def DecryptFilesInInput():
    with open(f"{os.getcwd()}/key.txt", "r") as f:
        key = f.readline()

    crypt = MaiCrypt.MaiFinaleCrypt(key)

    if not os.path.isdir(f"{os.getcwd()}/input/decrypted"):
        os.mkdir(f"{os.getcwd()}/input/decrypted")

    for file in os.listdir(f"{os.getcwd()}/input"):
        if file != "SoundBGM.txt" and not os.path.isdir(f"{os.getcwd()}/input/{file}"):
            # print(f"{os.getcwd()}/input/{file}")
            plain_text = crypt.convert_to_text(f"{os.getcwd()}/input/{file}")
            with open(f"{os.getcwd()}/input/decrypted/{file.replace('.bin', '')}.txt", "wb") as f:
                f.write(plain_text)


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
            with open(f"{os.getcwd()}/output/encrypted/{file.replace('.txt', '')}.bin", "wb") as f:
                f.write(cipher_text)


class GUI:
    def __init__(self):
        self.conn = CreateConnection(db)

    def DisplayData(self, sender, data):
        # Callbacks run on a separate thread, sqlite doesn't like that
        tempConn = CreateConnection(db)
        if data == "mmMusic":
            lines = dba.SelectMmMusic(tempConn)
            simple.show_item("mmMusicDisplay")
            core.clear_table("mmMusicTable")
            for line in lines:
                core.add_row("mmMusicTable", line)

        elif data == "mmScore":
            lines = dba.SelectMmScore(tempConn)
            simple.show_item("mmScoreDisplay")
            core.clear_table("mmScoreTable")
            for line in lines:
                core.add_row("mmScoreTable", line)
        else:
            pass

        tempConn.close()

    def SelectMaimaiFolder(self):
        root = tkinter.Tk()
        root.withdraw()
        folder = filedialog.askdirectory(title="Select maimai folder")

        if not os.path.isdir(f"{os.getcwd()}/input"):
            os.mkdir(f"{os.getcwd()}/input")

        if folder[folder.rfind("/") + 1:] == "maimai":
            if os.path.isfile(f"{folder}/data/SoundBGM.txt"):
                core.set_value("input_soundBgm", f"{folder}/data/SoundBGM.txt")
                shutil.copy(f"{folder}/data/SoundBGM.txt", f"{os.getcwd()}/input/SoundBGM.txt")
            if os.path.isfile(f"{folder}/data/tables/mmMusic.bin"):
                core.set_value("input_mmMusic", f"{folder}/data/tables/mmMusic.bin")
                shutil.copy(f"{folder}/data/tables/mmMusic.bin", f"{os.getcwd()}/input/mmMusic.bin")
            if os.path.isfile(f"{folder}/data/tables/mmScore.bin"):
                core.set_value("input_mmScore", f"{folder}/data/tables/mmScore.bin")
                shutil.copy(f"{folder}/data/tables/mmScore.bin", f"{os.getcwd()}/input/mmScore.bin")
            if os.path.isfile(f"{folder}/data/tables/mmtextout_ex.bin"):
                core.set_value("input_mmTextoutEx", f"{folder}/data/tables/mmtextout_ex.bin")
                shutil.copy(f"{folder}/data/tables/mmtextout_ex.bin", f"{os.getcwd()}/input/mmtextout_ex.bin")
            if os.path.isfile(f"{folder}/data/tables/mmtextout_jp.bin"):
                core.set_value("input_mmTextoutJp", f"{folder}/data/tables/mmtextout_jp.bin")
                shutil.copy(f"{folder}/data/tables/mmtextout_jp.bin", f"{os.getcwd()}/input/mmtextout_jp.bin")

    def ActivateDisplay(self):
        with simple.window("window_selectMaimaiFiles", label="Select maimai Files", y_pos=400):
            core.add_button("button_selectMaimaiFolder", label="Select maimai folder", callback=self.SelectMaimaiFolder)
            core.add_input_text("input_mmMusic")
            core.add_input_text("input_mmScore")
            core.add_input_text("input_mmTextoutEx")
            core.add_input_text("input_mmTextoutJp")
            core.add_input_text("input_soundBgm")
            core.add_button("button_decryptFiles", label="Decrypt Files", callback=DecryptFilesInInput)
            core.add_button("button_loadFilesIntoDatabase", label="Load Files Into Database", callback=lambda:LoadFilesIntoDb(f"{os.getcwd()}/input"))

        with simple.window("Browse Db"):
            core.add_text("Browse current data")
            core.add_button("button_displayMmMusic", label="mmMusic", callback=self.DisplayData, callback_data="mmMusic")
            core.add_button("button_displayMmScore", label="mmScore", callback=self.DisplayData, callback_data="mmScore")

        with simple.window("window_adjustMaimaiData", label="Adjust maimai song data"):
            with simple.tab_bar("Data Types"):
                with simple.tab("Artist"):
                    core.add_text("Artist")
                    core.add_input_text("input_addArtistId", label="Artist ID")
                    core.add_input_text("input_addArtistEx", label="Ex Artist")
                    core.add_input_text("input_addArtistJp", label="Jp Artist")
                    core.add_button("button_addArtistToDb", label="Add artist to database", callback=self.InsertDataToDb, callback_data="InsertArtist")
                    core.add_same_line()
                    core.add_button("button_getArtistFromDb", label="Get artist from database", callback=self.GetDataFromDb, callback_data="GetArtist")
                with simple.tab("Track Name"):
                    core.add_text("Track Name")
                    core.add_input_text("input_addTrackId", label="Track ID")
                    core.add_input_text("input_addTrackEx", label="Ex Track")
                    core.add_input_text("input_addTrackJp", label="Jp Track")
                    core.add_button("button_addTrackNameToDb", label="Add track name to database", callback=self.InsertDataToDb, callback_data="InsertTrackName")
                    core.add_same_line()
                    core.add_button("button_getTrackNameFromDb", label="Get track from database", callback=self.GetDataFromDb, callback_data="GetTrackName")
                core.add_checkbox("checkbox_replaceDbEntry", label="Overwrite Previous Db Entry")

        with simple.window("window_generateMaimaiFiles", label="Generate maimai Files", x_pos=400):
            core.add_text("Create files for FiNALE")
            core.add_button("button_createFiles", label="Generate Files", callback=GenerateFilesFromDb(self.conn))
            core.add_button("button_encryptFiles", label="Encrypt Files", callback=EncryptFilesInOutput)

        with simple.window("window_mmMusicDisplay", label="mmMusic Grid", show=False):
            columns = ["track_id", "name", "ver", "subcate", "bpm", "sort_id", "dress", "darkness", "mile", "vl",
                       "event", "rec", "pvstart", "pvend", "song_duration", "off_ranking", "ad_def", "remaster",
                       "special_pv", "challenge_track", "bonus", "genre_id", "title", "artist", "sort_jp_index",
                       "sort_ex_index", "filename"]
            core.add_table("mmMusicTable", columns, height=800)

        with simple.window("window_mmScoreDisplay", label="mmScore Grid", show=False):
            columns = ["track_id", "name", "lv", "score_id", "utage_mode", "safename"]
            core.add_table("mmScoreTable", columns, height=800)

        with simple.window("window_log", label="Log"):
            core.add_input_text("input_log", label="", multiline=True, readonly=True, width=600, height=1200)
            core.add_same_line()
            core.add_button("button_clearLog", label="Clear", callback=lambda: core.set_value("input_log", ""))

        core.enable_docking(dock_space=True)
        core.start_dearpygui()

    def InsertDataToDb(self, sender, data):
        if data == "InsertArtist":
            tempConn = CreateConnection(db)
            artistId = hlp.AffixZeroesToString(core.get_value("input_addArtistId"), 4)
            artistEx = core.get_value("input_addArtistEx")
            artistJp = core.get_value("input_addArtistJp")

            if artistId == "":
                return

            if not (dba.InsertLineToTextOutArtist(tempConn, [artistId, artistEx, artistJp])):
                if core.get_value("checkbox_replaceDbEntry"):
                    dba.ReplaceLineInTextOutArtist(tempConn, [artistId, artistEx, artistJp])
                    self.AppendLog("Entry replaced")
                else:
                    self.AppendLog("Entry already exists")
            else:
                self.AppendLog("Entry added")

        if data == "InsertTrackName":
            tempConn = CreateConnection(db)
            trackId = hlp.AffixZeroesToString(core.get_value("input_addTrackId"), 4)
            trackEx = core.get_value("input_addTrackEx")
            trackJp = core.get_value("input_addTrackJp")

            if trackId == "":
                return

            if not (dba.InsertLineToTextOutTrack(tempConn, [trackId, trackEx, trackJp])):
                if core.get_value("checkbox_replaceDbEntry"):
                    dba.ReplaceLineInTextOutTrack(tempConn, [trackId, trackEx, trackJp])
                    self.AppendLog("Entry replaced")
                else:
                    self.AppendLog("Entry already exists")
            else:
                self.AppendLog("Entry added")

    def GetDataFromDb(self, sender, data):
        if data == "GetArtist":
            tempConn = CreateConnection(db)
            artistId = hlp.AffixZeroesToString(core.get_value("input_addArtistId"), 4)
            row = dba.SelectMmTextoutArtistById(tempConn, artistId)

            if len(row) > 0:
                row = row[0]
                core.set_value("input_addArtistEx", row[0])
                core.set_value("input_addArtistJp", row[1])
            else:
                core.set_value("input_addArtistEx", "")
                core.set_value("input_addArtistJp", "")
        if data == "GetTrackName":
            tempConn = CreateConnection(db)
            trackId = hlp.AffixZeroesToString(core.get_value("input_addTrackId"), 4)
            row = dba.SelectMmTextoutTrackById(tempConn, trackId)

            if len(row) > 0:
                row = row[0]
                core.set_value("input_addTrackEx", row[0])
                core.set_value("input_addTrackJp", row[1])
            else:
                core.set_value("input_addTrackEx", "")
                core.set_value("input_addTrackJp", "")

    def AppendLog(self, text):
        core.set_value("input_log", f"{core.get_value('input_log')}{datetime.datetime.now().strftime('%H:%M:%S')} - {text}\n")


if __name__ == '__main__':
    db = f"{os.getcwd()}/test.db"
    conn = CreateConnection(db)
    InitDb(conn)

    # path = r"L:\Games\SDEY_1.99"
    # LoadFilesIntoDb(conn, path)

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

    """
    tmpl.CreateMmMusicFromTemplate(GenerateMmMusicFromDb(conn))
    tmpl.CreateMmScoreFromTemplate(GenerateMmScoreFromDb(conn))
    tmpl.CreateSoundBgmFromTemplate(GenerateSoundBgmFromDb(conn))
    tmpl.CreateMmTextOutEx(GenerateMmTextoutExFromDb(conn))
    tmpl.CreateMmTextOutJp(GenerateMmTextoutJpFromDb(conn))
    EncryptFilesInOutput()
    """

    # dba.InsertLineToTextOutExTrack(conn, ["0020", "love circulation"])
    # dba.UpdateLineToTextOutJpTrack(conn, ["恋愛サーキュレーション", "0020"])
    conn.close()
    GUI().ActivateDisplay()
