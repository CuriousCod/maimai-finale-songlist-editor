import os, sys
import DatabaseFormat
import sqlite3 as sq
import datetime
import Templates as tmpl
import Convert as cvrt
import ReadData as readDat
import GenerateData as genDat
import DearGui as dgHelp
import MaiCrypt
import tkinter
import shutil
import configparser
from tkinter import filedialog
from sqlite3 import Error
import DatabaseActions as dba
import Helpers as hlp
import dearpygui.dearpygui as dpg

# TODO Display all ids without data
# TODO Function to check all data connections for an id
# TODO Import all required data from other maimai versions based on mmusic id
# TODO Support for mmMusic event field
# TODO Dynamic row adding for mmScore entries
# TODO Load files into db should always create a new db file
# TODO Make sort id easier to understand/automatic (01 -> a, 02 -> b, etc)


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
    supportedVersions = ["Finale", "Murasaki"]

    if not os.path.isfile(os.getcwd() + "\\config.ini"):
        conf.add_section("Database")
        conf["Database"]["Name"] = f"{os.getcwd()}/database/maimai.db"
        conf.add_section("FilesFinale")
        conf.add_section("FilesMurasaki")
    else:
        conf.read(os.getcwd() + "\\config.ini")
        if not conf.has_section("Database"):
            conf.add_section("Database")
            conf["Database"]["Name"] = f"{os.getcwd()}/database/maimai.db"
        for version in supportedVersions:
            if not conf.has_section(f"Files{version}"):
                conf.add_section(f"Files{version}")
                conf[f"Files{version}"]["mmMusic"] = ""
                conf[f"Files{version}"]["mmScore"] = ""
                conf[f"Files{version}"]["mmTextoutEx"] = ""
                conf[f"Files{version}"]["mmTextoutJp"] = ""
                conf[f"Files{version}"]["soundBgm"] = ""

    with open(os.getcwd() + "\\config.ini", "w") as f:
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
        conn.close()


    def DisplayTable(self, sender, data):
        # Callbacks run on a separate thread, sqlite doesn't like that
        tempConn = CreateConnection(self.db)
        table = hlp.DataContainers()

        if data == table.mmMusic:
            lines = dba.SelectMmMusic(tempConn)
            dpg.show_item(self.ui_window_mmMusicDisplay)
            dpg.clear_table("table_mmMusic")
            for line in lines:
                dpg.add_row("table_mmMusic", line)

        elif data == table.mmScore:
            lines = dba.SelectMmScore(tempConn)
            dpg.show_item(self.ui_window_mmScoreDisplay)
            dpg.clear_table("table_mmScore")
            for line in lines:
                dpg.add_row("table_mmScore", line)

        elif data == table.artist:
            lines = dba.SelectMmTextoutArtist(tempConn)
            dpg.show_item(self.ui_window_textoutArtistDisplay)
            dpg.clear_table("table_textoutArtist")
            for line in lines:
                dpg.add_row("table_textoutArtist", line)

        elif data == table.track:
            lines = dba.SelectMmTextoutTrack(tempConn)
            dpg.show_item(self.ui_window_textoutTrackDisplay)
            dpg.clear_table("table_textoutTrack")
            for line in lines:
                dpg.add_row("table_textoutTrack", line)

        elif data == table.designer:
            lines = dba.SelectMmTextoutDesigner(tempConn)
            dpg.show_item(self.ui_window_textoutDesignerDisplay)
            dpg.clear_table("table_textoutDesigner")
            for line in lines:
                dpg.add_row("table_textoutDesigner", line)

        elif data == table.soundBgm:
            lines = dba.SelectSoundBgmOrderId(tempConn)
            dpg.show_item(self.ui_window_soundBgmDisplay)
            dpg.clear_table("table_soundBgm")
            for line in lines:
                dpg.add_row("table_soundBgm", [line[1], line[0]])

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
                    dpg.set_value(self.ui_filesFinale_input_soundBgm, f"{folder}/data/SoundBGM.txt")
                    shutil.copy(f"{folder}/data/SoundBGM.txt", f"{os.getcwd()}/input/SoundBGM.txt")
                if os.path.isfile(f"{folder}/data/tables/mmMusic.bin"):
                    dpg.set_value(self.ui_filesFinale_input_mmMusic, f"{folder}/data/tables/mmMusic.bin")
                    shutil.copy(f"{folder}/data/tables/mmMusic.bin", f"{os.getcwd()}/input/mmMusic.bin")
                if os.path.isfile(f"{folder}/data/tables/mmSdpg.bin"):
                    dpg.set_value(self.ui_filesFinale_input_mmScore, f"{folder}/data/tables/mmSdpg.bin")
                    shutil.copy(f"{folder}/data/tables/mmSdpg.bin", f"{os.getcwd()}/input/mmSdpg.bin")
                if os.path.isfile(f"{folder}/data/tables/mmtextout_ex.bin"):
                    dpg.set_value(self.ui_filesFinale_input_mmTextoutEx, f"{folder}/data/tables/mmtextout_ex.bin")
                    shutil.copy(f"{folder}/data/tables/mmtextout_ex.bin", f"{os.getcwd()}/input/mmtextout_ex.bin")
                if os.path.isfile(f"{folder}/data/tables/mmtextout_jp.bin"):
                    dpg.set_value(self.ui_filesFinale_input_mmTextoutJp, f"{folder}/data/tables/mmtextout_jp.bin")
                    shutil.copy(f"{folder}/data/tables/mmtextout_jp.bin", f"{os.getcwd()}/input/mmtextout_jp.bin")
        elif version == "Murasaki":
            if folder[folder.rfind("/") + 1:] == "maimai":
                if os.path.isfile(f"{folder}/data/SoundBGM.txt"):
                    dpg.set_value(self.ui_filesMurasaki_input_soundBgm, f"{folder}/data/SoundBGM.txt")
                    shutil.copy(f"{folder}/data/SoundBGM.txt", f"{os.getcwd()}/input/SoundBGM.txt")
                if os.path.isfile(f"{folder}/data/tables/mmMusic.tbl"):
                    dpg.set_value(self.ui_filesMurasaki_input_mmMusic, f"{folder}/data/tables/mmMusic.tbl")
                    shutil.copy(f"{folder}/data/tables/mmMusic.tbl", f"{os.getcwd()}/input/mmMusic.tbl")
                if os.path.isfile(f"{folder}/data/tables/mmSdpg.tbl"):
                    dpg.set_value(self.ui_filesMurasaki_input_mmScore, f"{folder}/data/tables/mmSdpg.tbl")
                    shutil.copy(f"{folder}/data/tables/mmSdpg.tbl", f"{os.getcwd()}/input/mmSdpg.tbl")
                if os.path.isfile(f"{folder}/data/tables/mmtextout_ex.tbl"):
                    dpg.set_value(self.ui_filesMurasaki_input_mmTextoutEx, f"{folder}/data/tables/mmtextout_ex.tbl")
                    shutil.copy(f"{folder}/data/tables/mmtextout_ex.tbl", f"{os.getcwd()}/input/mmtextout_ex.tbl")
                if os.path.isfile(f"{folder}/data/tables/mmtextout_jp.tbl"):
                    dpg.set_value(self.ui_filesMurasaki_input_mmTextoutJp, f"{folder}/data/tables/mmtextout_jp.tbl")
                    shutil.copy(f"{folder}/data/tables/mmtextout_jp.tbl", f"{os.getcwd()}/input/mmtextout_jp.tbl")
        elif version == "Green":
            pass

    def GenerateAndEncryptFiles(self):
        GenerateFilesFromDb(self.db)
        self.AppendLog("Files created")
        if dpg.get_value(self.ui_generate_checkbox_encryptFiles):
            EncryptFilesInOutput()
            self.AppendLog("Encryption complete")

    def SelectTableRow(self, table):
        if len(dpg.get_table_selections(table)) > 1:
            # Check if new selection is lower or higher than current selection
            selectionOffsetFromPreviousSelection = dpg.get_table_selections(table)[0][0]

            if selectionOffsetFromPreviousSelection == dpg.get_table_selections(table)[1][0]:
                indx = -1
            else:
                indx = 0
        else:
            indx = 0

        selectedRow = dpg.get_table_selections(table)[indx][0]

        for cell in dpg.get_table_selections(table):
            dpg.set_table_selection(table, cell[0], cell[1], False)

        for col in range(len(dpg.get_table_data(table)[0])):
            dpg.set_table_selection(table, selectedRow, col, True)

    def GetFirstSelectedCellValue(self, table):
        return dpg.get_table_item(table, dpg.get_table_selections(table)[0][0],
                                   dpg.get_table_selections(table)[0][1])

    def ActivateDisplay(self):
        data = hlp.DataContainers()

        with dpg.window(label="Select maimai files") as ui_window_selectMaimaiFiles:
            with dpg.tab_bar(label="maimai Versions"):
                with dpg.tab(label="FiNALE"):
                    self.ui_filesFinale_button_selectMaimaiFolder = dpg.add_button( label="Select maimai FiNALE folder",
                                    callback=lambda: self.SelectMaimaiFolder("Finale"))
                    self.ui_filesFinale_input_mmMusic = dpg.add_input_text(label="mmMusic.bin")
                    self.ui_filesFinale_input_mmScore = dpg.add_input_text(label="mmScore.bin")
                    self.ui_filesFinale_input_mmTextoutEx = dpg.add_input_text(label="mmTextoutEx.bin")
                    self.ui_filesFinale_input_mmTextoutJp = dpg.add_input_text(label="mmTextoutJp.bin")
                    self.ui_filesFinale_input_soundBgm = dpg.add_input_text(label="soundBGM.txt")
                    self.ui_filesFinale_button_decryptFiles = dpg.add_button(label="Decrypt Files",
                                    callback=DecryptFilesInInput)
                    self.ui_filesFinale_button_loadFilesIntoDatabase = dpg.add_button(label="Load Files Into Database",
                                    callback=lambda: LoadFilesIntoDb(f"{os.getcwd()}/input", self.db))
                with dpg.tab(label="Murasaki"):
                    self.ui_filesMurasaki_button_selectMaimaiFolder = dpg.add_button(label="Select maimai Murasaki folder",
                                    callback=lambda: self.SelectMaimaiFolder("Murasaki"))
                    self.ui_filesMurasaki_input_mmMusic = dpg.add_input_text(label="mmMusic.tbl")
                    self.ui_filesMurasaki_input_mmScore = dpg.add_input_text(label="mmSdpg.tbl")
                    self.ui_filesMurasaki_input_mmTextoutEx = dpg.add_input_text(label="mmTextoutEx.tbl")
                    self.ui_filesMurasaki_input_mmTextoutJp = dpg.add_input_text(label="mmTextoutJp.tbl")
                    self.ui_filesMurasaki_input_soundBgm = dpg.add_input_text(label="soundBGM.txt")
                with dpg.tab(label="Green"):
                    pass
        with dpg.window(label="Import maimai data") as self.ui_window_importMaimaiData:
            self.ui_import_input_importTrackId = dpg.add_input_int(min_value=0, step_fast=10, max_value=99999,
                               label="Track Id", default_value=0)
            self.ui_import_combo_importVersion = dpg.add_combo(label="Import from version",
                           items=["maimai Murasaki", "maimai Green"], default_value="maimai Murasaki")
            self.ui_import_button_importTrackId = dpg.add_button(label="Import data", callback=self.ImportData)

        with dpg.window(label="Edit maimai FiNALE data") as self.ui_window_editMaimaiData:
            with dpg.tab_bar(label="Data Types"):
                # TODO add tips
                with dpg.tab(label="mmMusic"):
                    self.ui_dataMmMusic_input_addTrackId = dpg.add_input_int(label="Track ID", max_value=999, min_value=0,
                                       step_fast=100, callback=self.GetDataFromDb, user_data=data.mmMusic)
                    # name
                    self.ui_dataMmMusic_input_addVersion = dpg.add_input_int(label="Version", max_value=99999, min_value=0,
                                       step_fast=1000, default_value=10000)
                    # subcate -> 30
                    self.ui_dataMmMusic_input_addBpm = dpg.add_input_float(label="BPM", max_value=999.999, format="%.3f",
                                         min_value=0, step=1.0, step_fast=10.0)
                    self.ui_dataMmMusic_input_addSortId = dpg.add_input_int(label="Sort Id", max_value=999999, min_value=0,
                                       step=10, step_fast=1000, default_value=300000)
                    # dress -> 0
                    # darkness -> 0
                    # mile -> 0
                    self.ui_dataMmMusic_checkbox_addHasVideo = dpg.add_checkbox(label="Track has video file")
                    # event -> 0
                    # rec -> 1
                    self.ui_dataMmMusic_input_addPvStart = dpg.add_input_float(label="PV Start", max_value=999.99,
                                         step_fast=10.0, step=1.0, format="%.2f", min_value=0.00)
                    self.ui_dataMmMusic_input_addPvEnd = dpg.add_input_float(label="PV End", max_value=999.99, step_fast=10.0,
                                         step=1.0, format="%.2f", min_value=0.00)
                    # song duration -> 0
                    # off_rank -> 0
                    # ad_def -> 0
                    self.ui_dataMmMusic_input_addRemaster = dpg.add_input_int(label="Remaster", max_value=99999999,
                                       min_value=0, step=1, step_fast=10000000, default_value=99999999)
                    # special_pv -> 0
                    # challenge_track -> 0
                    # bonus -> 0
                    self.ui_dataMmMusic_combo_addGenreId = dpg.add_combo(label="Genre",
                                   items=["Pops & Anime", "niconico & Vocaloid", "Touhou Project", "Sega",
                                          "Game & Variety", "Original & Joypolis", "None"], default_value="Pops & Anime")
                    self.ui_dataMmMusic_input_addTitleId = dpg.add_input_int(label="Title Id", max_value=9999, min_value=0,
                                       step_fast=100)
                    self.ui_dataMmMusic_input_addArtistId = dpg.add_input_int(label="Artist Id", max_value=9999, min_value=0,
                                       step_fast=100)
                    self.ui_dataMmMusic_input_addSortJpIndex = dpg.add_input_int(label="Sort Index JP", max_value=999999,
                                       min_value=0, step_fast=10000, step=1)
                    self.ui_dataMmMusic_input_addSortExIndex = dpg.add_input_int(label="Sort Index EX", max_value=999999,
                                       min_value=0, step_fast=10000, step=1)
                    self.ui_dataMmMusic_input_addFilename = dpg.add_input_text(label="Filename")
                    self.ui_dataMmMusic_button_showMmMusicTable = dpg.add_button(label="Show music table",
                                    callback=self.DisplayTable, user_data=data.mmMusic)
                    self.ui_dataMmMusic_button_addTrackToDb = dpg.add_button(label="Add track to database",
                                    callback=self.InsertDataToDb, user_data=data.mmMusic)

                    self.ui_dataMmMusic_hidden_subcate = dpg.add_text(show=False, default_value="30")
                    self.ui_dataMmMusic_hidden_dress = dpg.add_text(show=False, default_value="0")
                    self.ui_dataMmMusic_hidden_darkness = dpg.add_text(show=False, default_value="0")
                    self.ui_dataMmMusic_hidden_mile = dpg.add_text(show=False, default_value="0")

                    self.ui_dataMmMusic_hidden_event = dpg.add_text(show=False, default_value="0")
                    self.ui_dataMmMusic_hidden_rec = dpg.add_text(show=False, default_value="1")
                    self.ui_dataMmMusic_hidden_songDuration = dpg.add_text(show=False, default_value="0")
                    self.ui_dataMmMusic_hidden_offRanking = dpg.add_text(show=False, default_value="0")

                    self.ui_dataMmMusic_hidden_adDef = dpg.add_text(show=False, default_value="0")
                    self.ui_dataMmMusic_hidden_specialPv = dpg.add_text(show=False, default_value="0")
                    self.ui_dataMmMusic_hidden_challengeTrack = dpg.add_text(show=False, default_value="0")
                    self.ui_dataMmMusic_hidden_bonus = dpg.add_text(show=False, default_value="0")

                with dpg.tab(label="mmScore"):
                    self.ui_dataMmScore_input_addTrackId = dpg.add_input_int(label="Track ID", max_value=999, min_value=0,
                                       step_fast=100, default_value=0, callback=self.GetDataFromDb,
                                       user_data=data.mmScore)

                    dpg.add_text("Score Id")
                    dpg.add_same_line(spacing=60)
                    dpg.add_text("Difficulty")
                    dpg.add_same_line(spacing=52)
                    dpg.add_text("Score Designer Id")

                    self.ui_dataMmScore_input_addScoreId = []
                    self.ui_dataMmScore_input_addDifficulty = []
                    self.ui_dataMmScore_input_addDesignerId = []
                    self.ui_dataMmScore_checkbox_addIsInUtage = []

                    for i in range(1, 7, 1):

                        self.ui_dataMmScore_input_addScoreId.append(dpg.add_input_int(label="", min_value=0, max_value=99, step_fast=10, width=100, default_value=0))
                        dpg.add_same_line()
                        self.ui_dataMmScore_input_addDifficulty.append(dpg.add_input_float(label="", max_value=99.9,
                                             format="%.1f", min_value=0, step=0.1, step_fast=1.0, width=100))
                        dpg.add_same_line()
                        self.ui_dataMmScore_input_addDesignerId.append(dpg.add_input_int(label="", max_value=99,
                                           min_value=0, step_fast=10, width=100))
                        dpg.add_same_line()
                        self.ui_dataMmScore_checkbox_addIsInUtage.append(dpg.add_checkbox(label="In Utage"))

                    self.ui_dataMmScore_input_addBaseSafename = dpg.add_input_text(label="Score Basename")
                    self.ui_dataMmScore_button_addScoreToDb = dpg.add_button(label="Add score to database",
                                    callback=self.InsertDataToDb, user_data=data.mmScore)
                    dpg.add_same_line()
                    self.ui_dataMmScore_button_showMmScoreTable = dpg.add_button(label="Show score table",
                                    callback=self.DisplayTable, user_data=data.mmScore)

                with dpg.tab(label="Sound BGM"):
                    self.ui_dataSoundBgm_input_addTrackId = dpg.add_input_int(label="Track ID", max_value=999, min_value=0,
                                       step_fast=100, callback=self.GetDataFromDb, user_data=data.soundBgm)
                    self.ui_dataSoundBgm_input_addTitle = dpg.add_input_text(label="Track Filename")
                    self.ui_dataSoundBgm_button_addSoundBgmToDB = dpg.add_button(label="Add sound bgm to database",
                                    callback=self.InsertDataToDb, user_data=data.soundBgm)
                    dpg.add_same_line()
                    self.ui_dataMmScore_button_showSoundBgmTable = dpg.add_button(label="Show sound table",
                                    callback=self.DisplayTable, user_data=data.soundBgm)

                with dpg.tab(label="Artist"):
                    dpg.add_text("Artist")
                    self.ui_dataArtist_input_addArtistId = dpg.add_input_int(label="Artist ID", max_value=9999, min_value=0,
                                       step_fast=100, callback=self.GetDataFromDb, user_data=data.mmMusic)
                    self.ui_dataArtist_input_addArtistEx = dpg.add_input_text(label="Ex Artist")
                    self.ui_dataArtist_input_addArtistJp = dpg.add_input_text(label="Jp Artist")
                    self.ui_dataArtist_button_addArtistToDb = dpg.add_button(label="Add artist to database",
                                    callback=self.InsertDataToDb, user_data=data.artist)
                    dpg.add_same_line()
                    self.ui_dataTrack_button_showArtistTable = dpg.add_button(label="Show track artist table",
                                    callback=self.DisplayTable, user_data=data.artist)
                with dpg.tab(label="Track Name"):
                    dpg.add_text("Track Name")
                    self.ui_dataTrack_input_addTrackId = dpg.add_input_int(label="Track ID", max_value=9999, min_value=0,
                                       step_fast=100, callback=self.GetDataFromDb, user_data=data.track)
                    self.ui_dataTrack_input_addTrackEx = dpg.add_input_text(label="Ex Track")
                    self.ui_dataTrack_input_addTrackJp = dpg.add_input_text(label="Jp Track")
                    self.ui_dataTrack_button_addTrackNameToDb = dpg.add_button(label="Add track name to database",
                                    callback=self.InsertDataToDb, user_data=data.track)
                    dpg.add_same_line()
                    self.ui_dataTrack_button_showTrackNameTable = dpg.add_button(label="Show track name table",
                                    callback=self.DisplayTable, user_data=data.track)
                with dpg.tab(label="Designer Name"):
                    dpg.add_text("Designer Name")
                    self.ui_dataDesigner_input_addDesignerId = dpg.add_input_int(label="Designer ID", max_value=99,
                                       min_value=0, step_fast=10, callback=self.GetDataFromDb,
                                       user_data=data.designer)
                    self.ui_dataDesigner_input_addDesignerEx = dpg.add_input_text(label="Ex Designer")
                    self.ui_dataDesigner_input_addDesignerJp = dpg.add_input_text(label="Jp Designer")
                    self.ui_dataDesigner_button_addDesignerToDb = dpg.add_button(label="Add designer to database",
                                    callback=self.InsertDataToDb, user_data=data.designer)
                    dpg.add_same_line()
                    self.ui_dataDesigner_button_showDesignerTable = dpg.add_button(label="Show score designer table",
                                    callback=self.DisplayTable, user_data=data.designer)

            self.ui_data_checkbox_replaceDbEntry = dpg.add_checkbox(label="Overwrite existing database entry")

        with dpg.window(label="Generate maimai Files") as self.ui_window_generateMaimaiFiles:
            dpg.add_text("Generate data files for maimai FiNALE")
            self.ui_generate_button_createFiles = dpg.add_button(label="Generate Files",
                            callback=self.GenerateAndEncryptFiles)
            self.ui_generate_checkbox_encryptFiles = dpg.add_checkbox(label="Encrypt Files", default_value=True)
            dpg.add_spacing(count=4)
            self.ui_generate_button_openOutputFolder = dpg.add_button(label="Open Output Folder",
                            callback=lambda: os.startfile(f"{os.getcwd()}/output"))

        # TODO Table Columns

        with dpg.window(label="mmMusic Grid", show=False) as self.ui_window_mmMusicDisplay:
            self.ui_table_mmMusic_input_filter = dpg.add_input_text(label="Filter", callback=lambda: self.FilterData(data.mmMusic))
            columns = ["track_id", "name", "ver", "subcate", "bpm", "sort_id", "dress", "darkness", "mile", "vl",
                       "event", "rec", "pvstart", "pvend", "song_duration", "off_ranking", "ad_def", "remaster",
                       "special_pv", "challenge_track", "bonus", "genre_id", "title", "artist", "sort_jp_index",
                       "sort_ex_index", "filename"]
            self.ui_table_mmMusic = dpg.add_table(height=0, width=0,
                           callback=lambda: [self.SelectTableRow("table_mmMusic"),
                                             dpg.set_value(self.ui_dataMmMusic_input_addTrackId,
                                                            int(self.GetFirstSelectedCellValue("table_mmMusic"))),
                                             self.GetDataFromDb("", data.mmMusic)])

        with dpg.window(label="mmScore Grid", show=False) as self.ui_window_mmScoreDisplay:
            columns = ["track_id", "name", "lv", "designer_id", "utage_mode", "safename"]
            self.ui_table_mmScore = dpg.add_table(height=0, width=0,
                           callback=lambda: [self.SelectTableRow("table_mmScore"),
                                             dpg.set_value(self.ui_dataMmScore_input_addTrackId,
                                                            int(self.GetFirstSelectedCellValue("table_mmScore")[:-2])),
                                             self.GetDataFromDb("", data.mmScore)])

        with dpg.window(label="Artist Name Grid", show=False) as self.ui_window_textoutArtistDisplay:
            columns = ["artist_id", "ex_artist_title", "jp_artist_title"]
            self.ui_table_textoutArtist = dpg.add_table(height=0, width=0,
                           callback=lambda: [self.SelectTableRow("table_textoutArtist"),
                                             dpg.set_value(self.ui_dataArtist_input_addArtistId,
                                                            int(self.GetFirstSelectedCellValue("table_textoutArtist"))),
                                             self.GetDataFromDb("", data.artist)])

        with dpg.window(label="Track Name Grid", show=False) as self.ui_window_textoutTrackDisplay:
            columns = ["track_id", "ex_track_title", "jp_track_title"]
            self.ui_table_textoutTrack = dpg.add_table(height=0, width=0,
                           callback=lambda: [self.SelectTableRow("table_textoutTrack"),
                                             dpg.set_value(self.ui_dataTrack_input_addTrackId,
                                                            int(self.GetFirstSelectedCellValue("table_textoutTrack"))),
                                             self.GetDataFromDb("", data.track)])

        with dpg.window(label="Track Designer Grid", show=False) as self.ui_window_textoutDesignerDisplay:
            columns = ["designer_id", "ex_designer_name", "jp_designer_name"]
            self.ui_table_textoutDesigner = dpg.add_table(height=0, width=0,
                           callback=lambda: [self.SelectTableRow("table_textoutDesigner"),
                                             dpg.set_value(self.ui_dataDesigner_input_addDesignerId,
                                                            int(self.GetFirstSelectedCellValue(
                                                                "table_textoutDesigner"))),
                                             self.GetDataFromDb("", data.designer)])

        with dpg.window(label="Sound BGM Grid", show=False) as self.ui_window_soundBgmDisplay:
            columns = ["track_id", "title"]
            self.ui_table_soundBgm = dpg.add_table(height=0, width=0,
                           callback=lambda: [self.SelectTableRow("table_soundBgm"),
                                             dpg.set_value(self.ui_dataSoundBgm_input_addTrackId,
                                                            int(self.GetFirstSelectedCellValue("table_soundBgm"))),
                                             self.GetDataFromDb("", data.soundBgm)])

        with dpg.window(label="Log") as self.ui_window_log:
            self.ui_log_input_log = dpg.add_input_text(label="", multiline=True, readonly=True, width=600, height=1200)
            dpg.add_same_line()
            self.ui_log_button_clearLog = dpg.add_button(label="Clear", callback=lambda: dpg.set_value(self.ui_log_input_log, ""))

        dpg.enable_docking(dock_space=True)

        # TODO Fix these

        # dpg.add_additional_font("NotoSerifCJKjp-Medium.otf", 20, "japanese")

        dpg.set_start_callback(self.OnStart)
        # dpg.set_render_callback(self.MainCallback)
        dpg.set_exit_callback(self.OnExit)

        self.load_layout(self.GetCurrentWindowNames())

        # dpg.set_main_window_title("maimaiTool")
        dpg.start_dearpygui()

    def InsertDataToDb(self, sender, data):
        tempConn = CreateConnection(self.db)
        insert = hlp.DataContainers()

        if data == insert.artist:
            artistId = hlp.AffixZeroesToString(dpg.get_value(self.ui_dataArtist_input_addArtistId), 4)
            artistEx = dpg.get_value(self.ui_dataArtist_input_addArtistEx)
            artistJp = dpg.get_value(self.ui_dataArtist_input_addArtistJp)

            if artistId == "":
                return

            if not (dba.InsertLineToTextOutArtist(tempConn, [artistId, artistEx, artistJp])):
                if dpg.get_value(self.ui_data_checkbox_replaceDbEntry):
                    dba.ReplaceLineInTextOutArtist(tempConn, [artistId, artistEx, artistJp])
                    self.AppendLog("Entry replaced")
                else:
                    self.AppendLog("Entry already exists")
            else:
                self.AppendLog("Entry added")

        elif data == insert.track:
            trackId = hlp.AffixZeroesToString(dpg.get_value(self.ui_dataTrack_input_addTrackId), 4)
            trackEx = dpg.get_value(self.ui_dataTrack_input_addTrackEx)
            trackJp = dpg.get_value(self.ui_dataTrack_input_addTrackJp)

            if trackId == "":
                return

            if not (dba.InsertLineToTextOutTrack(tempConn, [trackId, trackEx, trackJp])):
                if dpg.get_value(self.ui_data_checkbox_replaceDbEntry):
                    dba.ReplaceLineInTextOutTrack(tempConn, [trackId, trackEx, trackJp])
                    self.AppendLog("Entry replaced")
                else:
                    self.AppendLog("Entry already exists")
            else:
                self.AppendLog("Entry added")

        elif data == insert.designer :
            designerId = hlp.AffixZeroesToString(dpg.get_value(self.ui_dataDesigner_input_addDesignerId), 4)
            designerEx = dpg.get_value(self.ui_dataDesigner_input_addDesignerEx)
            designerJp = dpg.get_value(self.ui_dataDesigner_input_addDesignerJp)

            if designerId == "":
                return

            if not (dba.InsertLineToTextOutDesigner(tempConn, [designerId, designerEx, designerJp])):
                if dpg.get_value(self.ui_data_checkbox_replaceDbEntry):
                    dba.ReplaceLineInTextOutDesigner(tempConn, [designerId, designerEx, designerJp])
                    self.AppendLog("Entry replaced")
                else:
                    self.AppendLog("Entry already exists")
            else:
                self.AppendLog("Entry added")

        elif data == insert.mmMusic:
            trackId = dpg.get_value(self.ui_dataMmMusic_input_addTrackId)

            if trackId == "":
                return

            name = f"eMusic_{hlp.AffixZeroesToString(trackId, 3)}"
            version = dpg.get_value(self.ui_dataMmMusic_input_addVersion)
            subcate = "30"
            bpm = f'{round(dpg.get_value(self.ui_dataMmMusic_input_addBpm), 3):g}'
            sortId = dpg.get_value(self.ui_dataMmMusic_input_addSortId)
            dress = "0"
            darkness = "0"
            mile = "0"
            videoBool = hlp.BoolToValueReversed(dpg.get_value(self.ui_dataMmMusic_checkbox_addHasVideo))
            event = "0"
            rec = "1"
            pvStart = f'{round(dpg.get_value(self.ui_dataMmMusic_input_addPvStart), 2):g}'
            pvEnd = f'{round(dpg.get_value(self.ui_dataMmMusic_input_addPvEnd), 2):g}'
            songDuration = "0"
            offRanking = "0"
            adDef = "0"
            remaster = dpg.get_value(self.ui_dataMmMusic_input_addRemaster)
            specialPv = "0"
            challengeTrack = "0"
            bonus = "0"
            genreId = hlp.GenreTextToFinaleValue(dpg.get_value(self.ui_dataMmMusic_combo_addGenreId))
            titleId = hlp.AffixZeroesToString(dpg.get_value(self.ui_dataMmMusic_input_addTitleId), 4)
            artistId = hlp.AffixZeroesToString(dpg.get_value(self.ui_dataMmMusic_input_addArtistId), 4)
            sortIndexJp = dpg.get_value(self.ui_dataMmMusic_input_addSortJpIndex)
            sortIndexEx = dpg.get_value(self.ui_dataMmMusic_input_addSortExIndex)
            filename = dpg.get_value(self.ui_dataMmMusic_input_addFilename).lower()

            subcate = dpg.get_value(self.ui_dataMmMusic_hidden_subcate)
            dress = dpg.get_value(self.ui_dataMmMusic_hidden_dress)
            darkness = dpg.get_value(self.ui_dataMmMusic_hidden_darkness)
            mile = dpg.get_value(self.ui_dataMmMusic_hidden_mile)

            event = dpg.get_value(self.ui_dataMmMusic_hidden_event)
            rec = dpg.get_value(self.ui_dataMmMusic_hidden_rec)
            songDuration = dpg.get_value(self.ui_dataMmMusic_hidden_songDuration)
            offRanking = dpg.get_value(self.ui_dataMmMusic_hidden_offRanking)

            adDef = dpg.get_value(self.ui_dataMmMusic_hidden_adDef)
            specialPv = dpg.get_value(self.ui_dataMmMusic_hidden_specialPv)
            challengeTrack = dpg.get_value(self.ui_dataMmMusic_hidden_challengeTrack)
            bonus = dpg.get_value(self.ui_dataMmMusic_hidden_bonus)

            data = [trackId, name, version, subcate, bpm, sortId, dress, darkness, mile, videoBool, event, rec
                , pvStart, pvEnd, songDuration, offRanking, adDef, remaster, specialPv, challengeTrack, bonus, genreId,
                    titleId, artistId, sortIndexJp, sortIndexEx, filename]

            if not (dba.InsertLineToMusic(tempConn, data)):
                if dpg.get_value(self.ui_data_checkbox_replaceDbEntry):
                    dba.ReplaceLineInMusic(tempConn, data)
                    self.AppendLog("Entry replaced")
                else:
                    self.AppendLog("Entry already exists")
            else:
                self.AppendLog("Entry added")

        elif data == insert.mmScore:
            trackId = dpg.get_value(self.ui_dataMmScore_input_addTrackId)

            if trackId == "":
                return

            # Get all rows where score id is not 0
            for i in range(1, 7, 1):
                if dpg.get_value(f"dataMmScore_input_addScoreId_0{i}") != 0:
                    scoreId = hlp.AffixZeroesToString(dpg.get_value(f"dataMmScore_input_addScoreId_0{i}"), 2)
                    lv = f'{round(dpg.get_value(f"dataMmScore_input_addDifficulty_0{i}"), 1):g}' # :g Removes trailing zeroes
                    designerId = dpg.get_value(f"dataMmScore_input_addDesignerId_0{i}")
                    utageMode = hlp.BoolToValueReversed(dpg.get_value(f"dataMmScore_checkbox_addIsInUtage_0{i}"))
                    baseSafename = dpg.get_value(self.ui_dataMmScore_input_addBaseSafename)

                    name = f"eScore_{hlp.AffixZeroesToString(trackId, 3)}_{baseSafename}_{scoreId}"
                    safename = f"{hlp.AffixZeroesToString(trackId, 3)}_{baseSafename}_{scoreId}"

                    trackAndScoreId = int(str(trackId) + scoreId)

                    data = [trackAndScoreId, name, lv, designerId, utageMode, safename]

                    if not (dba.InsertLineToScore(tempConn, data)):
                        if dpg.get_value(self.ui_data_checkbox_replaceDbEntry):
                            dba.ReplaceLineInScore(tempConn, data)
                            self.AppendLog(f"Entry {scoreId} replaced")
                        else:
                            self.AppendLog(f"Entry {scoreId} already exists")
                    else:
                        self.AppendLog(f"Entry {scoreId} added")

        elif data == insert.soundBgm:
            title = dpg.get_value(self.ui_dataSoundBgm_input_addTitle)
            trackId = dpg.get_value(self.ui_dataSoundBgm_input_addTrackId)

            if not (dba.InsertLineToSoundBgm(tempConn, [title, trackId])):
                if dpg.get_value(self.ui_data_checkbox_replaceDbEntry):
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
        get = hlp.DataContainers()

        if data == get.artist:
            artistId = hlp.AffixZeroesToString(dpg.get_value(self.ui_dataArtist_input_addArtistId), 4)
            row = dba.SelectMmTextoutArtistById(tempConn, artistId)

            if len(row) > 0:
                row = row[0]
                dpg.set_value(self.ui_dataArtist_input_addArtistEx, row[0])
                dpg.set_value(self.ui_dataArtist_input_addArtistJp, row[1])
            else:
                dpg.set_value(self.ui_dataArtist_input_addArtistEx, "")
                dpg.set_value(self.ui_dataArtist_input_addArtistJp, "")
        elif data == get.track:
            trackId = hlp.AffixZeroesToString(dpg.get_value(self.ui_dataTrack_input_addTrackId), 4)
            row = dba.SelectMmTextoutTrackById(tempConn, trackId)

            if len(row) > 0:
                row = row[0]
                dpg.set_value(self.ui_dataTrack_input_addTrackEx, row[0])
                dpg.set_value(self.ui_dataTrack_input_addTrackJp, row[1])
            else:
                dpg.set_value(self.ui_dataTrack_input_addTrackEx, "")
                dpg.set_value(self.ui_dataTrack_input_addTrackJp, "")
        elif data == get.designer:
            designerId = hlp.AffixZeroesToString(dpg.get_value(self.ui_dataDesigner_input_addDesignerId), 4)
            row = dba.SelectMmTextoutDesignerById(tempConn, designerId)

            if len(row) > 0:
                row = row[0]
                dpg.set_value(self.ui_dataDesigner_input_addDesignerEx, row[0])
                dpg.set_value(self.ui_dataDesigner_input_addDesignerJp, row[1])
            else:
                dpg.set_value(self.ui_dataDesigner_input_addDesignerEx, "")
                dpg.set_value(self.ui_dataDesigner_input_addDesignerJp, "")

        elif data == get.mmMusic:
            trackId = dpg.get_value(self.ui_dataMmMusic_input_addTrackId)
            row = dba.SelectMmMusicById(tempConn, trackId)

            if len(row) > 0:
                row = row[0]
                dgHelp.UpdateDataMmMusicFields(row)
            else:
                dgHelp.DefaultDataMmMusicFields()

        # Grabs all scores for the track id
        elif data == get.mmScore:
            trackId = dpg.get_value(self.ui_dataMmScore_input_addTrackId)
            rows = dba.SelectMmScoreById(tempConn, hlp.AffixZeroesToString(trackId, 3))

            # Reset fields first
            dgHelp.DefaultDataMmScoreFields()
            dgHelp.UpdateDataMmScoreFields(rows)

        elif data == get.soundBgm:
            trackId = hlp.AffixZeroesToString(dpg.get_value(self.ui_dataSoundBgm_input_addTrackId), 3)
            row = dba.SelectSoundBgmById(tempConn, trackId)

            if len(row) > 0:
                row = row[0]
                dpg.set_value(self.ui_dataSoundBgm_input_addTitle, row[0])
            else:
                dpg.set_value(self.ui_dataSoundBgm_input_addTitle, "")
        else:
            self.AppendLog("wip")

        tempConn.close()

    # TODO Currently only supports Murasaki
    def ImportData(self):
        types = hlp.DataContainers()

        dpg.set_value(self.ui_dataMmMusic_input_addTrackId, dpg.get_value(self.ui_import_input_importTrackId))
        dpg.set_value(self.ui_dataMmScore_input_addTrackId, dpg.get_value(self.ui_import_input_importTrackId))

        # mmMusic
        dgHelp.UpdateDataMmMusicFields(cvrt.ConvertSplitMmMusicLineFromMurasakiToFinale(
                readDat.ReadMmMusicSingleLine(dpg.get_value(self.ui_filesMurasaki_input_mmMusic),
                                              dpg.get_value(self.ui_import_input_importTrackId))))

        # mmScore
        dgHelp.DefaultDataMmScoreFields()
        dgHelp.UpdateDataMmScoreFields(readDat.ReadMmScoreLinesWithTrackId(dpg.get_value(self.ui_filesMurasaki_input_mmScore), dpg.get_value(self.ui_import_input_importTrackId)))

        # Track name
        # TODO This should check that track id has updated in the mmMusic field
        trackExName = readDat.ReadMmTextoutLineWithId(dpg.get_value(self.ui_filesMurasaki_input_mmTextoutEx), dpg.get_value(self.ui_dataMmMusic_input_addTitleId), types.track)
        trackJpName = readDat.ReadMmTextoutLineWithId(dpg.get_value(self.ui_filesMurasaki_input_mmTextoutJp), dpg.get_value(self.ui_dataMmMusic_input_addTitleId), types.track)
        dgHelp.UpdateDataTrackNameFields([dpg.get_value(self.ui_dataMmMusic_input_addTitleId), trackExName, trackJpName])

        self.AppendLog("Data imported")

    def FilterData(self, table):
        tempConn = CreateConnection(self.db)
        filters = hlp.DataContainers()

        if table == filters.mmMusic:
            keyword = dpg.get_value(self.ui_table_mmMusic_input_filter)
            rows = dba.SelectMmMusicByLikeFilename(tempConn, keyword)
            if len(rows) > 0:
                dpg.clear_table("table_mmMusic")
                for row in rows:
                    dpg.add_row("table_mmMusic", row)

        tempConn.close()


    def AppendLog(self, text):
        dpg.set_value(self.ui_log_input_log,
                       f"{dpg.get_value(self.ui_log_input_log)}{datetime.datetime.now().strftime('%H:%M:%S')} - {text}\n")

    def MainCallback(self):
        dpg.set_item_width("log_input_log", dpg.get_drawing_size("window_log")[0] - 100)
        dpg.set_item_height("log_input_log", dpg.get_drawing_size("window_log")[1] - 35)

    def OnStart(self):
        pass

        # This doesn't set the main window size properly, when called from OnStart()
        # self.load_layout(self.GetCurrentWindowNames())

    def OnExit(self):
        self.save_layout(self.GetCurrentWindowNames())

    # TODO Rename
    def save_layout(self, windows):
        with open(os.getcwd() + "\\config.ini", "r+") as f:
            if not self.config.has_section("Layout"):
                self.config["Layout"] = {}
            #for window in windows:
            #    self.config["Layout"][
            #        window + "_pos"] = f"{str(dpg.get_window_pos(window)[0])}, {str(dpg.get_window_pos(window)[1])}"
            #    self.config["Layout"][
            #        window + "_size"] = f"{str(dpg.get_drawing_size(window)[0])}, {str(dpg.get_drawing_size(window)[1])}"
            #self.config["Layout"][
            #    "MainWindow"] = f"{str(dpg.get_main_window_size()[0])}, {str(dpg.get_main_window_size()[1])}"

            supportedVersions = ["Finale", "Murasaki"]

            for version in supportedVersions:
                for name, file in dgHelp.GetMaimaiFilesFromInput(version).items():
                    if file:
                        self.config[f"Files{version}"][name] = file

            self.config.write(f)

    def load_layout(self, windows):
        #if self.config.has_section("Layout"):
        #    for window in windows:
        #        try:
        #            pos = self.config["Layout"][window + "_pos"].split(", ")
        #            size = self.config["Layout"][window + "_size"].split(", ")
                    # dpg.set_window_pos(window, int(pos[0]), int(pos[1]))
                    # dpg.set_drawing_size(window, int(size[0]), int(size[1]))
        #        except KeyError as e:
        #            print(f"KeyError: {e}")
        #    size = self.config["Layout"]["MainWindow"].split(", ")
            # dpg.set_main_window_size(int(size[0]), int(size[1]))

        supportedVersions = ["Finale", "Murasaki"]

        for version in supportedVersions:
            files = []

            files.append(self.config[f"Files{version}"]["mmMusic"])
            files.append(self.config[f"Files{version}"]["mmScore"])
            files.append(self.config[f"Files{version}"]["mmTextoutEx"])
            files.append(self.config[f"Files{version}"]["mmTextoutJp"])
            files.append(self.config[f"Files{version}"]["soundBgm"])

            # dgHelp.SetMaimaiFilesFromConfig(version, files)

    def GetCurrentWindowNames(self):
        windows = dpg.get_windows()
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
