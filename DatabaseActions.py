import sqlite3 as sq
from sqlite3 import Error


def ExecuteSql(conn, sql, line):
    cur = conn.cursor()
    try:
        cur.execute(sql, line)
        conn.commit()
    except sq.IntegrityError:
        return False
    return True


def InsertLineToMusic(conn, line):
    sql = """INSERT INTO mm_music(track_id, name, ver, subcate, bpm, sort_id, dress, darkness, mile, vl, event, 
    rec, pvstart, pvend, song_duration, off_ranking, ad_def, remaster, special_pv, challenge_track, bonus, genre_id, 
    title, artist, sort_jp_index, sort_ex_index, filename) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """

    return ExecuteSql(conn, sql, line)


def ReplaceLineInMusic(conn, line):
    sql = """REPLACE INTO mm_music(track_id, name, ver, subcate, bpm, sort_id, dress, darkness, mile, vl, event, 
    rec, pvstart, pvend, song_duration, off_ranking, ad_def, remaster, special_pv, challenge_track, bonus, genre_id, 
    title, artist, sort_jp_index, sort_ex_index, filename) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """

    return ExecuteSql(conn, sql, line)


def InsertLineToScore(conn, line):
    sql = """INSERT INTO mm_score(track_id, name, lv, designer_id, utage_mode, safename) VALUES(?,?,?,?,?,?) """

    return ExecuteSql(conn, sql, line)


def ReplaceLineInScore(conn, line):
    sql = """Replace INTO mm_score(track_id, name, lv, designer_id, utage_mode, safename) VALUES(?,?,?,?,?,?) """

    return ExecuteSql(conn, sql, line)

# Artist ---------------------------------------------------------------------------------------------------------------


def InsertLineToTextOutArtist(conn, line):
    sql = """INSERT INTO mm_textout_artist(artist_id, ex_track_artist, jp_track_artist) VALUES(?,?,?) """

    return ExecuteSql(conn, sql, line)


def ReplaceLineInTextOutArtist(conn, line):
    sql = """REPLACE INTO mm_textout_artist(artist_id, ex_track_artist, jp_track_artist) VALUES(?,?,?) """

    return ExecuteSql(conn, sql, line)


def InsertLineToTextOutExArtist(conn, line):
    sql = """INSERT INTO mm_textout_artist(artist_id, ex_track_artist) VALUES(?,?) """

    return ExecuteSql(conn, sql, line)


def UpdateLineToTextOutJpArtist(conn, line):
    sql = """UPDATE mm_textout_artist SET jp_track_artist = ? WHERE artist_id = ?"""

    return ExecuteSql(conn, sql, line)

# Track ----------------------------------------------------------------------------------------------------------------


def InsertLineToTextOutTrack(conn, line):
    sql = """INSERT INTO mm_textout_track(track_id, ex_track_title, jp_track_title) VALUES(?,?,?) """

    return ExecuteSql(conn, sql, line)


def ReplaceLineInTextOutTrack(conn, line):
    sql = """REPLACE INTO mm_textout_track(track_id, ex_track_title, jp_track_title) VALUES(?,?,?) """

    return ExecuteSql(conn, sql, line)


def InsertLineToTextOutExTrack(conn, line):
    sql = """INSERT INTO mm_textout_track(track_id, ex_track_title) VALUES(?,?) """

    return ExecuteSql(conn, sql, line)


def UpdateLineToTextOutJpTrack(conn, line):
    sql = """UPDATE mm_textout_track SET jp_track_title = ? WHERE track_id = ?"""

    return ExecuteSql(conn, sql, line)

# Designer -------------------------------------------------------------------------------------------------------------


def InsertLineToTextOutDesigner(conn, line):
    sql = """INSERT INTO mm_textout_designer(designer_id, ex_designer_title, jp_designer_title) VALUES(?,?,?) """

    return ExecuteSql(conn, sql, line)


def ReplaceLineInTextOutDesigner(conn, line):
    sql = """REPLACE INTO mm_textout_designer(designer_id, ex_designer_title, jp_designer_title) VALUES(?,?,?) """

    return ExecuteSql(conn, sql, line)


def InsertLineToTextOutExDesigner(conn, line):
    sql = """INSERT INTO mm_textout_designer(designer_id, ex_designer_name) VALUES(?,?) """

    return ExecuteSql(conn, sql, line)


def UpdateLineToTextOutJpDesigner(conn, line):
    sql = """UPDATE mm_textout_designer SET jp_designer_name = ? WHERE designer_id = ? """

    return ExecuteSql(conn, sql, line)


# SoundBGM -------------------------------------------------------------------------------------------------------------


def InsertLineToSoundBgm(conn, line):
    sql = """INSERT INTO sound_bgm(title, track_id) VALUES(?,?) """

    return ExecuteSql(conn, sql, line)


def ReplaceLineInSoundBgm(conn, line):
    sql = """REPPLACE INTO sound_bgm(title, track_id) VALUES(?,?) """

    return ExecuteSql(conn, sql, line)


def SelectMmMusic(conn):
    select = """SELECT track_id, name, ver, subcate, bpm, sort_id, dress, darkness, mile, vl, event, 
    rec, pvstart, pvend, song_duration, off_ranking, ad_def, remaster, special_pv, challenge_track, bonus, genre_id, 
    title, artist, sort_jp_index, sort_ex_index, filename FROM mm_music ORDER BY track_id"""

    cur = conn.cursor()
    cur.execute(select)

    rows = cur.fetchall()

    return rows


def SelectMmMusicById(conn, track_id):
    select = """SELECT track_id, name, ver, subcate, bpm, sort_id, dress, darkness, mile, vl, event, 
    rec, pvstart, pvend, song_duration, off_ranking, ad_def, remaster, special_pv, challenge_track, bonus, genre_id, 
    title, artist, sort_jp_index, sort_ex_index, filename FROM mm_music WHERE track_id = ? ORDER BY track_id"""

    cur = conn.cursor()
    cur.execute(select, (track_id,))

    rows = cur.fetchall()

    return rows


def SelectMmScore(conn):
    select = """SELECT track_id, name, lv, designer_id, utage_mode, safename FROM mm_score ORDER BY track_id"""

    cur = conn.cursor()
    cur.execute(select)

    rows = cur.fetchall()

    return rows

# Grab id from safename as track_id contains track id + score id combined
def SelectMmScoreById(conn, track_id):
    select = """SELECT track_id, name, lv, designer_id, utage_mode, safename FROM mm_score WHERE safename LIKE ? ORDER BY track_id"""

    cur = conn.cursor()
    cur.execute(select, (f"{track_id}%",))

    rows = cur.fetchall()

    return rows


def SelectMmTextoutArtist(conn):
    select = """SELECT artist_id, ex_track_artist, jp_track_artist FROM mm_textout_artist ORDER BY artist_id"""

    cur = conn.cursor()
    cur.execute(select)

    rows = cur.fetchall()

    return rows


def SelectMmTextoutArtistById(conn, artist_id):
    select = """SELECT ex_track_artist, jp_track_artist FROM mm_textout_artist WHERE artist_id = ? ORDER BY artist_id"""

    cur = conn.cursor()
    cur.execute(select, (artist_id,))

    rows = cur.fetchall()

    return rows


def SelectMmTextoutTrack(conn):
    select = """SELECT track_id, ex_track_title, jp_track_title FROM mm_textout_track ORDER BY track_id"""

    cur = conn.cursor()
    cur.execute(select)

    rows = cur.fetchall()

    return rows


def SelectMmTextoutTrackById(conn, track_id):
    select = """SELECT ex_track_title, jp_track_title FROM mm_textout_track WHERE track_id = ? ORDER BY track_id"""

    cur = conn.cursor()
    cur.execute(select, (track_id,))

    rows = cur.fetchall()

    return rows


def SelectMmTextoutDesigner(conn):
    select = """SELECT designer_id, ex_designer_name, jp_designer_name FROM mm_textout_designer ORDER BY designer_id"""

    cur = conn.cursor()
    cur.execute(select)

    rows = cur.fetchall()

    return rows

def SelectMmTextoutDesignerById(conn, designer_id):
    select = """SELECT ex_designer_name, jp_designer_name FROM mm_textout_designer WHERE designer_id = ? ORDER BY designer_id"""

    cur = conn.cursor()
    cur.execute(select, (designer_id,))

    rows = cur.fetchall()

    return rows

def SelectSoundBgmOrderTitle(conn):
    select = """SELECT title, track_id FROM sound_bgm ORDER BY title"""

    cur = conn.cursor()
    cur.execute(select)

    rows = cur.fetchall()

    return rows


def SelectSoundBgmOrderId(conn):
    select = """SELECT title, track_id FROM sound_bgm ORDER BY track_id"""

    cur = conn.cursor()
    cur.execute(select)

    rows = cur.fetchall()

    return rows


def SelectSoundBgmById(conn, track_id):
    select = """SELECT title, track_id FROM sound_bgm WHERE track_id = ? ORDER BY title"""

    cur = conn.cursor()
    cur.execute(select, (track_id,))

    rows = cur.fetchall()

    return rows


def SelectTitleIdAndArtistIdFromMmMusic(conn, trackId):
    select = """SELECT title, artist FROM mm_music WHERE track_id = ? """

    cur = conn.cursor()
    cur.execute(select, (trackId,))

    rows = cur.fetchall()

    return rows


# Filters -------------------------------------------------------------------------------------------------------------
def SelectMmMusicByLikeFilename(conn, keyword):
    select ="""SELECT track_id, name, ver, subcate, bpm, sort_id, dress, darkness, mile, vl, event, 
       rec, pvstart, pvend, song_duration, off_ranking, ad_def, remaster, special_pv, challenge_track, bonus, genre_id, 
       title, artist, sort_jp_index, sort_ex_index, filename FROM mm_music WHERE filename LIKE ?"""

    cur = conn.cursor()
    cur.execute(select, (f"%{keyword}%",))

    rows = cur.fetchall()

    return rows