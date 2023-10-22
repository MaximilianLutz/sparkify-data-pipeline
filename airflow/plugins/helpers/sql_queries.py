class SqlQueries:
    # Table Drop Queries
    staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
    staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
    songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
    user_table_drop = "DROP TABLE IF EXISTS users;"
    song_table_drop = "DROP TABLE IF EXISTS songs;"
    artist_table_drop = "DROP TABLE IF EXISTS artists;"
    time_table_drop = "DROP TABLE IF EXISTS time;"

    # Table Creation Queries
    staging_events_table_create = """
        CREATE TABLE IF NOT EXISTS staging_events (
            artist TEXT,
            auth TEXT,
            firstName TEXT,
            gender CHAR(1),
            itemInSession INT, 
            lastName TEXT,
            length FLOAT,
            level TEXT,
            location TEXT,
            method TEXT,
            page TEXT,
            registration BIGINT,
            sessionId INT,
            song TEXT,
            status INT,
            ts BIGINT,
            userAgent TEXT,
            userId INT
        );
    """

    staging_songs_table_create = """
        CREATE TABLE IF NOT EXISTS staging_songs (
            num_songs INT,
            artist_id TEXT,
            artist_latitude FLOAT,
            artist_longitude FLOAT,
            artist_location TEXT,
            artist_name TEXT,
            song_id TEXT,
            title TEXT,
            duration FLOAT,
            year INT
        );
    """

    songplay_table_create = """
        CREATE TABLE IF NOT EXISTS songplays (
            songplay_id TEXT PRIMARY KEY,
            start_time TIMESTAMP NOT NULL,
            user_id INT NOT NULL,
            level TEXT,
            song_id TEXT NOT NULL,
            artist_id TEXT NOT NULL,
            session_id INT,
            location TEXT,
            user_agent TEXT
        );
    """

    user_table_create = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            gender CHAR(1),
            level TEXT NOT NULL
        );
    """

    song_table_create = """
        CREATE TABLE IF NOT EXISTS songs (
            song_id TEXT PRIMARY KEY,
            title TEXT,
            artist_id TEXT NOT NULL,
            year INT,
            duration FLOAT
        );
    """

    artist_table_create = """
        CREATE TABLE IF NOT EXISTS artists (
            artist_id TEXT PRIMARY KEY,
            name TEXT,
            location TEXT,
            latitude FLOAT,
            longitude FLOAT
        );
    """

    time_table_create = """
        CREATE TABLE IF NOT EXISTS time (
            start_time TIMESTAMP PRIMARY KEY,
            hour INT,
            day INT,
            week INT,
            month INT,
            year INT,
            weekday INT
        );
    """

    #Table Insert Queries
    
    songplay_table_insert = """
        SELECT
            md5(events.sessionid || events.start_time) songplay_id,
            events.start_time, 
            events.userid, 
            events.level, 
            songs.song_id, 
            songs.artist_id, 
            events.sessionid,   
            events.location, 
            events.useragent
        FROM
            (SELECT TIMESTAMP 'epoch' + ts/1000 * interval '1 second' AS start_time, *
            FROM staging_events
            WHERE page='NextSong') events
        LEFT JOIN staging_songs songs
        ON events.song = songs.title
            AND events.artist = songs.artist_name
            AND events.length = songs.duration
            WHERE songs.song_id IS NOT NULL;
    """

    user_table_insert = """
        SELECT DISTINCT userid, firstname, lastname, gender, level
        FROM staging_events
        WHERE page='NextSong'
    """

    song_table_insert = """
        SELECT DISTINCT song_id, title, artist_id, year, duration
        FROM staging_songs
    """

    artist_table_insert = """
        SELECT DISTINCT artist_id, artist_name, artist_location, artist_latitude, artist_longitude
        FROM staging_songs
    """

    time_table_insert = """
        SELECT start_time, EXTRACT(hour FROM start_time), EXTRACT(day FROM start_time), EXTRACT(week FROM start_time),
               EXTRACT(month FROM start_time), EXTRACT(year FROM start_time), EXTRACT(dayofweek FROM start_time)
        FROM songplays
    """
    