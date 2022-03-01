import os
import datetime
import tkinter
import shutil
import configparser
from tkinter import filedialog
from src import Convert as cvrt, \
    GenerateData as genDat, ReadData as readDat, Helpers as hlp
from src.GUI import DearGuiHelper as dgHelp
from src.Encryption import MaiCrypt
from src.Database import DatabaseActions as dba, DatabaseFormat
import dearpygui.dearpygui as dpg

# TODO Display all unused track ids
# TODO Function to check all data connections for an id
# TODO Import all required data from other maimai versions based on mmusic id
# TODO Support for mmMusic event field
# TODO Dynamic row adding for mmScore entries
# TODO Load files into db should always create a new db file
# TODO Make sort id easier to understand/automatic (01 -> a, 02 -> b, etc)


def LoadFilesIntoNewDb(path, db):
    if not db:
        return

    conn = dba.CreateConnection(db)

    dba.InitDb(conn)

    readDat.ReadMmMusic(conn, path)
    readDat.ReadMmScore(conn, path)
    readDat.ReadTextOutEx(conn, path)
    readDat.ReadTextOutJp(conn, path)
    readDat.ReadSoundBgm(conn, path)

    conn.close()


def DecryptFilesInInput():
    with open(f"{os.getcwd()}/key.txt", "r") as f:
        key = f.readline()

    crypt = MaiCrypt.MaiFinaleCrypt(key)

    if not os.path.isdir(f"{os.getcwd()}/input/decrypted"):
        os.mkdir(f"{os.getcwd()}/input/decrypted")

    for file in os.listdir(f"{os.getcwd()}/input"):
        if file != "SoundBGM.txt" and not os.path.isdir(f"{os.getcwd()}/input/{file}") and file.endswith(".bin"):
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


class GUI:
    def __init__(self):
        hlp.CreateWorkDirectories()

        self.config = configparser.ConfigParser()
        self.config.read(InitConfig())

        self.db = self.config["Database"]["Name"]
        conn = dba.CreateConnection(self.db)
        dba.InitDb(conn)
        conn.close()

        self.ActivateDisplay()

    def DisplayTable(self, sender, app_data, user_data):
        # Callbacks run on a separate thread, sqlite doesn't like that
        tempConn = dba.CreateConnection(self.db)
        table = hlp.CommonData

        data = user_data

        if data == table.mmMusic:
            lines = dba.SelectMmMusic(tempConn)
            dpg.show_item(self.ui_window_mmMusicDisplay)

            dgHelp.FillTable(self.ui_table_mmMusic, lines)

        elif data == table.mmScore:
            lines = dba.SelectMmScore(tempConn)
            dpg.show_item(self.ui_window_mmScoreDisplay)

            dgHelp.FillTable(self.ui_table_mmScore, lines)

        elif data == table.artist:
            lines = dba.SelectMmTextoutArtist(tempConn)
            dpg.show_item(self.ui_window_textoutArtistDisplay)

            dgHelp.FillTable(self.ui_table_textoutArtist, lines)

        elif data == table.track:
            lines = dba.SelectMmTextoutTrack(tempConn)
            dpg.show_item(self.ui_window_textoutTrackDisplay)

            dgHelp.FillTable(self.ui_table_textoutTrack, lines)

        elif data == table.designer:
            lines = dba.SelectMmTextoutDesigner(tempConn)
            dpg.show_item(self.ui_window_textoutDesignerDisplay)

            dgHelp.FillTable(self.ui_table_textoutDesigner, lines)

        elif data == table.soundBgm:
            lines = dba.SelectSoundBgmOrderId(tempConn)
            dpg.show_item(self.ui_window_soundBgmDisplay)

            dgHelp.FillTable(self.ui_table_soundBgm, lines)

        else:
            pass

        tempConn.close()

    def DatabaseAccess(self, action):
        root = tkinter.Tk()
        root.withdraw()

        if action == "create":
            file = filedialog.asksaveasfilename(title=f"Create New Database", filetypes=[("Database files", "*.db")])
        else:  # load
            file = filedialog.askopenfilename(title=f"Load Database", filetypes=[("Database files", "*.db")])

        if not file:
            return None

        if not file.endswith(".db"):
            file = f"{file}.db"

        dpg.set_value(self.ui_filesFinale_input_dbName, file)
        self.db = file

        return file

    def SelectMaimaiFolder(self, version):
        root = tkinter.Tk()
        root.withdraw()
        folder = filedialog.askdirectory(title=f"Select maimai {version} folder")

        if version == "Finale":
            for dirpath, dirnames, filenames in os.walk(folder):
                if "maimai" not in dirpath:
                    continue
                for filename in filenames:
                    if filename == "SoundBGM.txt":
                        dpg.set_value(self.ui_filesFinale_input_soundBgm, f"{dirpath}/SoundBGM.txt")
                        shutil.copy(f"{dirpath}/SoundBGM.txt", f"{os.getcwd()}/input/SoundBGM.txt")
                    if filename == "mmMusic.bin":
                        dpg.set_value(self.ui_filesFinale_input_mmMusic, f"{dirpath}/mmMusic.bin")
                        shutil.copy(f"{dirpath}/mmMusic.bin", f"{os.getcwd()}/input/mmMusic.bin")
                    if filename == "mmScore.bin":
                        dpg.set_value(self.ui_filesFinale_input_mmScore, f"{dirpath}/mmScore.bin")
                        shutil.copy(f"{dirpath}/mmScore.bin", f"{os.getcwd()}/input/mmScore.bin")
                    if filename == "mmtextout_ex.bin":
                        dpg.set_value(self.ui_filesFinale_input_mmTextoutEx, f"{dirpath}/mmtextout_ex.bin")
                        shutil.copy(f"{dirpath}/mmtextout_ex.bin", f"{os.getcwd()}/input/mmtextout_ex.bin")
                    if filename == "mmtextout_jp.bin":
                        dpg.set_value(self.ui_filesFinale_input_mmTextoutJp, f"{dirpath}/mmtextout_jp.bin")
                        shutil.copy(f"{dirpath}/mmtextout_jp.bin", f"{os.getcwd()}/input/mmtextout_jp.bin")

        elif version == "Murasaki":  # Don't copy files, as they don't need to be decrypted or modified
            for dirpath, dirnames, filenames in os.walk(folder):
                if "maimai" not in dirpath:
                    continue
                for filename in filenames:
                    if filename == "SoundBGM.txt":
                        dpg.set_value(self.ui_filesMurasaki_input_soundBgm, f"{dirpath}/SoundBGM.txt")
                    if filename == "mmMusic.tbl":
                        dpg.set_value(self.ui_filesMurasaki_input_mmMusic, f"{dirpath}/mmMusic.tbl")
                    if filename == "mmScore.tbl":
                        dpg.set_value(self.ui_filesMurasaki_input_mmScore, f"{dirpath}/mmScore.tbl")
                    if filename == "mmtextout_ex.tbl":
                        dpg.set_value(self.ui_filesMurasaki_input_mmTextoutEx, f"{dirpath}/mmtextout_ex.tbl")
                    if filename == "mmtextout_jp.tbl":
                        dpg.set_value(self.ui_filesMurasaki_input_mmTextoutJp, f"{dirpath}/mmtextout_jp.tbl")
        elif version == "Green":
            pass

    def GenerateAndEncryptFiles(self):
        genDat.GenerateFilesFromDb(self.db)
        self.AppendLog("Files created")

        if not dpg.get_value(self.ui_generate_checkbox_encryptFiles):
            return

        EncryptFilesInOutput()
        self.AppendLog("Encryption complete")

    # TODO Broken in new DPG versions
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

    # TODO Broken in new DPG versions
    def GetFirstSelectedCellValue(self, table):
        return dpg.get_table_item(table, dpg.get_table_selections(table)[0][0],
                                  dpg.get_table_selections(table)[0][1])

    def ActivateDisplay(self):
        dpg.create_context()
        dpg.create_viewport(title="Otohime - maimai FiNALE songlist editor")
        dpg.setup_dearpygui()

        data = hlp.CommonData

        with dpg.window(label="Select maimai files") as ui_window_selectMaimaiFiles:
            with dpg.tab_bar(label="maimai Versions"):
                with dpg.tab(label="FiNALE"):
                    dpg.add_spacer(height=5)
                    self.ui_filesFinale_button_selectMaimaiFolder = dpg.add_button(label="Select maimai FiNALE folder",
                                                                                   callback=lambda: self.SelectMaimaiFolder(
                                                                                       "Finale"), width=220, height=25)
                    dpg.add_spacer(height=5)
                    self.ui_filesFinale_input_mmMusic = dpg.add_input_text(label="mmMusic.bin")
                    self.ui_filesFinale_input_mmScore = dpg.add_input_text(label="mmScore.bin")
                    self.ui_filesFinale_input_mmTextoutEx = dpg.add_input_text(label="mmTextoutEx.bin")
                    self.ui_filesFinale_input_mmTextoutJp = dpg.add_input_text(label="mmTextoutJp.bin")
                    self.ui_filesFinale_input_soundBgm = dpg.add_input_text(label="soundBGM.txt")
                    dpg.add_spacer(height=5)
                    self.ui_filesFinale_button_decryptFiles = dpg.add_button(label="Decrypt Files",
                                                                             callback=DecryptFilesInInput, width=220, height=25)
                    self.ui_filesFinale_button_createDatabaseFromFiles = dpg.add_button(
                        label="Create Database From Files",
                        callback=lambda: LoadFilesIntoNewDb(f"{os.getcwd()}/input", self.DatabaseAccess("create")), width=220, height=25)
                    dpg.add_spacer(width=7)
                    self.ui_filesFinale_input_dbName = dpg.add_input_text(label="Current Database")
                    dpg.add_spacer(height=5)
                    self.ui_filesFinale_button_changeDb = dpg.add_button(label="Change Database",
                                                                         callback=lambda: self.DatabaseAccess("load"), width=220, height=25)
                    dpg.set_value(self.ui_filesFinale_input_dbName, self.db)

                with dpg.tab(label="Murasaki"):
                    dpg.add_spacer(height=5)
                    self.ui_filesMurasaki_button_selectMaimaiFolder = dpg.add_button(
                        label="Select maimai Murasaki folder",
                        callback=lambda: self.SelectMaimaiFolder("Murasaki"), width=220, height=25)
                    dpg.add_spacer(height=5)
                    self.ui_filesMurasaki_input_mmMusic = dpg.add_input_text(label="mmMusic.tbl")
                    self.ui_filesMurasaki_input_mmScore = dpg.add_input_text(label="mmScore.tbl")
                    self.ui_filesMurasaki_input_mmTextoutEx = dpg.add_input_text(label="mmTextoutEx.tbl")
                    self.ui_filesMurasaki_input_mmTextoutJp = dpg.add_input_text(label="mmTextoutJp.tbl")
                    self.ui_filesMurasaki_input_soundBgm = dpg.add_input_text(label="soundBGM.txt")
                # with dpg.tab(label="Green"):
                #     pass
        with dpg.window(label="Import maimai data from older versions") as self.ui_window_importMaimaiData:
            self.ui_import_input_importTrackId = dpg.add_input_int(min_value=0, step_fast=10, max_value=99999,
                                                                   label="Track Id", default_value=0, min_clamped=True)
            self.ui_import_combo_importVersion = dpg.add_combo(label="Import from version",
                                                               items=["maimai Murasaki"],
                                                               #items=["maimai Murasaki", "maimai Green"],
                                                               default_value="maimai Murasaki")
            self.ui_import_button_importTrackId = dpg.add_button(label="Import data", callback=self.ImportData)

        with dpg.window(label="Edit maimai FiNALE data") as self.ui_window_editMaimaiData:
            with dpg.tab_bar(label="Data Types"):
                # TODO add tips

                # -----------------------------------------------------------------------------------------------------#

                with dpg.tab(label="mmMusic"):
                    dpg.add_text("mmMusic")
                    self.ui_dataMmMusic_input_addTrackId = dpg.add_input_int(label="Track ID", max_value=999,
                                                                             min_value=0,
                                                                             step_fast=100, callback=self.GetDataFromDb,
                                                                             user_data=data.mmMusic, min_clamped=True)
                    # name
                    self.ui_dataMmMusic_input_addVersion = dpg.add_input_int(label="Version", max_value=99999,
                                                                             min_value=0,
                                                                             step_fast=1000, default_value=10000)
                    # subcate -> 30
                    self.ui_dataMmMusic_input_addBpm = dpg.add_input_float(label="BPM", max_value=999.999,
                                                                           format="%.3f",
                                                                           min_value=0, step=1.0, step_fast=10.0)
                    self.ui_dataMmMusic_input_addSortId = dpg.add_input_int(label="Sort Id", max_value=999999,
                                                                            min_value=0,
                                                                            step=10, step_fast=1000,
                                                                            default_value=300000)
                    # dress -> 0
                    # darkness -> 0
                    # mile -> 0
                    self.ui_dataMmMusic_checkbox_addHasVideo = dpg.add_checkbox(label="Track has video file")
                    # event -> 0
                    # rec -> 1
                    self.ui_dataMmMusic_input_addPvStart = dpg.add_input_float(label="PV Start", max_value=999.99,
                                                                               step_fast=10.0, step=1.0, format="%.2f",
                                                                               min_value=0.00)
                    self.ui_dataMmMusic_input_addPvEnd = dpg.add_input_float(label="PV End", max_value=999.99,
                                                                             step_fast=10.0,
                                                                             step=1.0, format="%.2f", min_value=0.00)
                    # song duration -> 0
                    # off_rank -> 0
                    # ad_def -> 0
                    self.ui_dataMmMusic_input_addRemaster = dpg.add_input_int(label="Remaster", max_value=99999999,
                                                                              min_value=0, step=1, step_fast=10000000,
                                                                              default_value=99999999)
                    # special_pv -> 0
                    # challenge_track -> 0
                    # bonus -> 0
                    self.ui_dataMmMusic_combo_addGenreId = dpg.add_combo(label="Genre",
                                                                         items=["Pops & Anime", "niconico & Vocaloid",
                                                                                "Touhou Project", "Sega",
                                                                                "Game & Variety", "Original & Joypolis",
                                                                                "None"], default_value="Pops & Anime")
                    self.ui_dataMmMusic_input_addTitleId = dpg.add_input_int(label="Title Id", max_value=9999,
                                                                             min_value=0,
                                                                             step_fast=100)
                    self.ui_dataMmMusic_input_addArtistId = dpg.add_input_int(label="Artist Id", max_value=9999,
                                                                              min_value=0,
                                                                              step_fast=100)
                    self.ui_dataMmMusic_input_addSortJpIndex = dpg.add_input_int(label="Sort Index JP",
                                                                                 max_value=999999,
                                                                                 min_value=0, step_fast=10000, step=1)
                    self.ui_dataMmMusic_input_addSortExIndex = dpg.add_input_int(label="Sort Index EX",
                                                                                 max_value=999999,
                                                                                 min_value=0, step_fast=10000, step=1)
                    self.ui_dataMmMusic_input_addFilename = dpg.add_input_text(label="Filename")

                    dpg.add_spacer(height=5)
                    with dpg.group(horizontal=True):
                        self.ui_dataMmMusic_button_showMmMusicTable = dpg.add_button(label="Show music table",
                                                                                 callback=self.DisplayTable,
                                                                                 user_data=data.mmMusic, width=200, height=25)
                        self.ui_dataMmMusic_button_addTrackToDb = dpg.add_button(label="Add track to database",
                                                                             callback=self.InsertDataToDb,
                                                                             user_data=data.mmMusic, width=200, height=25)

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

                # -----------------------------------------------------------------------------------------------------#

                with dpg.tab(label="mmScore"):
                    dpg.add_text("mmScore")
                    self.ui_dataMmScore_input_addTrackId = dpg.add_input_int(label="Track ID", max_value=999,
                                                                             min_value=0,
                                                                             step_fast=100, default_value=0,
                                                                             callback=self.GetDataFromDb,
                                                                             user_data=data.mmScore)
                    with dpg.group(horizontal=True):
                        dpg.add_text("Score Id")
                        dpg.add_text("Difficulty")
                        dpg.add_text("Score Designer Id")

                    self.ui_dataMmScore_input_addScoreId = []
                    self.ui_dataMmScore_input_addDifficulty = []
                    self.ui_dataMmScore_input_addDesignerId = []
                    self.ui_dataMmScore_checkbox_addIsInUtage = []

                    for i in range(1, 7, 1):
                        with dpg.group(horizontal=True):
                            self.ui_dataMmScore_input_addScoreId.append(
                                dpg.add_input_int(label="", min_value=0, max_value=99, step_fast=10, width=100,
                                                  default_value=0))

                            self.ui_dataMmScore_input_addDifficulty.append(dpg.add_input_float(label="", max_value=99.9,
                                                                                               format="%.1f",
                                                                                               min_value=0, step=0.1,
                                                                                               step_fast=1.0,
                                                                                               width=100))

                            self.ui_dataMmScore_input_addDesignerId.append(dpg.add_input_int(label="", max_value=99,
                                                                                             min_value=0, step_fast=10,
                                                                                             width=100))

                            self.ui_dataMmScore_checkbox_addIsInUtage.append(dpg.add_checkbox(label="In Utage"))

                    self.ui_dataMmScore_input_addBaseSafename = dpg.add_input_text(label="Score Basename")

                    dpg.add_spacer(height=5)
                    with dpg.group(horizontal=True):
                        self.ui_dataMmScore_button_addScoreToDb = dpg.add_button(label="Add score to database",
                                                                                 callback=self.InsertDataToDb,
                                                                                 user_data=data.mmScore, width=200, height=25)

                        self.ui_dataMmScore_button_showMmScoreTable = dpg.add_button(label="Show score table",
                                                                                     callback=self.DisplayTable,
                                                                                     user_data=data.mmScore, width=200, height=25)

                # -----------------------------------------------------------------------------------------------------#

                with dpg.tab(label="Sound BGM"):
                    dpg.add_text("Sound BGM")
                    self.ui_dataSoundBgm_input_addTrackId = dpg.add_input_int(label="Track ID", max_value=999,
                                                                              min_value=0,
                                                                              step_fast=100,
                                                                              callback=self.GetDataFromDb,
                                                                              user_data=data.soundBgm)
                    self.ui_dataSoundBgm_input_addTitle = dpg.add_input_text(label="Track Filename")

                    dpg.add_spacer(height=5)
                    with dpg.group(horizontal=True):
                        self.ui_dataSoundBgm_button_addSoundBgmToDB = dpg.add_button(label="Add sound bgm to database",
                                                                                     callback=self.InsertDataToDb,
                                                                                     user_data=data.soundBgm, width=200, height=25)

                        self.ui_dataMmScore_button_showSoundBgmTable = dpg.add_button(label="Show sound table",
                                                                                      callback=self.DisplayTable,
                                                                                      user_data=data.soundBgm, width=200, height=25)

                # -----------------------------------------------------------------------------------------------------#

                with dpg.tab(label="Artist"):
                    dpg.add_text("Artist")
                    self.ui_dataArtist_input_addArtistId = dpg.add_input_int(label="Artist ID", max_value=9999,
                                                                             min_value=0,
                                                                             step_fast=100, callback=self.GetDataFromDb,
                                                                             user_data=data.artist)
                    self.ui_dataArtist_input_addArtistEx = dpg.add_input_text(label="Ex Artist")
                    self.ui_dataArtist_input_addArtistJp = dpg.add_input_text(label="Jp Artist")

                    dpg.add_spacer(height=5)
                    with dpg.group(horizontal=True):
                        self.ui_dataArtist_button_addArtistToDb = dpg.add_button(label="Add artist to database",
                                                                                 callback=self.InsertDataToDb,
                                                                                 user_data=data.artist, width=200, height=25)
                        self.ui_dataTrack_button_showArtistTable = dpg.add_button(label="Show track artist table",
                                                                                  callback=self.DisplayTable,
                                                                                  user_data=data.artist, width=200, height=25)

                # -----------------------------------------------------------------------------------------------------#

                with dpg.tab(label="Track Name"):
                    dpg.add_text("Track Name")
                    self.ui_dataTrack_input_addTrackId = dpg.add_input_int(label="Track ID", max_value=9999,
                                                                           min_value=0,
                                                                           step_fast=100, callback=self.GetDataFromDb,
                                                                           user_data=data.track)
                    self.ui_dataTrack_input_addTrackEx = dpg.add_input_text(label="Ex Track")
                    self.ui_dataTrack_input_addTrackJp = dpg.add_input_text(label="Jp Track")

                    dpg.add_spacer(height=5)
                    with dpg.group(horizontal=True):
                        self.ui_dataTrack_button_addTrackNameToDb = dpg.add_button(label="Add track name to database",
                                                                                   callback=self.InsertDataToDb,
                                                                                   user_data=data.track, width=200, height=25)

                        self.ui_dataTrack_button_showTrackNameTable = dpg.add_button(label="Show track name table",
                                                                                     callback=self.DisplayTable,
                                                                                     user_data=data.track, width=200, height=25)

                # -----------------------------------------------------------------------------------------------------#

                with dpg.tab(label="Designer Name"):
                    dpg.add_text("Designer Name")
                    self.ui_dataDesigner_input_addDesignerId = dpg.add_input_int(label="Designer ID", max_value=99,
                                                                                 min_value=0, step_fast=10,
                                                                                 callback=self.GetDataFromDb,
                                                                                 user_data=data.designer)
                    self.ui_dataDesigner_input_addDesignerEx = dpg.add_input_text(label="Ex Designer")
                    self.ui_dataDesigner_input_addDesignerJp = dpg.add_input_text(label="Jp Designer")

                    dpg.add_spacer(height=5)
                    with dpg.group(horizontal=True):
                        self.ui_dataDesigner_button_addDesignerToDb = dpg.add_button(label="Add designer to database",
                                                                                     callback=self.InsertDataToDb,
                                                                                     user_data=data.designer, width=200, height=25)

                        self.ui_dataDesigner_button_showDesignerTable = dpg.add_button(
                            label="Show score designer table",
                            callback=self.DisplayTable, user_data=data.designer, width=200, height=25)

            self.ui_data_checkbox_replaceDbEntry = dpg.add_checkbox(label="Overwrite existing database entry")

        with dpg.window(label="Generate maimai Files") as self.ui_window_generateMaimaiFiles:
            dpg.add_text("Generate data files for maimai FiNALE")
            self.ui_generate_button_createFiles = dpg.add_button(label="Generate Files",
                                                                 callback=self.GenerateAndEncryptFiles)
            self.ui_generate_checkbox_encryptFiles = dpg.add_checkbox(label="Encrypt Files", default_value=True)
            dpg.add_spacer(width=4)
            self.ui_generate_button_openOutputFolder = dpg.add_button(label="Open Output Folder",
                                                                      callback=lambda: os.startfile(
                                                                          f"{os.getcwd()}/output"))

        with dpg.window(label="mmMusic Grid", show=False) as self.ui_window_mmMusicDisplay:
            # self.ui_table_mmMusic_input_filter = dpg.add_input_text(label="Filter",
            #                                                         callback=lambda: self.FilterData(data.mmMusic))
            columns = ["track_id", "name", "ver", "subcate", "bpm", "sort_id", "dress", "darkness", "mile", "vl",
                       "event", "rec", "pvstart", "pvend", "song_duration", "off_ranking", "ad_def", "remaster",
                       "special_pv", "challenge_track", "bonus", "genre_id", "title", "artist", "sort_jp_index",
                       "sort_ex_index", "filename"]
            with dpg.table(header_row=True, resizable=True, sortable=True, hideable=True) as self.ui_table_mmMusic:
                for column in columns:
                    dpg.add_table_column(label=column)

        with dpg.window(label="mmScore Grid", show=False) as self.ui_window_mmScoreDisplay:
            columns = ["track_id", "name", "lv", "designer_id", "utage_mode", "safename"]
            with dpg.table(header_row=True, resizable=True, sortable=True, hideable=True) as self.ui_table_mmScore:
                for column in columns:
                    dpg.add_table_column(label=column)

        with dpg.window(label="Artist Name Grid", show=False) as self.ui_window_textoutArtistDisplay:
            columns = ["artist_id", "ex_artist_title", "jp_artist_title"]
            with dpg.table(header_row=True, resizable=True, sortable=True,
                           hideable=True) as self.ui_table_textoutArtist:
                for column in columns:
                    dpg.add_table_column(label=column)

        with dpg.window(label="Track Name Grid", show=False) as self.ui_window_textoutTrackDisplay:
            columns = ["track_id", "ex_track_title", "jp_track_title"]
            with dpg.table(header_row=True, resizable=True, sortable=True, hideable=True) as self.ui_table_textoutTrack:
                for column in columns:
                    dpg.add_table_column(label=column)

        with dpg.window(label="Track Designer Grid", show=False) as self.ui_window_textoutDesignerDisplay:
            columns = ["designer_id", "ex_designer_name", "jp_designer_name"]
            with dpg.table(header_row=True, resizable=True, sortable=True,
                           hideable=True) as self.ui_table_textoutDesigner:
                for column in columns:
                    dpg.add_table_column(label=column)

        with dpg.window(label="Sound BGM Grid", show=False) as self.ui_window_soundBgmDisplay:
            columns = ["track_id", "title"]
            with dpg.table(header_row=True, resizable=True, sortable=True, hideable=True) as self.ui_table_soundBgm:
                for column in columns:
                    dpg.add_table_column(label=column)

        with dpg.window(label="Log") as self.ui_window_log:
            with dpg.group(horizontal=True):
                self.ui_log_input_log = dpg.add_input_text(label="", multiline=True, readonly=True, width=600,
                                                           height=1200)
                self.ui_log_button_clearLog = dpg.add_button(label="Clear",
                                                             callback=lambda: dpg.set_value(self.ui_log_input_log, ""))

        dpg.configure_app(docking=True, docking_space=True, load_init_file="dpg.ini", init_file="dpg.ini",
                          auto_save_init_file=True)

        with dpg.font_registry():
            with dpg.font("NotoSerifCJKjp-Medium.otf", 20) as font1:
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
                dpg.add_font_range_hint(dpg.mvFontRangeHint_Japanese)
                dpg.bind_font(font1)

        dpg.set_frame_callback(1, callback=self.OnStart)

        dpg.set_exit_callback(self.OnExit)

        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def InsertDataToDb(self, sender, app_data, user_data):
        data = user_data

        tempConn = dba.CreateConnection(self.db)
        insert = hlp.CommonData

        if data == insert.artist:
            artistId = hlp.AffixZeroesToString(dpg.get_value(self.ui_dataArtist_input_addArtistId), 4)
            artistEx = dpg.get_value(self.ui_dataArtist_input_addArtistEx)
            artistJp = dpg.get_value(self.ui_dataArtist_input_addArtistJp)

            if not artistId:
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

            if not trackId:
                return

            if not (dba.InsertLineToTextOutTrack(tempConn, [trackId, trackEx, trackJp])):
                if dpg.get_value(self.ui_data_checkbox_replaceDbEntry):
                    dba.ReplaceLineInTextOutTrack(tempConn, [trackId, trackEx, trackJp])
                    self.AppendLog("Entry replaced")
                else:
                    self.AppendLog("Entry already exists")
            else:
                self.AppendLog("Entry added")

        elif data == insert.designer:
            designerId = hlp.AffixZeroesToString(dpg.get_value(self.ui_dataDesigner_input_addDesignerId), 4)
            designerEx = dpg.get_value(self.ui_dataDesigner_input_addDesignerEx)
            designerJp = dpg.get_value(self.ui_dataDesigner_input_addDesignerJp)

            if not designerId:
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

            if not trackId:
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

            if not trackId:
                return

            # Get all rows where score id is not 0
            for i in range(0, 6, 1):
                if dpg.get_value(self.ui_dataMmScore_input_addScoreId[i]) != 0:
                    scoreId = hlp.AffixZeroesToString(dpg.get_value(self.ui_dataMmScore_input_addScoreId[i]), 2)
                    lv = f'{round(dpg.get_value(self.ui_dataMmScore_input_addDifficulty[i]), 1):g}'  # :g Removes trailing zeroes
                    designerId = dpg.get_value(self.ui_dataMmScore_input_addDesignerId[i])
                    utageMode = hlp.BoolToValueReversed(dpg.get_value(self.ui_dataMmScore_checkbox_addIsInUtage[i]))
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

    def GetDataFromDb(self, sender, app_data, user_data):
        data = user_data

        tempConn = dba.CreateConnection(self.db)
        get = hlp.CommonData

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
                dgHelp.UpdateDataMmMusicFields(self, row)
            else:
                dgHelp.DefaultDataMmMusicFields(self)

        # Grabs all scores for the track id
        elif data == get.mmScore:
            trackId = dpg.get_value(self.ui_dataMmScore_input_addTrackId)
            rows = dba.SelectMmScoreById(tempConn, hlp.AffixZeroesToString(trackId, 3))

            # Reset fields first
            dgHelp.DefaultDataMmScoreFields(self)
            dgHelp.UpdateDataMmScoreFields(self, rows)

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
        types = hlp.CommonData

        def GetVal(id: int):
            return dpg.get_value(id)

        def ValidateFile(file: str) -> bool:
            if not file:
                self.AppendLog("Please add files to import from into the Select maimai files window")
                return False

            if not os.path.isfile(file):
                self.AppendLog(f"{file} does not exist")
                return False
            return True

        def ProcessMmMusic() -> bool:
            mmMusicLine = readDat.ReadMmMusicSingleLine(mmMusicPath, importTrackId)

            if not mmMusicLine:
                self.AppendLog("Could not read mmMusic file")
                return False

            conversion = cvrt.ConvertSplitMmMusicLineFromMurasakiToFinale(mmMusicLine)
            dgHelp.UpdateDataMmMusicFields(self, conversion)

            return True

        def ProcessMmScore() -> bool:
            mmScoreLine = readDat.ReadMmScoreLinesWithTrackId(mmScorePath, importTrackId)

            if not mmScoreLine:
                self.AppendLog("Could not read mmScore file")
                return False

            if len(mmScoreLine) == 0:
                self.AppendLog("No scores found for this track id")
                return False

            dgHelp.DefaultDataMmScoreFields(self)
            dgHelp.UpdateDataMmScoreFields(self, mmScoreLine)

            return True

        def ProcessSoundBgm() -> bool:
            soundBgmLine = readDat.ReadSoundBgmLineWithId(soundBgmPath, importTrackId)

            if not soundBgmLine:
                self.AppendLog("No track found in soundBGM file")
                return False

            if not dgHelp.UpdateSoundBgmFields(self, soundBgmLine):
                self.AppendLog("Could not read soundBGM file")
                return False

            return True


        mmMusicPath = GetVal(self.ui_filesMurasaki_input_mmMusic)
        mmScorePath = GetVal(self.ui_filesMurasaki_input_mmScore)
        mmTextoutExPath = GetVal(self.ui_filesMurasaki_input_mmTextoutEx)
        mmTextoutJpPath = GetVal(self.ui_filesMurasaki_input_mmTextoutJp)
        soundBgmPath = GetVal(self.ui_filesMurasaki_input_soundBgm)

        files = [mmMusicPath, mmScorePath, mmTextoutExPath, mmTextoutJpPath, soundBgmPath]

        for file in files:
            if not ValidateFile(file):
                return

        dgHelp.DefaultDataMmMusicFields(self)

        importTrackId = GetVal(self.ui_import_input_importTrackId)

        if importTrackId == 0:
            self.AppendLog("Please select a track id to import")
            return

        dpg.set_value(self.ui_dataMmMusic_input_addTrackId, importTrackId)
        dpg.set_value(self.ui_dataMmScore_input_addTrackId, importTrackId)

        if not ProcessMmMusic():
            return

        if not ProcessMmScore():
            return

        # Track name
        trackExName = readDat.ReadMmTextoutLineWithId(mmTextoutExPath, importTrackId, types.track)

        trackJpName = readDat.ReadMmTextoutLineWithId(mmTextoutJpPath, importTrackId, types.track)

        if not trackExName or trackJpName:
            self.AppendLog("Could not find track name")

        dgHelp.UpdateDataTrackNameFields(self, [importTrackId, trackExName, trackJpName])

        # Artist
        artistExName = readDat.ReadMmTextoutLineWithId(mmTextoutExPath, importTrackId, types.artist)

        artistJpName = readDat.ReadMmTextoutLineWithId(mmTextoutJpPath, importTrackId, types.artist)

        if not artistExName or artistJpName:
            self.AppendLog("Could not find artist name")

        dgHelp.UpdateDataArtistFields(self, [importTrackId, artistExName, artistJpName])

        # Designer
        designerExName = readDat.ReadMmTextoutLineWithId(mmTextoutExPath, importTrackId, types.designer)

        designerJpName = readDat.ReadMmTextoutLineWithId(mmTextoutJpPath, importTrackId, types.designer)

        if not designerExName or designerJpName:
            self.AppendLog("Could not find designer name")

        dgHelp.UpdateDataDesignerFields(self, [importTrackId, designerExName, designerJpName])

        if not ProcessSoundBgm():
            return

        self.AppendLog("Data imported successfully")

    # TODO This will be removed as sorting is builtin in the newer DPG versions
    # def FilterData(self, table):
    #     tempConn = CreateConnection(self.db)
    #     filters = hlp.CommonData
    #
    #     if table == filters.mmMusic:
    #         keyword = dpg.get_value(self.ui_table_mmMusic_input_filter)
    #         rows = dba.SelectMmMusicByLikeFilename(tempConn, keyword)
    #         if len(rows) > 0:
    #             dpg.clear_table("table_mmMusic")
    #             for row in rows:
    #                 dpg.add_row("table_mmMusic", row)
    #
    #     tempConn.close()

    def AppendLog(self, text):
        dpg.set_value(self.ui_log_input_log,
                      f"{dpg.get_value(self.ui_log_input_log)}{datetime.datetime.now().strftime('%H:%M:%S')} - {text}\n")

    def MainCallback(self):
        pass
        # dpg.set_item_width(self.ui_log_input_log, dpg.get_drawing_size("window_log")[0] - 100)
        # dpg.set_item_height(self.ui_log_input_log, dpg.get_drawing_size("window_log")[1] - 35)

    def OnStart(self):
        self.LoadConfig()

        # This doesn't set the main window size properly, when called from OnStart()
        # self.LoadConfig(self.GetCurrentWindowNames())

    def OnExit(self):
        self.SaveConfig()

    def SaveConfig(self):
        with open(os.getcwd() + "\\config.ini", "r+") as f:
            self.config["Database"]["Name"] = self.db

            supportedVersions = ["Finale", "Murasaki"]

            for version in supportedVersions:
                for name, file in dgHelp.GetMaimaiFilesFromInput(self, version).items():
                    if file:
                        self.config[f"Files{version}"][name] = file

            self.config.write(f)

    def LoadConfig(self):
        supportedVersions = ["Finale", "Murasaki"]
        maimaiFiles = ["mmMusic", "mmScore", "mmTextoutEx", "mmTextoutJp", "soundBgm"]

        for version in supportedVersions:
            files = {0: "", 1: "", 2: "", 3: "", 4: ""}

            for enum, maimaiFile in enumerate(maimaiFiles):
                if self.config.has_option(f"Files{version}", maimaiFile):
                    files[enum] = self.config[f"Files{version}"][maimaiFile]

            dgHelp.SetMaimaiFilesFromConfig(self, version, files)


if __name__ == '__main__':
    GUI()
