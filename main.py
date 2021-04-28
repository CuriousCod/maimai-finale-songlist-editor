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
import configparser
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

        self.config = configparser.ConfigParser()

        if not os.path.isfile(os.getcwd() + "\\config.ini"):
            with open(os.getcwd() + "\\config.ini", "w"):
                pass
        self.config.read(os.getcwd() + "\\config.ini")

    def DisplayData(self, sender, data):
        # Callbacks run on a separate thread, sqlite doesn't like that
        tempConn = CreateConnection(db)
        if data == "mmMusic":
            lines = dba.SelectMmMusic(tempConn)
            simple.show_item("window_mmMusicDisplay")
            core.clear_table("table_mmMusic")
            for line in lines:
                core.add_row("table_mmMusic", line)

        elif data == "mmScore":
            lines = dba.SelectMmScore(tempConn)
            simple.show_item("window_mmScoreDisplay")
            core.clear_table("table_mmScore")
            for line in lines:
                core.add_row("table_mmScore", line)

        elif data == "artist":
            lines = dba.SelectMmTextoutArtist(tempConn)
            simple.show_item("window_textoutArtistDisplay")
            core.clear_table("table_textoutArtist")
            for line in lines:
                core.add_row("table_textoutArtist", line)

        elif data == "track":
            lines = dba.SelectMmTextoutTrack(tempConn)
            simple.show_item("window_textoutTrackDisplay")
            core.clear_table("table_textoutTrack")
            for line in lines:
                core.add_row("table_textoutTrack", line)

        elif data == "designer":
            lines = dba.SelectMmTextoutDesigner(tempConn)
            simple.show_item("window_textoutDesignerDisplay")
            core.clear_table("table_textoutDesigner")
            for line in lines:
                core.add_row("table_textoutDesigner", line)

        elif data == "soundBgm":
            lines = dba.SelectSoundBgm(tempConn)
            simple.show_item("window_soundBgmDisplay")
            core.clear_table("table_soundBgm")
            for line in lines:
                core.add_row("table_soundBgm", line)

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

        with simple.window("window_selectMaimaiFiles", label="Select maimai files", y_pos=400):
            core.add_button("button_selectMaimaiFolder", label="Select maimai folder", callback=self.SelectMaimaiFolder)
            core.add_input_text("files_input_mmMusic")
            core.add_input_text("files_input_mmScore")
            core.add_input_text("files_input_mmTextoutEx")
            core.add_input_text("files_input_mmTextoutJp")
            core.add_input_text("files_input_soundBgm")
            core.add_button("files_button_decryptFiles", label="Decrypt Files", callback=DecryptFilesInInput)
            core.add_button("files_button_loadFilesIntoDatabase", label="Load Files Into Database", callback=lambda:LoadFilesIntoDb(f"{os.getcwd()}/input"))

        with simple.window("Browse Db"):
            core.add_text("Browse current data")
            core.add_button("browse_button_displayMmMusic", label="mmMusic", callback=self.DisplayData, callback_data="mmMusic")
            core.add_button("browse_button_displayMmScore", label="mmScore", callback=self.DisplayData, callback_data="mmScore")
            core.add_button("browse_button_displayArtist", label="Artist", callback=self.DisplayData, callback_data="artist")
            core.add_button("browse_button_displayTrack", label="Track", callback=self.DisplayData, callback_data="track")
            core.add_button("browse_button_displayDesigner", label="Designer", callback=self.DisplayData, callback_data="designer")
            core.add_button("browse_button_displaySoundBgm", label="Sound BGM", callback=self.DisplayData, callback_data="soundBgm")

        with simple.window("window_editMaimaiData", label="Edit maimai data"):
            with simple.tab_bar("Data Types"):
                with simple.tab("Artist"):
                    core.add_text("Artist")
                    core.add_input_int("dataArtist_input_addArtistId", label="Artist ID", max_value=9999, min_value=0, step_fast=100)
                    core.add_input_text("dataArtist_input_addArtistEx", label="Ex Artist")
                    core.add_input_text("dataArtist_input_addArtistJp", label="Jp Artist")
                    core.add_button("dataArtist_button_addArtistToDb", label="Add artist to database", callback=self.InsertDataToDb, callback_data="InsertArtist")
                    core.add_same_line()
                    core.add_button("dataArtist_button_getArtistFromDb", label="Get artist from database", callback=self.GetDataFromDb, callback_data="GetArtist")
                with simple.tab("Track Name"):
                    core.add_text("Track Name")
                    core.add_input_int("dataTrack_input_addTrackId", label="Track ID", max_value=9999, min_value=0, step_fast=100)
                    core.add_input_text("dataTrack_input_addTrackEx", label="Ex Track")
                    core.add_input_text("dataTrack_input_addTrackJp", label="Jp Track")
                    core.add_button("dataTrack_button_addTrackNameToDb", label="Add track name to database", callback=self.InsertDataToDb, callback_data="InsertTrackName")
                    core.add_same_line()
                    core.add_button("dataTrack_button_getTrackNameFromDb", label="Get track from database", callback=self.GetDataFromDb, callback_data="GetTrackName")
                with simple.tab("Designer Name"):
                    core.add_text("Designer Name")
                    core.add_input_int("dataDesigner_input_addDesignerId", label="Designer ID", max_value=99, min_value=0, step_fast=10)
                    core.add_input_text("dataDesigner_input_addDesignerEx", label="Ex Designer")
                    core.add_input_text("dataDesigner_input_addDesignerJp", label="Jp Designer")
                    core.add_button("dataDesigner_button_addDesignerToDb", label="Add designer to database", callback=self.InsertDataToDb, callback_data="InsertDesignerName")
                    core.add_same_line()
                    core.add_button("dataDesigner_button_getDesignerFromDb", label="Get designer from database", callback=self.GetDataFromDb, callback_data="GetDesignerName")
                # TODO add tips
                with simple.tab("mmMusic"):
                    core.add_input_int("dataMmMusic_input_addTrackId", label="Track ID", max_value=999, min_value=0, step_fast=100)
                    # name
                    core.add_input_int("dataMmMusic_input_addVersion", label="Version", max_value=99999, min_value=0, step_fast=1000, default_value=10000)
                    # subcate -> 30
                    core.add_input_float("dataMmMusic_input_addBpm", label="Bpm", max_value=999.99, format="%.2f", min_value=0, step=1.0, step_fast=10.0)
                    core.add_input_int("dataMmMusic_input_addSortId", label="Sort Id", max_value=999999, min_value=0, step=10, step_fast=1000, default_value=300000)
                    # dress -> 0
                    # darkness -> 0
                    # mile -> 0
                    core.add_checkbox("dataMmMusic_checkbox_addHasVideo", label="Track has video file")
                    # event -> 0
                    # rec -> 1
                    core.add_input_float("dataMmMusic_input_addPvStart", label="PV Start", max_value=999.99, step_fast=10.0, step=1.0, format="%.2f")
                    core.add_input_float("dataMmMusic_input_addPvEnd", label="PV End", max_value=999.99, step_fast=10.0, step=1.0, format="%.2f")
                    # song duration -> 0
                    # off_rank -> 0
                    # ad_def -> 0
                    core.add_checkbox("dataMmMusic_checkbox_addHasRemaster", label="Track has remaster difficulty")
                    # special_pv -> 0
                    # challenge_track -> 0
                    # bonus -> 0
                    core.add_combo("dataMmMusic_combo_genreId", items=["Pops & Anime", "niconico & Vocaloid", "Touhou Project", "Sega", "Game & Variety", "Original & Joypolis"])
                    core.add_input_int("dataMmMusic_input_addTitleId", label="Title Id", max_value=9999, min_value=0, step_fast=100)
                    core.add_input_int("dataMmMusic_input_addArtistId", label="Artist Id", max_value=9999, min_value=0, step_fast=100)
                    core.add_input_int("dataMmMusic_input_addSortJpIndex", label="Sort Index JP", max_value=999999, min_value=0, step_fast=10000, step=1)
                    core.add_input_int("dataMmMusic_input_addSortExIndex", label="Sort Index EX", max_value=999999, min_value=0, step_fast=10000, step=1)
                    core.add_input_text("dataMmMusic_input_addFilename", label="Filename")
                    core.add_button("dataMmMusic_button_addTrackToDb", label="Add track to database", callback=self.InsertDataToDb, callback_data="")
                    core.add_same_line()
                    core.add_button("dataMmMusic_button_getTrackFromDb", label="Get track from database", callback=self.GetDataFromDb, callback_data="")
                with simple.tab("mmScore"):
                    core.add_input_int("dataMmScore_input_addTrackId", label="Track ID", max_value=999, min_value=0, step_fast=100)
                    # name
                    core.add_input_float("dataMmScore_input_addDifficulty", label="Difficulty", max_value=99.9, format="%.1f", min_value=0, step=0.1, step_fast=1.0)
                    core.add_input_int("dataMmScore_input_addDesignerId", label="Score Designer Id", max_value=99, min_value=0, step_fast=10)
                    core.add_checkbox("dataMmScore_checkbox_addIsInUtage", label="Included in Utage")
                    core.add_input_text("dataMmScore_input_addSafename", label="Score Filename")
                    core.add_button("dataMmScore_button_addScoreToDb", label="Add score to database", callback=self.InsertDataToDb, callback_data="")
                    core.add_same_line()
                    core.add_button("dataMmScore_button_getScoreFromDb", label="Get score from database", callback=self.GetDataFromDb, callback_data="")
                with simple.tab("Sound BGM"):
                    core.add_input_int("dataSoundBgm_input_addTrackId", label="Track ID", max_value=999, min_value=0, step_fast=100)
                    core.add_input_text("dataSoundBgm_input_addTitle", label="Track Filename")
                    core.add_button("dataSoundBgm_button_addSoundBgmToDB", label="Add sound bgm to database", callback=self.InsertDataToDb, callback_data="")
                    core.add_same_line()
                    core.add_button("dataMmScore_button_getSoundBgmToDB", label="Get sound bgm from database", callback=self.GetDataFromDb, callback_data="")
                core.add_checkbox("data_checkbox_replaceDbEntry", label="Overwrite Previous Db Entry")

        with simple.window("window_generateMaimaiFiles", label="Generate maimai Files", x_pos=400):
            core.add_text("Generate data files for maimai FiNALE")
            core.add_button("generate_button_createFiles", label="Generate Files", callback=GenerateFilesFromDb(self.conn))
            core.add_same_line()
            core.add_button("generate_button_encryptFiles", label="Encrypt Files", callback=EncryptFilesInOutput)
            core.add_spacing(count=4)
            core.add_button("generate_button_openOutputFolder", label="Open Output Folder", callback=lambda: os.startfile(f"{os.getcwd()}/output"))

        with simple.window("window_mmMusicDisplay", label="mmMusic Grid", show=False):
            columns = ["track_id", "name", "ver", "subcate", "bpm", "sort_id", "dress", "darkness", "mile", "vl",
                       "event", "rec", "pvstart", "pvend", "song_duration", "off_ranking", "ad_def", "remaster",
                       "special_pv", "challenge_track", "bonus", "genre_id", "title", "artist", "sort_jp_index",
                       "sort_ex_index", "filename"]
            core.add_table("table_mmMusic", columns, height=0, width=0)

        with simple.window("window_mmScoreDisplay", label="mmScore Grid", show=False):
            columns = ["track_id", "name", "lv", "designer_id", "utage_mode", "safename"]
            core.add_table("table_mmScore", columns, height=0, width=0)

        with simple.window("window_textoutArtistDisplay", label="Artist Name Grid", show=False):
            columns = ["artist_id", "ex_artist_title", "jp_artist_title"]
            core.add_table("table_textoutArtist", columns, height=0, width=0)

        with simple.window("window_textoutTrackDisplay", label="Track Name Grid", show=False):
            columns = ["track_id", "ex_track_title", "jp_track_title"]
            core.add_table("table_textoutTrack", columns, height=0, width=0)

        with simple.window("window_textoutDesignerDisplay", label="Track Designer Grid", show=False):
            columns = ["designer_id", "ex_designer_name", "jp_designer_name"]
            core.add_table("table_textoutDesigner", columns, height=0, width=0)

        with simple.window("window_soundBgmDisplay", label="Sound BGM Grid", show=False):
            columns = ["title", "track_id"]
            core.add_table("table_soundBgm", columns, height=0, width=0)

        with simple.window("window_log", label="Log"):
            core.add_input_text("log_input_log", label="", multiline=True, readonly=True, width=600, height=1200)
            core.add_same_line()
            core.add_button("log_button_clearLog", label="Clear", callback=lambda: core.set_value("log_input_log", ""))

        core.enable_docking(dock_space=True)
        core.set_start_callback(self.OnStart)
        core.set_render_callback(self.MainCallback)
        core.set_exit_callback(self.OnExit)
        core.start_dearpygui()

    def InsertDataToDb(self, sender, data):
        if data == "InsertArtist":
            tempConn = CreateConnection(db)
            artistId = hlp.AffixZeroesToString(core.get_value("dataArtist_input_addArtistId"), 4)
            artistEx = core.get_value("dataArtist_input_addArtistEx")
            artistJp = core.get_value("dataArtist_input_addArtistJp")

            if artistId == "":
                return

            if not (dba.InsertLineToTextOutArtist(tempConn, [artistId, artistEx, artistJp])):
                if core.get_value("data_checkbox_replaceDbEntry"):
                    dba.ReplaceLineInTextOutArtist(tempConn, [artistId, artistEx, artistJp])
                    self.AppendLog("Entry replaced")
                else:
                    self.AppendLog("Entry already exists")
            else:
                self.AppendLog("Entry added")

        elif data == "InsertTrackName":
            tempConn = CreateConnection(db)
            trackId = hlp.AffixZeroesToString(core.get_value("dataTrack_input_addTrackId"), 4)
            trackEx = core.get_value("dataTrack_input_addTrackEx")
            trackJp = core.get_value("dataTrack_input_addTrackJp")

            if trackId == "":
                return

            if not (dba.InsertLineToTextOutTrack(tempConn, [trackId, trackEx, trackJp])):
                if core.get_value("data_checkbox_replaceDbEntry"):
                    dba.ReplaceLineInTextOutTrack(tempConn, [trackId, trackEx, trackJp])
                    self.AppendLog("Entry replaced")
                else:
                    self.AppendLog("Entry already exists")
            else:
                self.AppendLog("Entry added")

        elif data == "InsertDesignerName":
            self.AppendLog("wip")

        else:
            self.AppendLog("wip")

    def GetDataFromDb(self, sender, data):
        if data == "GetArtist":
            tempConn = CreateConnection(db)
            artistId = hlp.AffixZeroesToString(core.get_value("dataArtist_input_addArtistId"), 4)
            row = dba.SelectMmTextoutArtistById(tempConn, artistId)

            if len(row) > 0:
                row = row[0]
                core.set_value("dataArtist_input_addArtistEx", row[0])
                core.set_value("dataArtist_input_addArtistJp", row[1])
            else:
                core.set_value("dataArtist_input_addArtistEx", "")
                core.set_value("dataArtist_input_addArtistJp", "")
        elif data == "GetTrackName":
            tempConn = CreateConnection(db)
            trackId = hlp.AffixZeroesToString(core.get_value("dataTrack_input_addTrackId"), 4)
            row = dba.SelectMmTextoutTrackById(tempConn, trackId)

            if len(row) > 0:
                row = row[0]
                core.set_value("dataTrack_input_addTrackEx", row[0])
                core.set_value("dataTrack_input_addTrackJp", row[1])
            else:
                core.set_value("dataTrack_input_addTrackEx", "")
                core.set_value("dataTrack_input_addTrackJp", "")
        elif data == "GetDesignerName":
            self.AppendLog("wip")
        else:
            self.AppendLog("wip")

    def AppendLog(self, text):
        core.set_value("log_input_log", f"{core.get_value('log_input_log')}{datetime.datetime.now().strftime('%H:%M:%S')} - {text}\n")

    def MainCallback(self):
        simple.set_item_width("log_input_log", simple.get_drawing_size("window_log")[0] - 100)
        simple.set_item_height("log_input_log", simple.get_drawing_size("window_log")[1] - 35)

    def OnStart(self):
        self.load_layout(self.GetCurrentWindowNames())

    def OnExit(self):
        self.save_layout(self.GetCurrentWindowNames())

    def save_layout(self, windows):
        with open(os.getcwd() + "\\config.ini", "r+") as f:
            self.config["Layout"] = {}
            for window in windows:
                self.config["Layout"][window + "_posX"] = str(simple.get_window_pos(window)[0])
                self.config["Layout"][window + "_posY"] = str(simple.get_window_pos(window)[1])
                self.config["Layout"][window + "_sizeX"] = str(simple.get_drawing_size(window)[0])
                self.config["Layout"][window + "_sizeY"] = str(simple.get_drawing_size(window)[1])
            self.config.write(f)

    def load_layout(self, windows):
        if self.config.has_section("Layout"):
            for window in windows:
                try:
                    simple.set_window_pos(window, int(self.config["Layout"][window + "_posX"]),
                                          int(self.config["Layout"][window + "_posY"]))
                    simple.set_drawing_size(window, int(self.config["Layout"][window + "_sizeX"]),
                                                        int(self.config["Layout"][window + "_sizeY"]))
                except KeyError as e:
                    print(f"KeyError: {e}")

    def GetCurrentWindowNames(self):
        windows = core.get_windows()
        for i in range(6):
            # TODO This should be handled better
            # Remove dearpygui's default windows from list
            windows.pop(-1)

        return windows


if __name__ == '__main__':
    db = f"{os.getcwd()}/test.db"
    conn = CreateConnection(db)
    InitDb(conn)

    # path = r"L:\Games\SDEY_1.99"
    path = f"{os.getcwd()}/input"
    LoadFilesIntoDb(path)

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
