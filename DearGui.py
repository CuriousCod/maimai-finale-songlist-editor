import dearpygui.dearpygui as dpg
import Helpers as hlp


def UpdateDataMmMusicFields(self, row):
    if len(row) == 27:
        dpg.set_value(self.ui_dataMmMusic_input_addVersion, int(row[2]))
        dpg.set_value(self.ui_dataMmMusic_input_addBpm, float(row[4]))
        dpg.set_value(self.ui_dataMmMusic_input_addSortId, int(row[5]))
        dpg.set_value(self.ui_dataMmMusic_checkbox_addHasVideo, bool(hlp.ValueToBoolReversed(row[9])))
        dpg.set_value(self.ui_dataMmMusic_input_addPvStart, float(row[12]))
        dpg.set_value(self.ui_dataMmMusic_input_addPvEnd, float(row[13]))
        dpg.set_value(self.ui_dataMmMusic_input_addRemaster, int(row[17]))
        dpg.set_value(self.ui_dataMmMusic_combo_addGenreId, hlp.GenreValueToFinaleText(row[21]))
        dpg.set_value(self.ui_dataMmMusic_input_addTitleId, int(row[22]))
        dpg.set_value(self.ui_dataMmMusic_input_addArtistId, int(row[23]))
        dpg.set_value(self.ui_dataMmMusic_input_addSortJpIndex, int(row[24]))
        dpg.set_value(self.ui_dataMmMusic_input_addSortExIndex, int(row[25]))
        dpg.set_value(self.ui_dataMmMusic_input_addFilename, row[26])

        dpg.set_value(self.ui_dataMmMusic_hidden_subcate, row[3])
        dpg.set_value(self.ui_dataMmMusic_hidden_dress, row[6])
        dpg.set_value(self.ui_dataMmMusic_hidden_darkness, row[7])
        dpg.set_value(self.ui_dataMmMusic_hidden_mile, row[8])

        dpg.set_value(self.ui_dataMmMusic_hidden_event, row[10])
        dpg.set_value(self.ui_dataMmMusic_hidden_rec, row[11])
        dpg.set_value(self.ui_dataMmMusic_hidden_songDuration, row[14])
        dpg.set_value(self.ui_dataMmMusic_hidden_offRanking, row[15])

        dpg.set_value(self.ui_dataMmMusic_hidden_adDef, row[16])
        dpg.set_value(self.ui_dataMmMusic_hidden_specialPv, row[18])
        dpg.set_value(self.ui_dataMmMusic_hidden_challengeTrack, row[19])
        dpg.set_value(self.ui_dataMmMusic_hidden_bonus, row[20])

        return True
    else:
        DefaultDataMmMusicFields(self)


def DefaultDataMmMusicFields(self):
    dpg.set_value(self.ui_dataMmMusic_input_addVersion, 10000)
    dpg.set_value(self.ui_dataMmMusic_input_addBpm, 0.00)
    dpg.set_value(self.ui_dataMmMusic_input_addSortId, 300000)
    dpg.set_value(self.ui_dataMmMusic_checkbox_addHasVideo, False)
    dpg.set_value(self.ui_dataMmMusic_input_addPvStart, 0.00)
    dpg.set_value(self.ui_dataMmMusic_input_addPvEnd, 0.00)
    dpg.set_value(self.ui_dataMmMusic_input_addRemaster, 99999999)
    dpg.set_value(self.ui_dataMmMusic_combo_addGenreId, "Pops & Anime")
    dpg.set_value(self.ui_dataMmMusic_input_addTitleId, 0)
    dpg.set_value(self.ui_dataMmMusic_input_addArtistId, 0)
    dpg.set_value(self.ui_dataMmMusic_input_addSortJpIndex, 0)
    dpg.set_value(self.ui_dataMmMusic_input_addSortExIndex, 0)
    dpg.set_value(self.ui_dataMmMusic_input_addFilename, "")

    dpg.set_value(self.ui_dataMmMusic_hidden_subcate, "30")
    dpg.set_value(self.ui_dataMmMusic_hidden_dress, "0")
    dpg.set_value(self.ui_dataMmMusic_hidden_darkness, "0")
    dpg.set_value(self.ui_dataMmMusic_hidden_mile, "0")

    dpg.set_value(self.ui_dataMmMusic_hidden_event, "0")
    dpg.set_value(self.ui_dataMmMusic_hidden_rec, "1")
    dpg.set_value(self.ui_dataMmMusic_hidden_songDuration, "0")
    dpg.set_value(self.ui_dataMmMusic_hidden_offRanking, "0")

    dpg.set_value(self.ui_dataMmMusic_hidden_adDef, "0")
    dpg.set_value(self.ui_dataMmMusic_hidden_specialPv, "0")
    dpg.set_value(self.ui_dataMmMusic_hidden_challengeTrack, "0")
    dpg.set_value(self.ui_dataMmMusic_hidden_bonus, "0")


def UpdateDataMmScoreFields(self, rows):
    for enum, row in enumerate(rows):
        dpg.set_value(self.ui_dataMmScore_input_addScoreId[enum], int(str(row[0])[-2:]))
        dpg.set_value(self.ui_dataMmScore_input_addDifficulty[enum], float(row[2]))
        dpg.set_value(self.ui_dataMmScore_input_addDesignerId[enum], int(row[3]))
        dpg.set_value(self.ui_dataMmScore_checkbox_addIsInUtage[enum], hlp.ValueToBoolReversed(row[4]))

        if enum == 0:
            dpg.set_value(self.ui_dataMmScore_input_addBaseSafename, row[5][4:-3])

def DefaultDataMmScoreFields(self):
    for i in range(0, 6, 1):
        dpg.set_value(self.ui_dataMmScore_input_addScoreId[i], 0)
        dpg.set_value(self.ui_dataMmScore_input_addDifficulty[i], 0.0)
        dpg.set_value(self.ui_dataMmScore_input_addDesignerId[i], 0)
        dpg.set_value(self.ui_dataMmScore_checkbox_addIsInUtage[i], False)
        dpg.set_value(self.ui_dataMmScore_input_addBaseSafename, "")


def UpdateDataTrackNameFields(self, row):
    dpg.set_value(self.ui_dataTrack_input_addTrackId, row[0])
    dpg.set_value(self.ui_dataTrack_input_addTrackEx, row[1])
    dpg.set_value(self.ui_dataTrack_input_addTrackJp, row[2])


def GetMaimaiFilesFromInput(self, version):

    fileVariables = hlp.GetMaimaiVersionFileVariables(self, version)

    if not len(fileVariables) > 0:
        print("Unknown version")
        return

    files = {"mmMusic": dpg.get_value(fileVariables[0]),
             "mmScore": dpg.get_value(fileVariables[1]),
             "mmTextoutEx": dpg.get_value(fileVariables[2]),
             "mmTextoutJp": dpg.get_value(fileVariables[3]),
             "soundBgm": dpg.get_value(fileVariables[4])}

    return files


def SetMaimaiFilesFromConfig(self, version, files):

    fileVariables = hlp.GetMaimaiVersionFileVariables(self, version)

    if not len(fileVariables) > 0:
        print("Unknown version")
        return

    dpg.set_value(fileVariables[0], files[0])
    dpg.set_value(fileVariables[1], files[1])
    dpg.set_value(fileVariables[2], files[2])
    dpg.set_value(fileVariables[3], files[3])
    dpg.set_value(fileVariables[4], files[4])


def FillTable(table, lines):
    for child in dpg.get_item_children(table, slot=1):
        dpg.delete_item(child)

    for line in lines:
        with dpg.table_row(parent=table):
            for row in line:
                dpg.add_text(row)
