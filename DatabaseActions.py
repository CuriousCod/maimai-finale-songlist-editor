import sqlite3 as sq
from sqlite3 import Error


def InsertLineToMusic(conn, line):
    Insert = """INSERT INTO mm_music(track_id, name, ver, subcate, bpm, sort_id, dress, darkness, mile, vl, event, 
    rec, pvstart, pvend, song_duration, off_ranking, ad_def, remaster, special_pv, challenge_track, bonus, genre_id, 
    title, artist, sort_jp_index, sort_ex_index, filename) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) """

    cur = conn.cursor()
    try:
        cur.execute(Insert, line)
        conn.commit()
    except sq.IntegrityError:
        pass
    return


def InsertLineToScore(conn, line):
    Insert = """INSERT INTO mm_score(track_id, name, lv, score_id, utage_mode, safename) VALUES(?,?,?,?,?,?) """

    cur = conn.cursor()
    try:
        cur.execute(Insert, line)
        conn.commit()
    except sq.IntegrityError:
        pass
    return


def InsertLineToTextOutExArtist(conn, line):
    Insert = """INSERT INTO mm_textout_artist(artist_id, ex_track_artist) VALUES(?,?) """

    cur = conn.cursor()
    try:
        cur.execute(Insert, line)
        conn.commit()
    except sq.IntegrityError:
        pass
    return


def UpdateLineToTextOutJpArtist(conn, line):
    Insert = """UPDATE mm_textout_artist SET jp_track_artist = ? WHERE artist_id = ?"""

    cur = conn.cursor()
    try:
        cur.execute(Insert, line)
        conn.commit()
    except sq.IntegrityError:
        pass
    return


def InsertLineToTextOutExTrack(conn, line):
    update = """INSERT INTO mm_textout_track(track_id, ex_track_title) VALUES(?,?) """

    cur = conn.cursor()
    try:
        cur.execute(update, line)
        conn.commit()
    except sq.IntegrityError:
        pass
    return


def UpdateLineToTextOutJpTrack(conn, line):
    update = """UPDATE mm_textout_track SET jp_track_title = ? WHERE track_id = ?"""

    cur = conn.cursor()
    try:
        cur.execute(update, line)
        conn.commit()
    except sq.IntegrityError:
        pass
    return


def InsertLineToSoundBgm(conn, line):
    update = """INSERT INTO sound_bgm(title, track_id) VALUES(?,?) """

    cur = conn.cursor()
    try:
        cur.execute(update, line)
        conn.commit()
    except sq.IntegrityError:
        pass
    return


def SelectMmMusic(conn):
    select = """SELECT track_id, name, ver, subcate, bpm, sort_id, dress, darkness, mile, vl, event, 
    rec, pvstart, pvend, song_duration, off_ranking, ad_def, remaster, special_pv, challenge_track, bonus, genre_id, 
    title, artist, sort_jp_index, sort_ex_index, filename FROM mm_music ORDER BY track_id"""

    cur = conn.cursor()
    cur.execute(select)

    rows = cur.fetchall()

    return rows


def SelectMmScore(conn):
    select = """SELECT track_id, name, lv, score_id, utage_mode, safename FROM mm_score ORDER BY track_id"""

    cur = conn.cursor()
    cur.execute(select)

    rows = cur.fetchall()

    return rows


def SelectMmTextoutArtist(conn):
    select = """SELECT artist_id, ex_track_artist, jp_track_artist FROM mm_textout_artist ORDER BY artist_id"""

    cur = conn.cursor()
    cur.execute(select)

    rows = cur.fetchall()

    return rows


def SelectMmTextoutTrack(conn):
    select = """SELECT track_id, ex_track_title, jp_track_title FROM mm_textout_track ORDER BY track_id"""

    cur = conn.cursor()
    cur.execute(select)

    rows = cur.fetchall()

    return rows


def SelectSoundBgm(conn):
    select = """SELECT title, track_id FROM sound_bgm ORDER BY title"""

    cur = conn.cursor()
    cur.execute(select)

    rows = cur.fetchall()

    return rows
