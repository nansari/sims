-- SQLite
-- ALTER TABLE password RENAME TO password_old;

-- CREATE TABLE password (
-- 	id INTEGER NOT NULL, 
-- 	password_hash VARCHAR(256) NOT NULL, 
-- 	user_id INTEGER NOT NULL, 
--     attempt_counts INTEGER DEFAULT 0,
--     is_allowed INTEGER DEFAULT 0,
--     last_attempt_time DATETIME DEFAULT NULL,
--     last_successful_attempt_time DATETIME DEFAULT NULL,
-- 	PRIMARY KEY (id), 
-- 	FOREIGN KEY(user_id) REFERENCES user (id), 
-- 	UNIQUE (user_id)
-- );


INSERT INTO password (user_id, password_hash) VALUES (1, 'scrypt:32768:8:1$p7EPi10FWc3wd83n$75cff340cabbec28d04bb48e37b29a6dca9fb6df69d866af12d0708ac021129df5fe3eee7e9e49b3ff9a11b76e9dedc5f455b778d9b4587cc16d8ea6fea7713e');
-- select * from password;

