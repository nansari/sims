-- DELETE FROM password WHERE id == 1;
-- DELETE FROM user WHERE id = 1;
INSERT INTO user (email, username, bithdate) VALUES ('admin@sims.com', 'admin', 1990);
INSERT INTO user (email, username, bithdate) VALUES ('nobody@sims.com', 'nobody', 1990);
INSERT INTO password (user_id, password_hash) VALUES (1, 'scrypt:32768:8:1$p7EPi10FWc3wd83n$75cff340cabbec28d04bb48e37b29a6dca9fb6df69d866af12d0708ac021129df5fe3eee7e9e49b3ff9a11b76e9dedc5f455b778d9b4587cc16d8ea6fea7713e');
