DELETE
FROM assignments;
DELETE
FROM task;
DELETE
FROM student;

INSERT INTO student(id, username, is_active, unique_url)
VALUES (1, 'v.zadov', 1, 'eOyjOZb9eIfULKMmGczVdCQvAuCnYw0BFVpc8os2QUtn7j4Ow4fiGJX1svOtJuGDOGkcHx'),
       (2, 'p.pastushenko', 1, 'iODbI4gffgZgALeVJSm2CiRef34ViRz1Xq2BtWazjREfq557LowecSt6mabynGM2zWm2o6'),
       (3, 't.kombat', 1, '6ct6iJZACWZA85J9tzBTbV93tFZrq0xQWTYURDdYNmIlnSS6LYfc0Aav8l8kVYqvebVdOW'),
       (4, 'n.zadova', 1, '26z97fO8jaiGuKKI5mmkHW5pWKEbGlS2agkIR8GygOOyG2EeBZOnOb2gBXK97UvKONcXn0'),
       (5, 's.smorkovich', 0, 'p4KRIPI7QhF21yCS6N1IeNj7sdzKGWTmpkpGLPKs4QGurtdWCmfCRRueCSvNsJazTZMnym');

INSERT INTO task(id, content)
VALUES (1, 'SCRAPED TABOEBA SENTENCE ONE'),
       (2, 'SCRAPED TABOEBA SENTENCE TWO'),
       (3, 'SCRAPED TABOEBA SENTENCE THREE'),
       (4, 'SCRAPED TABOEBA SENTENCE FOUR'),
       (5, 'SCRAPED TABOEBA SENTENCE FIVE'),
       (6, 'SCRAPED TABOEBA SENTENCE SIX'),
       (7, 'SCRAPED TABOEBA SENTENCE SEVEN');

INSERT INTO assignments(student_id, task_id)
VALUES (1, 1),
       (1, 2),
       (1, 3),
       (1, 4),
       (2, 1),
       (2, 2),
       (2, 3),
       (2, 4),
       (2, 5),
       (3, 1),
       (3, 2),
       (4, 1),
       (4, 2),
       (4, 3),
       (5, 1),
       (5, 3),
       (4, 4);