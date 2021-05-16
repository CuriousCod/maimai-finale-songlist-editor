from dearpygui import core, simple
import Helpers as hlp


# def ImportedMmMusicLineToGuiFormat(line):
#     guiLine = []
#
#     guiLine.append(line[0])
#     guiLine.append(line[2])
#     guiLine.append(line[4])
#     guiLine.append(line[5])
#     guiLine.append(line[9])
#     guiLine.append(line[12])
#     guiLine.append(line[13])
#     guiLine.append(line[17])
#     guiLine.append(line[21])
#     guiLine.append(line[22])  # Title
#     guiLine.append(line[23])  # Artist
#     guiLine.append(line[24])
#     guiLine.append(line[25])
#     guiLine.append(line[26])
#
#     return guiLine


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