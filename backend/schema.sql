PRAGMA foreign_keys = ON;

-- USERS
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    name TEXT NOT NULL,
    home_club TEXT,
    current_handicap REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- COURSES
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT,
    par INTEGER NOT NULL,
    course_rating REAL NOT NULL,
    slope_rating INTEGER NOT NULL
);

-- HOLES
CREATE TABLE holes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    hole_number INTEGER NOT NULL CHECK (hole_number BETWEEN 1 AND 18),
    par INTEGER NOT NULL,
    stroke_index INTEGER NOT NULL CHECK (stroke_index BETWEEN 1 AND 18),
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- TEE TIMES
CREATE TABLE tee_times (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id INTEGER NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    holes INTEGER NOT NULL CHECK (holes IN (9, 18)),
    is_booked INTEGER DEFAULT 0,
    FOREIGN KEY (course_id) REFERENCES courses(id)
);

-- BOOKINGS
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    teetime_id INTEGER NOT NULL UNIQUE,
    booked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (teetime_id) REFERENCES tee_times(id)
);

-- ROUNDS
CREATE TABLE rounds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    teetime_id INTEGER,
    date_played DATE NOT NULL,
    tee TEXT,
    gross_score INTEGER,
    handicap_at_time REAL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (course_id) REFERENCES courses(id),
    FOREIGN KEY (teetime_id) REFERENCES tee_times(id)
);

-- HOLE SCORES
CREATE TABLE hole_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    round_id INTEGER NOT NULL,
    hole_id INTEGER NOT NULL,
    strokes INTEGER NOT NULL CHECK (strokes > 0),
    FOREIGN KEY (round_id) REFERENCES rounds(id),
    FOREIGN KEY (hole_id) REFERENCES holes(id),
    UNIQUE (round_id, hole_id)
);

-- HANDICAP HISTORY
CREATE TABLE handicap_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    handicap REAL NOT NULL,
    calculated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
