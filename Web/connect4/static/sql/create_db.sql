DROP TABLE IF EXISTS auth;
CREATE TABLE auth (
    a_user TEXT NOT NULL PRIMARY KEY,
    hashed_pass TEXT NOT NULL
);

DROP TABLE IF EXISTS stats;
CREATE TABLE stats (
    s_user TEXT NOT NULL PRIMARY KEY,
    games_won INTEGER DEFAULT 0,
    winstreak INTEGER DEFAULT 0,
    elo INTEGER DEFAULT 0,
    game TEXT DEFAULT null,
    opponent TEXT DEFAULT null
);

DROP TABLE IF EXISTS requests;
CREATE TABLE requests (
    challenged TEXT NOT NULL,
    challenger TEXT NOT NULL
);