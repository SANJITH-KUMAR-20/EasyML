
-- TABLE FOR EACH HANDLING USER SESSIONS
-- At the begining of each session the user session id is extracted from the user table and a model table id is generated and the model 
CREATE TABLE IF NOT EXISTS `usersession` (
    `user_session_id` VARCHAR(255) NOT NULL UNIQUE,
    `model_table_name` VARCHAR(255) UNIQUE,
    `model_train_count` INT(5),
    `best_model_cls` VARCHAR(255),
    `best_model_reg` VARCHAR(255),
    `best_model_clus` VARCHAR(255),
    PRIMARY KEY(`user_session_id`)
);


-- STORED PROCEDURE TO CREATE A MODEL TABLE FOR EACH USER PERSESSION
-- DELIMITER $$

-- CREATE PROCEDURE create_model_tabel(IN model_table_name VARCHAR(255))

-- BEGIN
--     SET @query = CONCAT('CREATE TABLE IF NOT EXISTS ', model_table_name, ' (
--         `model_id` VARCHAR (255) NOT NULL UNIQUE,
--         `model_name` VARCHAR(255),
--         `mse` FLOAT,
--         `mae` FLOAT,
--         `r2` FLOAT,
--         `accuracy` FLOAT,
--         `precision` FLOAT,
--         `recall` FLOAT,
--         `f1` FLOAT,
--         `ari` FLOAT,
--         `nmi` FLOAT,
--         `sil` FLOAT,
--         PRIMARY KEY(`model_id`)
--     )');
--     PREPARE stmt FROM @query;
--     EXECUTE stmt;
--     DEALLOCATE PREPARE stmt;
-- END$$

-- DELIMITER ;

-- -- TRIGGER TO CREATE THE MODEL TABLE
-- DELIMITER $$

-- CREATE TRIGGER allocate_model_table
-- AFTER INSERT ON usersession
-- FOR EACH ROW
-- BEGIN
--     CALL create_model_tabel(NEW.model_table_name);
-- END$$

-- DELIMITER ;


