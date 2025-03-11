CREATE DATABASE IF NOT EXISTS footy_db;
USE footy_db;

DROP TABLE IF EXISTS player;

CREATE TABLE player (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(50) NOT NULL,
    age INT,
    club VARCHAR(100) NOT NULL,
    nation VARCHAR(50) NOT NULL,
    appearances INT DEFAULT 0,
    goals INT DEFAULT 0,
    assists INT DEFAULT 0
);

LOAD DATA INFILE 'C:/Users/RIYA/Desktop/NAMAN/College/Advanced Python/footy/cleaned_players_data_v3.csv'
INTO TABLE player
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(name, position, age, club, nation, appearances, goals, assists);
