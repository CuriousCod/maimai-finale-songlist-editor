from dearpygui import core, simple
import Helpers as hlp


def UpdateDataMmMusicFields(row):
    if len(row) == 27:
        core.set_value("dataMmMusic_input_addVersion", int(row[2]))
        core.set_value("dataMmMusic_input_addBpm", float(row[4]))
        core.set_value("dataMmMusic_input_addSortId", int(row[5]))
        core.set_value("dataMmMusic_checkbox_addHasVideo", bool(hlp.ValueToBoolReversed(row[9])))
        core.set_value("dataMmMusic_input_addPvStart", float(row[12]))
        core.set_value("dataMmMusic_input_addPvEnd", float(row[13]))
        core.set_value("dataMmMusic_input_addRemaster", int(row[17]))
        core.set_value("dataMmMusic_combo_addGenreId", hlp.GenreValueToFinaleText(row[21]))
        core.set_value("dataMmMusic_input_addTitleId", int(row[22]))
        core.set_value("dataMmMusic_input_addArtistId", int(row[23]))
        core.set_value("dataMmMusic_input_addSortJpIndex", int(row[24]))
        core.set_value("dataMmMusic_input_addSortExIndex", int(row[25]))
        core.set_value("dataMmMusic_input_addFilename", row[26])

        core.set_value("dataMmMusic_hidden_subcate", row[3])
        core.set_value("dataMmMusic_hidden_dress", row[6])
        core.set_value("dataMmMusic_hidden_darkness", row[7])
        core.set_value("dataMmMusic_hidden_mile", row[8])

        core.set_value("dataMmMusic_hidden_event", row[10])
        core.set_value("dataMmMusic_hidden_rec", row[11])
        core.set_value("dataMmMusic_hidden_songDuration", row[14])
        core.set_value("dataMmMusic_hidden_offRanking", row[15])

        core.set_value("dataMmMusic_hidden_adDef", row[16])
        core.set_value("dataMmMusic_hidden_specialPv", row[18])
        core.set_value("dataMmMusic_hidden_challengeTrack", row[19])
        core.set_value("dataMmMusic_hidden_bonus", row[20])

        return True
    else:
        DefaultDataMmMusicFields()


def DefaultDataMmMusicFields():
    core.set_value("dataMmMusic_input_addVersion", 10000)
    core.set_value("dataMmMusic_input_addBpm", 0.00)
    core.set_value("dataMmMusic_input_addSortId", 300000)
    core.set_value("dataMmMusic_checkbox_addHasVideo", False)
    core.set_value("dataMmMusic_input_addPvStart", 0.00)
    core.set_value("dataMmMusic_input_addPvEnd", 0.00)
    core.set_value("dataMmMusic_input_addRemaster", 99999999)
    core.set_value("dataMmMusic_input_addGenre", "Pops & Anime")
    core.set_value("dataMmMusic_input_addTitleId", 0)
    core.set_value("dataMmMusic_input_addArtistId", 0)
    core.set_value("dataMmMusic_input_addSortJpIndex", 0)
    core.set_value("dataMmMusic_input_addSortExIndex", 0)
    core.set_value("dataMmMusic_input_addFilename", "")

    core.set_value("dataMmMusic_hidden_subcate", "30")
    core.set_value("dataMmMusic_hidden_dress", "0")
    core.set_value("dataMmMusic_hidden_darkness", "0")
    core.set_value("dataMmMusic_hidden_mile", "0")

    core.set_value("dataMmMusic_hidden_event", "0")
    core.set_value("dataMmMusic_hidden_rec", "1")
    core.set_value("dataMmMusic_hidden_songDuration", "0")
    core.set_value("dataMmMusic_hidden_offRanking", "0")

    core.set_value("dataMmMusic_hidden_adDef", "0")
    core.set_value("dataMmMusic_hidden_specialPv", "0")
    core.set_value("dataMmMusic_hidden_challengeTrack", "0")
    core.set_value("dataMmMusic_hidden_bonus", "0")


def UpdateDataMmScoreFields(rows):
    for enum, row in enumerate(rows):
        core.set_value(f"dataMmScore_input_addScoreId_0{enum + 1}", int(str(row[0])[-2:]))
        core.set_value(f"dataMmScore_input_addDifficulty_0{enum + 1}", float(row[2]))
        core.set_value(f"dataMmScore_input_addDesignerId_0{enum + 1}", int(row[3]))
        core.set_value(f"dataMmScore_checkbox_addIsInUtage_0{enum + 1}", hlp.ValueToBoolReversed(row[4]))

        if enum == 0:
            core.set_value(f"dataMmScore_input_addBaseSafename", row[5][4:-3])

def DefaultDataMmScoreFields():
    for i in range(1, 7, 1):
        core.set_value(f"dataMmScore_input_addScoreId_0{i}", 0)
        core.set_value(f"dataMmScore_input_addDifficulty_0{i}", 0.0)
        core.set_value(f"dataMmScore_input_addDesignerId_0{i}", 0)
        core.set_value(f"dataMmScore_checkbox_addIsInUtage_0{i}", False)
    core.set_value("dataMmScore_input_addBaseSafename", "")
