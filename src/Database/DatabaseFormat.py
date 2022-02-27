MmMusicSq = """ CREATE TABLE IF NOT EXISTS mm_music (
                    id integer PRIMARY KEY,
                    track_id integer UNIQUE,
                    name text NOT NULL,
                    ver text NOT NULL,
                    subcate text NOT NULL,
                    bpm text NOT NULL,
                    sort_id text NOT NULL,
                    dress text NOT NULL,
                    darkness text NOT NULL,
                    mile text NOT NULL,
                    vl text NOT NULL,
                    event text NOT NULL,
                    rec text NOT NULL,
                    pvstart text NOT NULL,
                    pvend text NOT NULL,
                    song_duration text NOT NULL,
                    off_ranking text NOT NULL,
                    ad_def text NOT NULL,
                    remaster text NOT NULL,
                    special_pv text NOT NULL,
                    challenge_track text NOT NULL,
                    bonus text NOT NULL,
                    genre_id text NOT NULL,
                    title text NOT NULL,
                    artist text NOT NULL,
                    sort_jp_index text NOT NULL,
                    sort_ex_index text NOT NULL,
                    filename text NOT NULL
                ); """

MmScoreSq = """ CREATE TABLE IF NOT EXISTS mm_score (
                    id integer PRIMARY KEY,
                    track_id integer UNIQUE,
                    name text NOT NULL,
                    lv text NOT NULL,
                    designer_id text NOT NULL,
                    utage_mode text NOT NULL,
                    safename text NOT NULL
                );"""

MmTextOutArtistSq = """ CREATE TABLE IF NOT EXISTS mm_textout_artist (
                    id integer PRIMARY KEY,
                    artist_id text UNIQUE,
                    ex_track_artist text,
                    jp_track_artist text
                );"""

MmTextOutTitleSq = """ CREATE TABLE IF NOT EXISTS mm_textout_track (
                    id integer PRIMARY KEY,
                    track_id text UNIQUE,
                    ex_track_title text,
                    jp_track_title text
                );"""

MmTextOutDesignerSq = """ CREATE TABLE IF NOT EXISTS mm_textout_designer (
                    id integer PRIMARY KEY,
                    designer_id text UNIQUE,
                    ex_designer_name text,
                    jp_designer_name text
                );"""

SoundBgmSq = """ CREATE TABLE IF NOT EXISTS sound_bgm (
                    id integer PRIMARY KEY,
                    title text UNIQUE,
                    track_id text UNIQUE
                );"""

Tables = [MmMusicSq, MmScoreSq, MmTextOutArtistSq, MmTextOutTitleSq, MmTextOutDesignerSq, SoundBgmSq]
