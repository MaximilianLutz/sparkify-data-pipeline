    # DROP Tables
    staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
    staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
    songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
    user_table_drop = "DROP TABLE IF EXISTS users;"
    song_table_drop = "DROP TABLE IF EXISTS songs;"
    artist_table_drop = "DROP TABLE IF EXISTS artists;"
    time_table_drop = "DROP TABLE IF EXISTS time;"

    # Create Tables
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