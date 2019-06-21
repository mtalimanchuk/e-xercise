DROP TABLE IF EXISTS task;
DROP TABLE IF EXISTS student;

CREATE TABLE student
(
  id         BIGINT       NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username   VARCHAR(100) NOT NULL UNIQUE,
  is_active  BOOLEAN      NOT NULL,
  unique_url VARCHAR(255) NOT NULL UNIQUE
);
CREATE TABLE task
(
  id                   BIGINT        NOT NULL AUTO_INCREMENT PRIMARY KEY,
  student_id           BIGINT        NOT NULL,
  content              VARCHAR(1024) NOT NULL,
  is_completed         BOOLEAN       NOT NULL DEFAULT FALSE,
  completion_timestamp TIMESTAMP
);

ALTER TABLE task
  ADD CONSTRAINT FOREIGN KEY fk_task_to_student (student_id) REFERENCES student (id);