#CREATE USER classroom@localhost IDENTIFIED BY 'changeme';
#CREATE DATABASE classroom_db;
#GRANT ALL PRIVILEGES ON classroom_db@localhost TO classroom@localhost IDENTIFIED BY 'changeme';

DROP TABLE IF EXISTS assignments;
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
  id      BIGINT        NOT NULL AUTO_INCREMENT PRIMARY KEY,
  content VARCHAR(1024) NOT NULL
);

CREATE TABLE assignments
(
  id                   BIGINT  NOT NULL AUTO_INCREMENT PRIMARY KEY,
  student_id           BIGINT  NOT NULL,
  task_id              BIGINT  NOT NULL,
  is_completed         BOOLEAN NOT NULL DEFAULT FALSE,
  completion_timestamp TIMESTAMP
);

ALTER TABLE assignments
  ADD CONSTRAINT FOREIGN KEY fk_assignments_to_student (student_id) REFERENCES student (id);
ALTER TABLE assignments
  ADD CONSTRAINT FOREIGN KEY fk_assignments_to_task (task_id) REFERENCES task (id);
ALTER TABLE assignments
  ADD UNIQUE (student_id, task_id);