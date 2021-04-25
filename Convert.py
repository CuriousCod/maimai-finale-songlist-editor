import Helpers as hlp

# Functions to convert maimai green data to finale


def SubConvertGenreFromGreenToFinale(genre):
    if genre == "2" or genre == "6":  # anime & pop
        return "4"
    elif genre == "11":  # vocaloid
        return "5"
    elif genre == "9" or genre == "7":  # game & variety
        return "8"
    elif genre == "5" or genre == "9":  # sega & joypolis
        return "7"
    elif genre == "3" or genre == "4":  # original
        return "9"
    elif genre == "10":  # touhou
        return "6"
    else:
        return "0"


def SubConvertScoreDifficultyFromGreenToFinale(score):
    if "easy" in score:
        return score.replace("easy", "01")
    elif "basic" in score:
        return score.replace("basic", "02")
    elif "adv" in score:
        return score.replace("adv", "03")
    elif "expert" in score:
        return score.replace("expert", "04")
    elif "master" in score:
        return score.replace("master", "05")
    else:
        return score


def ConvertMmMusicLineFromGreentoFinale(track_id):
    with open(r"I:\DL\Games\maimai GreeN PLUS\maimai\data\tables\mmMusic.tbl", "r", encoding="UTF16") as f:
        for line in f.readlines():
            if line.startswith(f"MMMUSIC( {track_id},"):
                split = list(hlp.SplitMusicOrScoreLine(line))

                # maimai green doesn't have a vl value, so it's set 0. Presumably all green tracks have a video file
                convertedLine = [split[0], split[1], split[2] + "0", "30", split[3], split[4], "0", "0", "0", "0", "0",
                                 "1", split[10], split[11], "0", "0", "0", "99999999", "0", "0", "0",
                                 SubConvertGenreFromGreenToFinale(split[14]), split[15].replace("RST_MUSICTITLE_", ""), split[16].replace("RST_MUSICARTIST_", ""), "000000", "000000",
                                 split[17]]

                return convertedLine


def ConvertMmScoreLineFromGreentoFinale(track_id):
    with open(r"I:\DL\Games\maimai GreeN PLUS\maimai\data\tables\mmScore.tbl", "r", encoding="UTF16") as f:
        for line in f.readlines():
            if line.startswith(f"MMSCORE( {track_id},"):
                split = list(hlp.SplitMusicOrScoreLine(line))
                convertedLine = [split[0], SubConvertScoreDifficultyFromGreenToFinale(split[1]), split[3], "0", "1",
                                 SubConvertScoreDifficultyFromGreenToFinale(split[9])]

                return convertedLine


def ConvertSoundBgmLineFromGreentoFinale(track_id):
    track_id = hlp.AffixZeroesToString(track_id, 3)

    with open(r"I:\DL\Games\maimai GreeN PLUS\maimai\data\SoundBGM.txt", "r", encoding="UTF8") as f:
        for line in f.readlines():
            if f"data/sound/{track_id}" in line:
                splitLines = line.split(", ")

                return [splitLines[0], track_id]


def ConvertMmTextOutArtistFromGreenToFinale(artist_id):
    artist_id = hlp.AffixZeroesToString(artist_id, 4)

    with open(r"I:\DL\Games\maimai GreeN PLUS\maimai\data\tables\mmtextout.tbl", "r", encoding="UTF16") as f:
        for line in f.readlines():
            if f"RST_MUSICARTIST_" in line:
                if artist_id in line:
                    splitLines = line.split(",")
                    splitLines[1] = splitLines[1].replace("L\"", "").replace("\"", "")
                    splitLines[2] = splitLines[2].replace("L\"", "").replace("\"", "")

                    return [artist_id, splitLines[2], splitLines[1]]


def ConvertMmTextOutTrackFromGreenToFinale(track_id):
    track_id = hlp.AffixZeroesToString(track_id, 4)

    with open(r"I:\DL\Games\maimai GreeN PLUS\maimai\data\tables\mmtextout.tbl", "r", encoding="UTF16") as f:
        for line in f.readlines():
            if f"RST_MUSICTITLE_" in line:
                if track_id in line:
                    splitLines = line.split(",")
                    splitLines[1] = splitLines[1].replace("L\"", "").replace("\"", "")
                    splitLines[2] = splitLines[2].replace("L\"", "").replace("\"", "")

                    return [track_id, splitLines[2], splitLines[1]]