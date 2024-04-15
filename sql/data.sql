PRAGMA foreign_keys = ON;

-- users
-- Example: username: test_user1, email: test_user1@umich.edu, password: test_user1
INSERT INTO users
VALUES('test_user1', 'test_user1@umich.edu', 'sha512$9241f1bd1f558e0b3aa86c82abdd79ee800e7b7028d4a66f24f2264b3a8951511d070e879bd2023b0f2aa7b780aa91fe6c176d90ef877a983ec34b40f07f0917', current_timestamp);

INSERT INTO users
VALUES('test_user2', 'test_user2@umich.edu', 'sha512$6e6bd12290be5f112d69587d932f263eeae98627c220dee5052ec3ba473c377960c9e301507bb6b354016cb984a1c16bf3cfc963bd5a20e33b2b17184d06a0fb', current_timestamp);

