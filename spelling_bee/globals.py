# !TEMPORARY
words = ['livid']
userlist = [938772342, 993189741]

messages = {
    'lonely': 'Nobody wants to play with you. Try again later.',
    'initiative': '%r wants to play. /join to start',
}

queries = {
    'is_playing':
        "SELECT * FROM active_games WHERE session=%r",
    'both_answered':
        "SELECT answered FROM %r",
    'drop':
        "DROP TABLE %r",
    'delete session':
        "DELETE FROM active_games WHERE session = %r",
    'delete_from_w2p':
        "DELETE FROM wishtoplay WHERE uid=%r",
    'face_control':
        "SELECT uid FROM wishtoplay WHERE w2p IS 1 AND creator IS NOT 1",
    'current_game':
        "SELECT player FROM active_games WHERE session = %r",
    'current_word':
        "SELECT current_word FROM %r WHERE player = %r",
    'current_score':
        "SELECT score FROM %r WHERE player = %r",
    'current_response':
        "SELECT response FROM %r WHERE player = %r",
    'add_user':
        "INSERT INTO wishtoplay VALUES(%r, 1, %r)",
    'update_opponents':
        "UPDATE %r SET %r = %r WHERE player = %r",

    'game_instance': """
        CREATE TABLE 
        IF NOT EXISTS 
        {table}
        (
        player INTEGER,
        answered NUMERIC,
        response TEXT,
        score NUMERIC,
        current_word TEXT
        )
        """,

    'register': """
        INSERT OR IGNORE 
        INTO %r 
        (player, answered, response, score, current_word)
        VALUES
        (%r, %r, %r, %r, %r)
        """,

    'create_w2p': """
        CREATE TABLE 
        IF NOT EXISTS 
        wishtoplay
        (
        uid INTEGER,
        w2p NUMERIC,
        creator NUMERIC
        );
        """,

    'create_active_games': """
        CREATE TABLE 
        IF NOT EXISTS 
        active_games
        (
        player INTEGER,
        session TEXT
        );
        """,

    'update_active_games': """
        INSERT OR IGNORE 
        INTO 
        active_games 
        VALUES
        (
        %r, %r
        );
        """,
}
