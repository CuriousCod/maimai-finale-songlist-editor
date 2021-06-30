import dearpygui.dearpygui as dpg
import Helpers as hlp


def UpdateDataMmMusicFields(row):
    if len(row) == 27:
        dpg.set_value("dataMmMusic_input_addVersion", int(row[2]))
        dpg.set_value("dataMmMusic_input_addBpm", float(row[4]))
        dpg.set_value("dataMmMusic_input_addSortId", int(row[5]))
        dpg.set_value("dataMmMusic_checkbox_addHasVideo", bool(hlp.ValueToBoolReversed(row[9])))
        dpg.set_value("dataMmMusic_input_addPvStart", float(row[12]))
        dpg.set_value("dataMmMusic_input_addPvEnd", float(row[13]))
        dpg.set_value("dataMmMusic_input_addRemaster", int(row[17]))
        dpg.set_value("dataMmMusic_combo_addGenreId", hlp.GenreValueToFinaleText(row[21]))
        dpg.set_value("dataMmMusic_input_addTitleId", int(row[22]))
        dpg.set_value("dataMmMusic_input_addArtistId", int(row[23]))
        dpg.set_value("dataMmMusic_input_addSortJpIndex", int(row[24]))
        dpg.set_value("dataMmMusic_input_addSortExIndex", int(row[25]))
        dpg.set_value("dataMmMusic_input_addFilename", row[26])

        dpg.set_value("dataMmMusic_hidden_subcate", row[3])
        dpg.set_value("dataMmMusic_hidden_dress", row[6])
        dpg.set_value("dataMmMusic_hidden_darkness", row[7])
        dpg.set_value("dataMmMusic_hidden_mile", row[8])

        dpg.set_value("dataMmMusic_hidden_event", row[10])
        dpg.set_value("dataMmMusic_hidden_rec", row[11])
        dpg.set_value("dataMmMusic_hidden_songDuration", row[14])
        dpg.set_value("dataMmMusic_hidden_offRanking", row[15])

        dpg.set_value("dataMmMusic_hidden_adDef", row[16])
        dpg.set_value("dataMmMusic_hidden_specialPv", row[18])
        dpg.set_value("dataMmMusic_hidden_challengeTrack", row[19])
        dpg.set_value("dataMmMusic_hidden_bonus", row[20])

        return True
    else:
        DefaultDataMmMusicFields()


def DefaultDataMmMusicFields():
    dpg.set_value("dataMmMusic_input_addVersion", 10000)
    dpg.set_value("dataMmMusic_input_addBpm", 0.00)
    dpg.set_value("dataMmMusic_input_addSortId", 300000)
    dpg.set_value("dataMmMusic_checkbox_addHasVideo", False)
    dpg.set_value("dataMmMusic_input_addPvStart", 0.00)
    dpg.set_value("dataMmMusic_input_addPvEnd", 0.00)
    dpg.set_value("dataMmMusic_input_addRemaster", 99999999)
    dpg.set_value("dataMmMusic_input_addGenre", "Pops & Anime")
    dpg.set_value("dataMmMusic_input_addTitleId", 0)
    dpg.set_value("dataMmMusic_input_addArtistId", 0)
    dpg.set_value("dataMmMusic_input_addSortJpIndex", 0)
    dpg.set_value("dataMmMusic_input_addSortExIndex", 0)
    dpg.set_value("dataMmMusic_input_addFilename", "")

    dpg.set_value("dataMmMusic_hidden_subcate", "30")
    dpg.set_value("dataMmMusic_hidden_dress", "0")
    dpg.set_value("dataMmMusic_hidden_darkness", "0")
    dpg.set_value("dataMmMusic_hidden_mile", "0")

    dpg.set_value("dataMmMusic_hidden_event", "0")
    dpg.set_value("dataMmMusic_hidden_rec", "1")
    dpg.set_value("dataMmMusic_hidden_songDuration", "0")
    dpg.set_value("dataMmMusic_hidden_offRanking", "0")

    dpg.set_value("dataMmMusic_hidden_adDef", "0")
    dpg.set_value("dataMmMusic_hidden_specialPv", "0")
    dpg.set_value("dataMmMusic_hidden_challengeTrack", "0")
    dpg.set_value("dataMmMusic_hidden_bonus", "0")


def UpdateDataMmScoreFields(rows):
    for enum, row in enumerate(rows):
        dpg.set_value(f"dataMmScore_input_addScoreId_0{enum + 1}", int(str(row[0])[-2:]))
        dpg.set_value(f"dataMmScore_input_addDifficulty_0{enum + 1}", float(row[2]))
        dpg.set_value(f"dataMmScore_input_addDesignerId_0{enum + 1}", int(row[3]))
        dpg.set_value(f"dataMmScore_checkbox_addIsInUtage_0{enum + 1}", hlp.ValueToBoolReversed(row[4]))

        if enum == 0:
            dpg.set_value(f"dataMmScore_input_addBaseSafename", row[5][4:-3])

def DefaultDataMmScoreFields():
    for i in range(1, 7, 1):
        dpg.set_value(f"dataMmScore_input_addScoreId_0{i}", 0)
        dpg.set_value(f"dataMmScore_input_addDifficulty_0{i}", 0.0)
        dpg.set_value(f"dataMmScore_input_addDesignerId_0{i}", 0)
        dpg.set_value(f"dataMmScore_checkbox_addIsInUtage_0{i}", False)
    dpg.set_value("dataMmScore_input_addBaseSafename", "")


def UpdateDataTrackNameFields(row):
    dpg.set_value("dataTrack_input_addTrackId", row[0])
    dpg.set_value("dataTrack_input_addTrackEx", row[1])
    dpg.set_value("dataTrack_input_addTrackJp", row[2])


def GetMaimaiFilesFromInput(version):
    files = {"mmMusic": dpg.get_value(f"files{version}_input_mmMusic"),
             "mmScore": dpg.get_value(f"files{version}_input_mmScore"),
             "mmTextoutEx": dpg.get_value(f"files{version}_input_mmTextoutEx"),
             "mmTextoutJp": dpg.get_value(f"files{version}_input_mmTextoutJp"),
             "soundBgm": dpg.get_value(f"files{version}_input_soundBgm")}

    return files


def SetMaimaiFilesFromConfig(version, files):
    dpg.set_value(f"files{version}_input_mmMusic", files[0])
    dpg.set_value(f"files{version}_input_mmScore", files[1])
    dpg.set_value(f"files{version}_input_mmTextoutEx", files[2])
    dpg.set_value(f"files{version}_input_mmTextoutJp", files[3])
    dpg.set_value(f"files{version}_input_soundBgm", files[4])

