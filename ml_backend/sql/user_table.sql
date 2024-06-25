CREATE TABLE IF NOT EXISTS `User` (
 `user_name` VARCHAR(50) NOT NULL,
 `mail_id` VARCHAR(100) NOT NULL UNIQUE,
 `permanent_session_id` VARCHAR(255) UNIQUE NOT NULL,
 `password` VARCHAR(8) NOT NULL,
 PRIMARY KEY (`mail_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- INSERT INTO user (user_name, mail_id, password) VALUES ('ist4d','fdfdhgfhd@gmail.com','dummy123');

SELECT * FROM user;