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
        core.set_value("dataMmMusic_input_addGenre", hlp.GenreValueToFinaleText(row[21]))
        core.set_value("dataMmMusic_input_addTitleId", int(row[22]))
        core.set_value("dataMmMusic_input_addArtistId", int(row[23]))
        core.set_value("dataMmMusic_input_addSortJpIndex", int(row[24]))
        core.set_value("dataMmMusic_input_addSortExIndex", int(row[25]))
        core.set_value("dataMmMusic_input_addFilename", row[26])

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