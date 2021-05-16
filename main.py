import os, sys
import DatabaseFormat
import sqlite3 as sq
import datetime
import Templates as tmpl
import Convert as cvrt
import ReadData as readDat
import GenerateData as genDat
import DearGui as dg
import MaiCrypt
import tkinter
import shutil
import configparser
from tkinter import filedialog
from sqlite3 import Error
import DatabaseActions as dba
import Helpers as hlp
from dearpygui import core, simple


# TODO Include the tutorial values in SoundBGM.txt
# TODO Include maimai filepaths in config
# TODO Display all ids without data
# TODO Function to check all data connections for an id
# TODO Import all required data from other maimai versions based on mmusic id


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


def LoadFilesIntoDb(path, db):
    conn = CreateConnection(db)

    readDat.ReadMmMusic(conn, path)
    readDat.ReadMmScore(conn, path)
    readDat.ReadTextOutEx(conn, path)
    readDat.ReadTextOutJp(conn, path)
    readDat.ReadSoundBgm(conn, path)

    conn.close()


def GenerateFilesFromDb(db):
    conn = CreateConnection(db)

    tmpl.CreateMmMusicFromTemplate(genDat.GenerateMmMusicFromDb(conn))
    tmpl.CreateMmScoreFromTemplate(genDat.GenerateMmScoreFromDb(conn))
    tmpl.CreateSoundBgmFromTemplate(genDat.GenerateSoundBgmFromDb(conn))
    tmpl.CreateMmTextOutEx(genDat.GenerateMmTextoutExFromDb(conn))
    tmpl.CreateMmTextOutJp(genDat.GenerateMmTextoutJpFromDb(conn))

    conn.close()


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

    for file in os.listdir(f"{os.getcwd()}/output"):
        if file != "SoundBGM.txt" and not os.path.isdir(f"{os.getcwd()}/output/{file}"):
            print(f"{os.getcwd()}/output/{file}")
            cipher_text = crypt.convert_to_bin(f"{os.getcwd()}/output/{file}")
            with open(f"{os.getcwd()}/output/encrypted/{file.replace('.txt', '')}.bin", "wb") as f:
                f.write(cipher_text)


def InitConfig():
    conf = configparser.ConfigParser()

    if not os.path.isfile(os.getcwd() + "\\config.ini"):
        with open(os.getcwd() + "\\config.ini", "w") as f:
            conf["Database"] = {}
            conf["Database"]["Name"] = f"{os.getcwd()}/database/maimai.db"
            conf.write(f)
    else:
        conf.read(os.getcwd() + "\\config.ini")
        if not conf.has_section("Database"):
            with open(os.getcwd() + "\\config.ini", "a") as f:
                conf["Database"] = {}
                conf["Database"]["Name"] = f"{os.getcwd()}/database/maimai.db"
                conf.write(f)

    return os.getcwd() + "\\config.ini"


def CreateWorkDirectories():
    if not os.path.isdir(f"{os.getcwd()}/output/encrypted"):
        os.mkdir(f"{os.getcwd()}/output/encrypted")

    if not os.path.isdir(f"{os.getcwd()}/input/"):
        os.mkdir(f"{os.getcwd()}/input/")

    if not os.path.isdir(f"{os.getcwd()}/database/"):
        os.mkdir(f"{os.getcwd()}/database/")


class GUI:
    def __init__(self):
        CreateWorkDirectories()

        self.config = configparser.ConfigParser()
        self.config.read(InitConfig())

        self.db = self.config["Database"]["Name"]
        conn = CreateConnection(self.db)
        InitDb(conn)

    def DisplayTable(self, sender, data):
        # Callbacks run on a separate thread, sqlite doesn't like that
        tempConn = CreateConnection(self.db)
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
            lines = dba.SelectSoundBgmOrderId(tempConn)
            simple.show_item("window_soundBgmDisplay")
            core.clear_table("table_soundBgm")
            for line in lines:
                core.add_row("table_soundBgm", [line[1], line[0]])

        else:
            pass

        tempConn.close()

    def SelectMaimaiFolder(self, version):
        root = tkinter.Tk()
        root.withdraw()
        folder = filedialog.askdirectory(title=f"Select maimai {version} folder")

        if version == "Finale":
            if folder[folder.rfind("/") + 1:] == "maimai":
                if os.path.isfile(f"{folder}/data/SoundBGM.txt"):
                    core.set_value(f"files{version}_input_soundBgm", f"{folder}/data/SoundBGM.txt")
                    shutil.copy(f"{folder}/data/SoundBGM.txt", f"{os.getcwd()}/input/SoundBGM.txt")
                if os.path.isfile(f"{folder}/data/tables/mmMusic.bin"):
                    core.set_value(f"files{version}_input_mmMusic", f"{folder}/data/tables/mmMusic.bin")
                    shutil.copy(f"{folder}/data/tables/mmMusic.bin", f"{os.getcwd()}/input/mmMusic.bin")
                if os.path.isfile(f"{folder}/data/tables/mmScore.bin"):
                    core.set_value(f"files{version}_input_mmScore", f"{folder}/data/tables/mmScore.bin")
                    shutil.copy(f"{folder}/data/tables/mmScore.bin", f"{os.getcwd()}/input/mmScore.bin")
                if os.path.isfile(f"{folder}/data/tables/mmtextout_ex.bin"):
                    core.set_value(f"files{version}_input_mmTextoutEx", f"{folder}/data/tables/mmtextout_ex.bin")
                    shutil.copy(f"{folder}/data/tables/mmtextout_ex.bin", f"{os.getcwd()}/input/mmtextout_ex.bin")
                if os.path.isfile(f"{folder}/data/tables/mmtextout_jp.bin"):
                    core.set_value(f"files{version}_input_mmTextoutJp", f"{folder}/data/tables/mmtextout_jp.bin")
                    shutil.copy(f"{folder}/data/tables/mmtextout_jp.bin", f"{os.getcwd()}/input/mmtextout_jp.bin")
        elif version == "Murasaki":
            if folder[folder.rfind("/") + 1:] == "maimai":
                if os.path.isfile(f"{folder}/data/SoundBGM.txt"):
                    core.set_value(f"files{version}_input_soundBgm", f"{folder}/data/SoundBGM.txt")
                    shutil.copy(f"{folder}/data/SoundBGM.txt", f"{os.getcwd()}/input/SoundBGM.txt")
                if os.path.isfile(f"{folder}/data/tables/mmMusic.tbl"):
                    core.set_value(f"files{version}_input_mmMusic", f"{folder}/data/tables/mmMusic.tbl")
                    shutil.copy(f"{folder}/data/tables/mmMusic.tbl", f"{os.getcwd()}/input/mmMusic.tbl")
                if os.path.isfile(f"{folder}/data/tables/mmScore.tbl"):
                    core.set_value(f"files{version}_input_mmScore", f"{folder}/data/tables/mmScore.tbl")
                    shutil.copy(f"{folder}/data/tables/mmScore.tbl", f"{os.getcwd()}/input/mmScore.tbl")
                if os.path.isfile(f"{folder}/data/tables/mmtextout_ex.tbl"):
                    core.set_value(f"files{version}_input_mmTextoutEx", f"{folder}/data/tables/mmtextout_ex.tbl")
                    shutil.copy(f"{folder}/data/tables/mmtextout_ex.tbl", f"{os.getcwd()}/input/mmtextout_ex.tbl")
                if os.path.isfile(f"{folder}/data/tables/mmtextout_jp.tbl"):
                    core.set_value(f"files{version}_input_mmTextoutJp", f"{folder}/data/tables/mmtextout_jp.tbl")
                    shutil.copy(f"{folder}/data/tables/mmtextout_jp.tbl", f"{os.getcwd()}/input/mmtextout_jp.tbl")
        elif version == "Green":
            pass

    def GenerateAndEncryptFiles(self):
        GenerateFilesFromDb(self.db)
        self.AppendLog("Files created")
        if core.get_value("generate_checkbox_encryptFiles"):
            EncryptFilesInOutput()
            self.AppendLog("Encryption complete")

    def SelectTableRow(self, table):
        if len(core.get_table_selections(table)) > 1:
            # Check if new selection is lower or higher than current selection
            selectionOffsetFromPreviousSelection = core.get_table_selections(table)[0][0]

            if selectionOffsetFromPreviousSelection == core.get_table_selections(table)[1][0]:
                indx = -1
            else:
                indx = 0
        else:
            indx = 0

        selectedRow = core.get_table_selections(table)[indx][0]

        for cell in core.get_table_selections(table):
            core.set_table_selection(table, cell[0], cell[1], False)

        for col in range(len(core.get_table_data(table)[0])):
            core.set_table_selection(table, selectedRow, col, True)

    def GetFirstSelectedCellValue(self, table):
        return core.get_table_item(table, core.get_table_selections(table)[0][0],
                                   core.get_table_selections(table)[0][1])

    def ActivateDisplay(self):
        with simple.window("window_selectMaimaiFiles", label="Select maimai files", y_pos=400):
            with simple.tab_bar("maimai Versions"):
                with simple.tab("FiNALE"):
                    core.add_button("filesFinale_button_selectMaimaiFolder", label="Select maimai FiNALE folder",
                                    callback=lambda: self.SelectMaimaiFolder("Finale"))
                    core.add_input_text("filesFinale_input_mmMusic", label="mmMusic.bin")
                    core.add_input_text("filesFinale_input_mmScore", label="mmScore.bin")
                    core.add_input_text("filesFinale_input_mmTextoutEx", label="mmTextoutEx.bin")
                    core.add_input_text("filesFinale_input_mmTextoutJp", label="mmTextoutJp.bin")
                    core.add_input_text("filesFinale_input_soundBgm", label="soundBGM.txt")
                    core.add_button("filesFinale_button_decryptFiles", label="Decrypt Files",
                                    callback=DecryptFilesInInput)
                    core.add_button("filesFinale_button_loadFilesIntoDatabase", label="Load Files Into Database",
                                    callback=lambda: LoadFilesIntoDb(f"{os.getcwd()}/input", self.db))
                with simple.tab("Murasaki"):
                    core.add_button("filesMurasaki_button_selectMaimaiFolder", label="Select maimai Murasaki folder",
                                    callback=lambda: self.SelectMaimaiFolder("Murasaki"))
                    core.add_input_text("filesMurasaki_input_mmMusic", label="mmMusic.tbl")
                    core.add_input_text("filesMurasaki_input_mmScore", label="mmScore.tbl")
                    core.add_input_text("filesMurasaki_input_mmTextoutEx", label="mmTextoutEx.tbl")
                    core.add_input_text("filesMurasaki_input_mmTextoutJp", label="mmTextoutJp.tbl")
                    core.add_input_text("filesMurasaki_input_soundBgm", label="soundBGM.txt")
                with simple.tab("Green"):
                    pass
        with simple.window("window_importMaimaiData", label="Import maimai data"):
            core.add_input_int("import_input_importTrackId", min_value=0, step_fast=10, max_value=99999,
                               label="Track Id", default_value=0)
            core.add_combo("import_combo_importVersion", label="Import from version",
                           items=["maimai Murasaki", "maimai Green"], default_value="maimai Murasaki")
            core.add_button("import_button_importTrackId", label="Import data", callback=self.ImportData)

        with simple.window("window_editMaimaiData", label="Edit maimai FiNALE data"):
            with simple.tab_bar("Data Types"):
                with simple.tab("Artist"):
                    core.add_text("Artist")
                    core.add_input_int("dataArtist_input_addArtistId", label="Artist ID", max_value=9999, min_value=0,
                                       step_fast=100, callback=self.GetDataFromDb, callback_data="GetArtist")
                    core.add_input_text("dataArtist_input_addArtistEx", label="Ex Artist")
                    core.add_input_text("dataArtist_input_addArtistJp", label="Jp Artist")
                    core.add_button("dataArtist_button_addArtistToDb", label="Add artist to database",
                                    callback=self.InsertDataToDb, callback_data="InsertArtist")
                    core.add_same_line()
                    core.add_button("dataTrack_button_showArtistTable", label="Show track artist table",
                                    callback=self.DisplayTable, callback_data="artist")
                with simple.tab("Track Name"):
                    core.add_text("Track Name")
                    core.add_input_int("dataTrack_input_addTrackId", label="Track ID", max_value=9999, min_value=0,
                                       step_fast=100, callback=self.GetDataFromDb, callback_data="GetTrackName")
                    core.add_input_text("dataTrack_input_addTrackEx", label="Ex Track")
                    core.add_input_text("dataTrack_input_addTrackJp", label="Jp Track")
                    core.add_button("dataTrack_button_addTrackNameToDb", label="Add track name to database",
                                    callback=self.InsertDataToDb, callback_data="InsertTrackName")
                    core.add_same_line()
                    core.add_button("dataTrack_button_showTrackNameTable", label="Show track name table",
                                    callback=self.DisplayTable, callback_data="track")
                with simple.tab("Designer Name"):
                    core.add_text("Designer Name")
                    core.add_input_int("dataDesigner_input_addDesignerId", label="Designer ID", max_value=99,
                                       min_value=0, step_fast=10, callback=self.GetDataFromDb,
                                       callback_data="GetDesignerName")
                    core.add_input_text("dataDesigner_input_addDesignerEx", label="Ex Designer")
                    core.add_input_text("dataDesigner_input_addDesignerJp", label="Jp Designer")
                    core.add_button("dataDesigner_button_addDesignerToDb", label="Add designer to database",
                                    callback=self.InsertDataToDb, callback_data="InsertDesignerName")
                    core.add_same_line()
                    core.add_button("dataDesigner_button_showDesignerTable", label="Show score designer table",
                                    callback=self.DisplayTable, callback_data="designer")
                # TODO add tips
                with simple.tab("mmMusic"):
                    core.add_input_int("dataMmMusic_input_addTrackId", label="Track ID", max_value=999, min_value=0,
                                       step_fast=100, callback=self.GetDataFromDb, callback_data="GetMmMusic")
                    # name
                    core.add_input_int("dataMmMusic_input_addVersion", label="Version", max_value=99999, min_value=0,
                                       step_fast=1000, default_value=10000)
                    # subcate -> 30
                    core.add_input_float("dataMmMusic_input_addBpm", label="BPM", max_value=999.999, format="%.3f",
                                         min_value=0, step=1.0, step_fast=10.0)
                    core.add_input_int("dataMmMusic_input_addSortId", label="Sort Id", max_value=999999, min_value=0,
                                       step=10, step_fast=1000, default_value=300000)
                    # dress -> 0
                    # darkness -> 0
                    # mile -> 0
                    core.add_checkbox("dataMmMusic_checkbox_addHasVideo", label="Track has video file")
                    # event -> 0
                    # rec -> 1
                    core.add_input_float("dataMmMusic_input_addPvStart", label="PV Start", max_value=999.99,
                                         step_fast=10.0, step=1.0, format="%.2f", min_value=0.00)
                    core.add_input_float("dataMmMusic_input_addPvEnd", label="PV End", max_value=999.99, step_fast=10.0,
                                         step=1.0, format="%.2f", min_value=0.00)
                    # song duration -> 0
                    # off_rank -> 0
                    # ad_def -> 0
                    core.add_input_int("dataMmMusic_input_addRemaster", label="Remaster", max_value=99999999,
                                       min_value=0, step=1, step_fast=10000000, default_value=99999999)
                    # special_pv -> 0
                    # challenge_track -> 0
                    # bonus -> 0
                    core.add_combo("dataMmMusic_combo_addGenreId", label="Genre",
                                   items=["Pops & Anime", "niconico & Vocaloid", "Touhou Project", "Sega",
                                          "Game & Variety", "Original & Joypolis"], default_value="Pops & Anime")
                    core.add_input_int("dataMmMusic_input_addTitleId", label="Title Id", max_value=9999, min_value=0,
                                       step_fast=100)
                    core.add_input_int("dataMmMusic_input_addArtistId", label="Artist Id", max_value=9999, min_value=0,
                                       step_fast=100)
                    core.add_input_int("dataMmMusic_input_addSortJpIndex", label="Sort Index JP", max_value=999999,
                                       min_value=0, step_fast=10000, step=1)
                    core.add_input_int("dataMmMusic_input_addSortExIndex", label="Sort Index EX", max_value=999999,
                                       min_value=0, step_fast=10000, step=1)
                    core.add_input_text("dataMmMusic_input_addFilename", label="Filename")
                    core.add_button("dataMmMusic_button_showMmMusicTable", label="Show music table",
                                    callback=self.DisplayTable, callback_data="mmMusic")
                    core.add_button("dataMmMusic_button_addTrackToDb", label="Add track to database",
                                    callback=self.InsertDataToDb, callback_data="InsertMmMusic")

                    core.add_text("dataMmMusic_hidden_subcate", show=False, default_value="30")
                    core.add_text("dataMmMusic_hidden_dress", show=False, default_value="0")
                    core.add_text("dataMmMusic_hidden_darkness", show=False, default_value="0")
                    core.add_text("dataMmMusic_hidden_mile", show=False, default_value="0")

                    core.add_text("dataMmMusic_hidden_event", show=False, default_value="0")
                    core.add_text("dataMmMusic_hidden_rec", show=False, default_value="1")
                    core.add_text("dataMmMusic_hidden_songDuration", show=False, default_value="0")
                    core.add_text("dataMmMusic_hidden_offRanking", show=False, default_value="0")

                    core.add_text("dataMmMusic_hidden_adDef", show=False, default_value="0")
                    core.add_text("dataMmMusic_hidden_specialPv", show=False, default_value="0")
                    core.add_text("dataMmMusic_hidden_challengeTrack", show=False, default_value="0")
                    core.add_text("dataMmMusic_hidden_bonus", show=False, default_value="0")

                with simple.tab("mmScore"):
                    core.add_input_int("dataMmScore_input_addTrackId", label="Track ID", max_value=999, min_value=0,
                                       step_fast=100, default_value=0, callback=self.GetDataFromDb,
                                       callback_data="GetMmScore")

                    core.add_text("Score Id")
                    core.add_same_line(spacing=60)
                    core.add_text("Difficulty")
                    core.add_same_line(spacing=52)
                    core.add_text("Score Designer Id")

                    for i in range(1, 7, 1):

                        core.add_input_int(f"dataMmScore_input_addScoreId_0{i}", label="", min_value=0, max_value=99, step_fast=10, width=100, default_value=0)
                        core.add_same_line()
                        core.add_input_float(f"dataMmScore_input_addDifficulty_0{i}", label="", max_value=99.9,
                                             format="%.1f", min_value=0, step=0.1, step_fast=1.0, width=100)
                        core.add_same_line()
                        core.add_input_int(f"dataMmScore_input_addDesignerId_0{i}", label="", max_value=99,
                                           min_value=0, step_fast=10, width=100)
                        core.add_same_line()
                        core.add_checkbox(f"dataMmScore_checkbox_addIsInUtage_0{i}", label="In Utage")

                    core.add_input_text("dataMmScore_input_addBaseSafename", label="Score Basename")
                    core.add_button("dataMmScore_button_addScoreToDb", label="Add score to database",
                                    callback=self.InsertDataToDb, callback_data="InsertMmScore")
                    core.add_same_line()
                    core.add_button("dataMmScore_button_showMmScoreTable", label="Show score table",
                                    callback=self.DisplayTable, callback_data="mmScore")
                with simple.tab("Sound BGM"):
                    core.add_input_int("dataSoundBgm_input_addTrackId", label="Track ID", max_value=999, min_value=0,
                                       step_fast=100, callback=self.GetDataFromDb, callback_data="GetSoundBgm")
                    core.add_input_text("dataSoundBgm_input_addTitle", label="Track Filename")
                    core.add_button("dataSoundBgm_button_addSoundBgmToDB", label="Add sound bgm to database",
                                    callback=self.InsertDataToDb, callback_data="")
                    core.add_same_line()
                    core.add_button("dataMmScore_button_showSoundBgmTable", label="Show sound table",
                                    callback=self.DisplayTable, callback_data="soundBgm")
                core.add_checkbox("data_checkbox_replaceDbEntry", label="Overwrite current database entry")

        with simple.window("window_generateMaimaiFiles", label="Generate maimai Files", x_pos=400):
            core.add_text("Generate data files for maimai FiNALE")
            core.add_button("generate_button_createFiles", label="Generate Files",
                            callback=self.GenerateAndEncryptFiles)
            core.add_checkbox("generate_checkbox_encryptFiles", label="Encrypt Files", default_value=True)
            core.add_spacing(count=4)
            core.add_button("generate_button_openOutputFolder", label="Open Output Folder",
                            callback=lambda: os.startfile(f"{os.getcwd()}/output"))

        with simple.window("window_mmMusicDisplay", label="mmMusic Grid", show=False):
            columns = ["track_id", "name", "ver", "subcate", "bpm", "sort_id", "dress", "darkness", "mile", "vl",
                       "event", "rec", "pvstart", "pvend", "song_duration", "off_ranking", "ad_def", "remaster",
                       "special_pv", "challenge_track", "bonus", "genre_id", "title", "artist", "sort_jp_index",
                       "sort_ex_index", "filename"]
            core.add_table("table_mmMusic", columns, height=0, width=0,
                           callback=lambda: [self.SelectTableRow("table_mmMusic"),
                                             core.set_value("dataMmMusic_input_addTrackId",
                                                            int(self.GetFirstSelectedCellValue("table_mmMusic"))),
                                             self.GetDataFromDb("", "GetMmMusic")])

        with simple.window("window_mmScoreDisplay", label="mmScore Grid", show=False):
            columns = ["track_id", "name", "lv", "designer_id", "utage_mode", "safename"]
            core.add_table("table_mmScore", columns, height=0, width=0,
                           callback=lambda: [self.SelectTableRow("table_mmScore"),
                                             core.set_value("dataMmScore_input_addTrackId",
                                                            int(self.GetFirstSelectedCellValue("table_mmScore")[:-2])),
                                             self.GetDataFromDb("", "GetMmScore")])

        with simple.window("window_textoutArtistDisplay", label="Artist Name Grid", show=False):
            columns = ["artist_id", "ex_artist_title", "jp_artist_title"]
            core.add_table("table_textoutArtist", columns, height=0, width=0,
                           callback=lambda: [self.SelectTableRow("table_textoutArtist"),
                                             core.set_value("dataArtist_input_addArtistId",
                                                            int(self.GetFirstSelectedCellValue("table_textoutArtist"))),
                                             self.GetDataFromDb("", "GetArtist")])

        with simple.window("window_textoutTrackDisplay", label="Track Name Grid", show=False):
            columns = ["track_id", "ex_track_title", "jp_track_title"]
            core.add_table("table_textoutTrack", columns, height=0, width=0,
                           callback=lambda: [self.SelectTableRow("table_textoutTrack"),
                                             core.set_value("dataTrack_input_addTrackId",
                                                            int(self.GetFirstSelectedCellValue("table_textoutTrack"))),
                                             self.GetDataFromDb("", "GetTrackName")])

        with simple.window("window_textoutDesignerDisplay", label="Track Designer Grid", show=False):
            columns = ["designer_id", "ex_designer_name", "jp_designer_name"]
            core.add_table("table_textoutDesigner", columns, height=0, width=0,
                           callback=lambda: [self.SelectTableRow("table_textoutDesigner"),
                                             core.set_value("dataDesigner_input_addDesignerId",
                                                            int(self.GetFirstSelectedCellValue(
                                                                "table_textoutDesigner"))),
                                             self.GetDataFromDb("", "GetDesignerName")])

        with simple.window("window_soundBgmDisplay", label="Sound BGM Grid", show=False):
            columns = ["track_id", "title"]
            core.add_table("table_soundBgm", columns, height=0, width=0,
                           callback=lambda: [self.SelectTableRow("table_soundBgm"),
                                             core.set_value("dataSoundBgm_input_addTrackId",
                                                            int(self.GetFirstSelectedCellValue("table_soundBgm"))),
                                             self.GetDataFromDb("", "GetSoundBgm")])

        with simple.window("window_log", label="Log"):
            core.add_input_text("log_input_log", label="", multiline=True, readonly=True, width=600, height=1200)
            core.add_same_line()
            core.add_button("log_button_clearLog", label="Clear", callback=lambda: core.set_value("log_input_log", ""))

        core.enable_docking(dock_space=True)

        core.add_additional_font("NotoSerifCJKjp-Medium.otf", 20, "japanese")

        core.set_start_callback(self.OnStart)
        core.set_render_callback(self.MainCallback)
        core.set_exit_callback(self.OnExit)

        self.load_layout(self.GetCurrentWindowNames())

        core.set_main_window_title("maimaiTool")
        core.start_dearpygui()

    def InsertDataToDb(self, sender, data):
        tempConn = CreateConnection(self.db)

        if data == "InsertArtist":
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
            designerId = hlp.AffixZeroesToString(core.get_value("dataDesigner_input_addDesignerId"), 4)
            designerEx = core.get_value("dataDesigner_input_addDesignerEx")
            designerJp = core.get_value("dataDesigner_input_addDesignerJp")

            if designerId == "":
                return

            if not (dba.InsertLineToTextOutDesigner(tempConn, [designerId, designerEx, designerJp])):
                if core.get_value("data_checkbox_replaceDbEntry"):
                    dba.ReplaceLineInTextOutDesigner(tempConn, [designerId, designerEx, designerJp])
                    self.AppendLog("Entry replaced")
                else:
                    self.AppendLog("Entry already exists")
            else:
                self.AppendLog("Entry added")

        elif data == "InsertMmMusic":
            trackId = core.get_value("dataMmMusic_input_addTrackId")

            if trackId == "":
                return

            name = f"eMusic_{hlp.AffixZeroesToString(trackId, 3)}"
            version = core.get_value("dataMmMusic_input_addVersion")
            subcate = "30"
            bpm = f'{round(core.get_value("dataMmMusic_input_addBpm"), 3):g}'
            sortId = core.get_value("dataMmMusic_input_addSortId")
            dress = "0"
            darkness = "0"
            mile = "0"
            videoBool = hlp.BoolToValueReversed(core.get_value("dataMmMusic_checkbox_addHasVideo"))
            event = "0"
            rec = "1"
            pvStart = f'{round(core.get_value("dataMmMusic_input_addPvStart"), 2):g}'
            pvEnd = f'{round(core.get_value("dataMmMusic_input_addPvEnd"), 2):g}'
            songDuration = "0"
            offRanking = "0"
            adDef = "0"
            remaster = core.get_value("dataMmMusic_input_addRemaster")
            specialPv = "0"
            challengeTrack = "0"
            bonus = "0"
            genreId = hlp.GenreTextToFinaleValue(core.get_value("dataMmMusic_combo_addGenreId"))
            titleId = hlp.AffixZeroesToString(core.get_value("dataMmMusic_input_addTitleId"), 4)
            artistId = hlp.AffixZeroesToString(core.get_value("dataMmMusic_input_addArtistId"), 4)
            sortIndexJp = core.get_value("dataMmMusic_input_addSortJpIndex")
            sortIndexEx = core.get_value("dataMmMusic_input_addSortExIndex")
            filename = core.get_value("dataMmMusic_input_addFilename").lower()

            subcate = core.get_value("dataMmMusic_hidden_subcate")
            dress = core.get_value("dataMmMusic_hidden_dress")
            darkness = core.get_value("dataMmMusic_hidden_darkness")
            mile = core.get_value("dataMmMusic_hidden_mile")

            event = core.get_value("dataMmMusic_hidden_event")
            rec = core.get_value("dataMmMusic_hidden_rec")
            songDuration = core.get_value("dataMmMusic_hidden_songDuration")
            offRanking = core.get_value("dataMmMusic_hidden_offRanking")

            adDef = core.get_value("dataMmMusic_hidden_adDef")
            specialPv = core.get_value("dataMmMusic_hidden_specialPv")
            challengeTrack = core.get_value("dataMmMusic_hidden_challengeTrack")
            bonus = core.get_value("dataMmMusic_hidden_bonus")

            data = [trackId, name, version, subcate, bpm, sortId, dress, darkness, mile, videoBool, event, rec
                , pvStart, pvEnd, songDuration, offRanking, adDef, remaster, specialPv, challengeTrack, bonus, genreId,
                    titleId, artistId, sortIndexJp, sortIndexEx, filename]

            if not (dba.InsertLineToMusic(tempConn, data)):
                if core.get_value("data_checkbox_replaceDbEntry"):
                    dba.ReplaceLineInMusic(tempConn, data)
                    self.AppendLog("Entry replaced")
                else:
                    self.AppendLog("Entry already exists")
            else:
                self.AppendLog("Entry added")

        elif data == "InsertMmScore":
            trackId = core.get_value("dataMmScore_input_addTrackId")

            if trackId == "":
                return

            # Get all rows where score id is not 0
            for i in range(1, 7, 1):
                if core.get_value(f"dataMmScore_input_addScoreId_0{i}") != 0:
                    scoreId = hlp.AffixZeroesToString(core.get_value(f"dataMmScore_input_addScoreId_0{i}"), 2)
                    lv = f'{round(core.get_value(f"dataMmScore_input_addDifficulty_0{i}"), 1):g}' # :g Removes trailing zeroes
                    designerId = core.get_value(f"dataMmScore_input_addDesignerId_0{i}")
                    utageMode = hlp.BoolToValueReversed(core.get_value(f"dataMmScore_checkbox_addIsInUtage_0{i}"))
                    baseSafename = core.get_value("dataMmScore_input_addBaseSafename")

                    name = f"eScore_{hlp.AffixZeroesToString(trackId, 3)}_{baseSafename}_{scoreId}"
                    safename = f"{hlp.AffixZeroesToString(trackId, 3)}_{baseSafename}_{scoreId}"

                    trackAndScoreId = int(str(trackId) + scoreId)

                    data = [trackAndScoreId, name, lv, designerId, utageMode, safename]

                    if not (dba.InsertLineToScore(tempConn, data)):
                        if core.get_value("data_checkbox_replaceDbEntry"):
                            dba.ReplaceLineInScore(tempConn, data)
                            self.AppendLog(f"Entry {scoreId} replaced")
                        else:
                            self.AppendLog(f"Entry {scoreId} already exists")
                    else:
                        self.AppendLog(f"Entry {scoreId} added")

        elif data == "InsertSoundBgm":
            title = core.get_value("dataSoundBgm_input_addTitle")
            trackId = core.get_value("dataSoundBgm_input_addTrackId")

            if not (dba.InsertLineToSoundBgm(tempConn, [title, trackId])):
                if core.get_value("data_checkbox_replaceDbEntry"):
                    dba.ReplaceLineInSoundBgm(tempConn, [title, trackId])
                    self.AppendLog("Entry replaced")
                else:
                    self.AppendLog("Entry already exists")
            else:
                self.AppendLog("Entry added")

        else:
            self.AppendLog("wip")

        tempConn.close()

    def GetDataFromDb(self, sender, data):
        tempConn = CreateConnection(self.db)

        if data == "GetArtist":
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
            designerId = hlp.AffixZeroesToString(core.get_value("dataDesigner_input_addDesignerId"), 4)
            row = dba.SelectMmTextoutDesignerById(tempConn, designerId)

            if len(row) > 0:
                row = row[0]
                core.set_value("dataDesigner_input_addDesignerEx", row[0])
                core.set_value("dataDesigner_input_addDesignerJp", row[1])
            else:
                core.set_value("dataDesigner_input_addDesignerEx", "")
                core.set_value("dataDesigner_input_addDesignerJp", "")

        elif data == "GetMmMusic":
            trackId = core.get_value("dataMmMusic_input_addTrackId")
            row = dba.SelectMmMusicById(tempConn, trackId)

            if len(row) > 0:
                row = row[0]
                dg.UpdateDataMmMusicFields(row)
            else:
                dg.DefaultDataMmMusicFields()

        # Grabs all scores for the track id
        elif data == "GetMmScore":
            trackId = core.get_value("dataMmScore_input_addTrackId")
            rows = dba.SelectMmScoreById(tempConn, hlp.AffixZeroesToString(trackId, 3))

            for i in range(1, 7, 1):
                core.set_value(f"dataMmScore_input_addScoreId_0{i}", 0)
                core.set_value(f"dataMmScore_input_addDifficulty_0{i}", 0.0)
                core.set_value(f"dataMmScore_input_addDesignerId_0{i}", 0)
                core.set_value(f"dataMmScore_checkbox_addIsInUtage_0{i}", False)

            core.set_value("dataMmScore_input_addBaseSafename", "")

            for enum, row in enumerate(rows):
                core.set_value(f"dataMmScore_input_addScoreId_0{enum + 1}", enum + 1)
                core.set_value(f"dataMmScore_input_addDifficulty_0{enum + 1}", float(row[2]))
                core.set_value(f"dataMmScore_input_addDesignerId_0{enum + 1}", int(row[3]))
                core.set_value(f"dataMmScore_checkbox_addIsInUtage_0{enum + 1}", hlp.ValueToBoolReversed(row[4]))

                if enum == 0:
                    core.set_value(f"dataMmScore_input_addBaseSafename", row[5][4:-3])

        elif data == "GetSoundBgm":
            trackId = core.get_value("dataSoundBgm_input_addTrackId")
            row = dba.SelectSoundBgmById(tempConn, trackId)

            if len(row) > 0:
                row = row[0]
                core.set_value("dataSoundBgm_input_addTitle", row[0])
            else:
                core.set_value("dataSoundBgm_input_addTitle", "")
        else:
            self.AppendLog("wip")

        tempConn.close()

    def ImportData(self):
        core.set_value("dataMmMusic_input_addTrackId", core.get_value("import_input_importTrackId"))

        if (dg.UpdateDataMmMusicFields(cvrt.ConvertSplitMmMusicLineFromMurasakiToFinale(
                readDat.ReadMmMusicSingleLine(core.get_value("filesMurasaki_input_mmMusic"),
                                              core.get_value("import_input_importTrackId"))))):
            pass
            # TODO Score is next, first need to reimplement score ui

    def AppendLog(self, text):
        core.set_value("log_input_log",
                       f"{core.get_value('log_input_log')}{datetime.datetime.now().strftime('%H:%M:%S')} - {text}\n")

    def MainCallback(self):
        simple.set_item_width("log_input_log", simple.get_drawing_size("window_log")[0] - 100)
        simple.set_item_height("log_input_log", simple.get_drawing_size("window_log")[1] - 35)

    def OnStart(self):
        pass

        # This doesn't set the main window size properly, when called from OnStart()
        # self.load_layout(self.GetCurrentWindowNames())

    def OnExit(self):
        self.save_layout(self.GetCurrentWindowNames())

    def save_layout(self, windows):
        with open(os.getcwd() + "\\config.ini", "r+") as f:
            self.config["Layout"] = {}
            for window in windows:
                self.config["Layout"][
                    window + "_pos"] = f"{str(simple.get_window_pos(window)[0])}, {str(simple.get_window_pos(window)[1])}"
                self.config["Layout"][
                    window + "_size"] = f"{str(simple.get_drawing_size(window)[0])}, {str(simple.get_drawing_size(window)[1])}"
            self.config["Layout"][
                "MainWindow"] = f"{str(core.get_main_window_size()[0])}, {str(core.get_main_window_size()[1])}"
            self.config.write(f)

    def load_layout(self, windows):
        if self.config.has_section("Layout"):
            for window in windows:
                try:
                    pos = self.config["Layout"][window + "_pos"].split(", ")
                    size = self.config["Layout"][window + "_size"].split(", ")
                    simple.set_window_pos(window, int(pos[0]), int(pos[1]))
                    simple.set_drawing_size(window, int(size[0]), int(size[1]))
                except KeyError as e:
                    print(f"KeyError: {e}")
            size = self.config["Layout"]["MainWindow"].split(", ")
            core.set_main_window_size(int(size[0]), int(size[1]))

    def GetCurrentWindowNames(self):
        windows = core.get_windows()
        for i in range(6):
            # TODO This should be handled better
            # Remove dearpygui's default windows from list
            windows.pop(-1)

        return windows


if __name__ == '__main__':
    # path = r"L:\Games\SDEY_1.99"

    # path = f"{os.getcwd()}/input"
    # LoadFilesIntoDb(path)

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

    GUI().ActivateDisplay()
