
--Insert 10 courses into the course database
INSERT INTO courses (name, location, par, course_rating, slope_rating) VALUES
('Royal County Down', 'Newcastle, Northern Ireland', 72, 74.2, 142),
('Royal Portrush – Dunluce Links', 'Portrush, Northern Ireland', 72, 75.8, 147),
('St Andrews – Old Course', 'St Andrews, Scotland', 72, 73.1, 132),
('Muirfield', 'Gullane, Scotland', 71, 74.1, 138),
('Carnoustie Championship Course', 'Carnoustie, Scotland', 72, 75.5, 145),
('Royal Birkdale', 'Southport, England', 72, 74.0, 140),
('Ballybunion Old Course', 'Ballybunion, Ireland', 72, 74.8, 144),
('Portmarnock Golf Club', 'Dublin, Ireland', 72, 73.5, 136),
('Pebble Beach Golf Links', 'California, USA', 72, 75.5, 145),
('Augusta National', 'Georgia, USA', 72, 74.6, 137);


--Generate holes (1-18) for each course
WITH RECURSIVE hole_numbers(n) AS (
    SELECT 1
    UNION ALL
    SELECT n + 1 FROM hole_numbers WHERE n < 18
)
INSERT INTO holes (course_id, hole_number, par, stroke_index)
SELECT
    c.id,
    h.n,
    CASE
        WHEN h.n IN (3, 7, 11, 16) THEN 5
        WHEN h.n IN (2, 6, 10, 14) THEN 3
        ELSE 4
    END AS par,
    h.n AS stroke_index
FROM courses c
CROSS JOIN hole_numbers h;


-- add tee time to each course (08:00am to 16:00pm)
WITH RECURSIVE dates(d) AS (
    SELECT date('now', '+14 days')
    UNION ALL
    SELECT date(d, '+1 day')
    FROM dates
    WHERE d < date('now', '+27 days')
),
timeslot(t) AS (
    SELECT time('08:00')
    UNION ALL
    SELECT time(t, '+10 minutes')
    FROM timeslot
    WHERE t < time('16:00')
)
INSERT INTO tee_times (course_id, date, time, holes, is_booked)
SELECT
    c.id,
    d.d,
    t.t,
    18,
    0
FROM courses c
CROSS JOIN dates d
CROSS JOIN timeslot t;

--creating a test user
INSERT INTO users (email, password_hash, name)
VALUES ('test@golf.com', 'hashed_pw', 'Test Golfer');
