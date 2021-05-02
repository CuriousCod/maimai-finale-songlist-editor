import DatabaseActions as dba
import Helpers as hlp


def GenerateMmMusicFromDb(conn):
    rows = dba.SelectMmMusic(conn)
    lines = []

    for row in rows:
        lines.append(GenerateMmMusicRow(row))

    return lines


def GenerateMmMusicRow(row):
    row = list(row)

    # Add affix to title and artist
    row[22] = f"RST_MUSICTITLE_{row[22]}"
    row[23] = f"RST_MUSICARTIST_{row[23]}"

    # Set row spacings
    row[0] = hlp.SetSpacing(row[0], 3)
    row[3] = hlp.SetSpacing(row[3], 2)
    row[4] = hlp.SetSpacing(row[4], 7)
    row[10] = hlp.SetSpacing(row[10], 8)
    row[12] = hlp.SetSpacing(row[12], 6)
    row[13] = hlp.SetSpacing(row[13], 6)
    row[14] = hlp.SetSpacing(row[14], 3)
    row[15] = hlp.SetSpacing(row[15], 2)
    row[16] = hlp.SetSpacing(row[16], 2)
    row[17] = hlp.SetSpacing(row[17], 8)
    row[24] = hlp.SetSpacing(row[24], 6)
    row[25] = hlp.SetSpacing(row[25], 6)

    # Calculate the space between filename and ) symbol
    lastRowSpacing = 25 - len(row[26]) - 2  # "" marks

    space = ""
    for i in range(lastRowSpacing):
        space += " "  # Add the proper amount of spacing

    completeLine = f"MMMUSIC( {row[0]}{row[1]}, {row[2]}, {row[3]}{row[4]}{row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9]}, {row[10]}{row[11]}, " \
                   f"{row[12]}{row[13]}{row[14]}{row[15]}{row[16]}{row[17]}{row[18]}, {row[19]}, {row[20]}, {row[21]}, {row[22]}, {row[23]}, " \
                   f"{row[24]}{row[25]}\"{row[26]}\"{space}) ///< {row[1].replace(' ', '').replace(',', '')}"

    # print(completeLine)

    """
    lines.append(
        f"MMMUSIC( {row[0]}{row[1]}, {row[2]}, {row[3]}{row[4]}{row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9]}, {row[10]}"
        f"{row[11]}, {row[12]}{row[13]}{row[14]}{row[15]}{row[16]}{row[17]}{row[18]}, {row[19]}, {row[20]}, {row[21]}, {row[22]}, "
        f"{row[23]}, {row[24]}{row[25]}\"{row[26]}\"{space}) ///< {row[1].replace(' ', '').replace(',', '')}\n")"""

    """ Without dynamic row adjustment
    print(
        f"MMMUSIC( {row[0]},   {row[1]}, {row[2]}, {row[3]}, {row[4]},     {row[5]}, {row[6]}, {row[7]}, {row[8]}, {row[9]}, {row[10]},        "
        f"{row[11]}, {row[12]},     {row[13]},     {row[14]},   {row[15]},  {row[16]},  {row[17]}, {row[18]}, {row[19]}, {row[20]}, {row[21]}, {row[22]}, "
        f"{row[23]}, {row[24]}, {row[25]}, \"{row[26]}\"{space}) ///< {row[1]}")"""

    return completeLine


def GenerateMmScoreFromDb(conn):
    rows = dba.SelectMmScore(conn)
    lines = []

    for row in rows:
        lines.append(GenerateMmScoreRow(row))

    return lines


def GenerateMmScoreRow(row):
    row = list(row)

    # Set row spacings
    row[0] = hlp.SetSpacing(row[0], 5)
    row[1] = hlp.SetSpacing(row[1], 36)
    row[2] = hlp.SetSpacing(row[2], 4)
    row[3] = hlp.SetSpacing(row[3], 2)

    # Calculate the space between filename and ) symbol
    lastRowSpacing = 32 - len(row[5]) - 2  # "" marks

    space = ""
    for i in range(lastRowSpacing):
        space += " "  # Add the proper amount of spacing

    # print( f"MMSCORE( {row[0]}{row[1]}{row[2]}{row[3]}{row[4]}, \"{row[5]}\"{space}) ///< {row[1].replace(' ',
    # '').replace(',', '')}")

    return f"MMSCORE( {row[0]}{row[1]}{row[2]}{row[3]}{row[4]}, \"{row[5]}\"{space}) ///< {row[1].replace(' ', '').replace(',', '')}"


def GenerateMmTextoutExFromDb(conn):
    artists = []
    tracks = []
    designers = []

    rows = dba.SelectMmTextoutArtist(conn)

    for row in rows:
        artists.append(f"MMTEXTOUT( L\"RST_MUSICARTIST_{row[0]}\" ,L\"{row[1]}\" )")

    rows = dba.SelectMmTextoutTrack(conn)

    for row in rows:
        tracks.append(f"MMTEXTOUT( L\"RST_MUSICTITLE_{row[0]}\" ,L\"{row[1]}\" )")

    rows = dba.SelectMmTextoutDesigner(conn)

    for row in rows:
        designers.append(f"MMTEXTOUT( L\"RST_SCORECREATOR_{row[0]}\" ,L\"{row[1]}\" )")

    return artists + tracks + designers


def GenerateMmTextoutJpFromDb(conn):
    artists = []
    tracks = []
    designers = []

    rows = dba.SelectMmTextoutArtist(conn)

    for row in rows:
        artists.append(f"MMTEXTOUT( L\"RST_MUSICARTIST_{row[0]}\" ,L\"{row[2]}\" )")

    rows = dba.SelectMmTextoutTrack(conn)

    for row in rows:
        tracks.append(f"MMTEXTOUT( L\"RST_MUSICTITLE_{row[0]}\" ,L\"{row[2]}\" )")

    rows = dba.SelectMmTextoutDesigner(conn)

    for row in rows:
        designers.append(f"MMTEXTOUT( L\"RST_SCORECREATOR_{row[0]}\" ,L\"{row[2]}\" )")

    return artists + tracks + designers


def GenerateSoundBgmFromDb(conn):
    rows = dba.SelectSoundBgmOrderTitle(conn)
    lines = []

    for row in rows:
        # print(f"{row[0]},{row[1]}")
        lines.append(f"{row[0]},{row[1]}")

    return lines
