-- drop database if exists music_quiz;
CREATE DATABASE IF NOT EXISTS music_quiz;
use music_quiz;

-- Album
-- CREATE TABLE album ()

-- Artist
CREATE TABLE artist (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    genres JSON NOT NULL
);

-- Song
CREATE TABLE song (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INT NOT NULL,
    album VARCHAR(255),
    genre VARCHAR(100) NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES artist (id)
);

-- Playlist
CREATE TABLE playlist (
    id VARCHAR(36) PRIMARY KEY,
    mbti_type VARCHAR(4) NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

-- Playlist songs
CREATE TABLE playlist_songs (
    playlist_id VARCHAR(36) NOT NULL,
    song_id INT NOT NULL,
    PRIMARY KEY (playlist_id, song_id),
    FOREIGN KEY (playlist_id) REFERENCES playlist (id),
    FOREIGN KEY (song_id) REFERENCES song (id)
);

-- Personality traits
CREATE TABLE personality_traits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(10) UNIQUE NOT NULL,
    description TEXT NOT NULL
);

-- MBTI to genre mappings
CREATE TABLE mbti_genre_affinities (
    mbti_type VARCHAR(4) NOT NULL,
    genre VARCHAR(100) NOT NULL,
    affinity_score INT NOT NULL,
    PRIMARY KEY (mbti_type, genre)
);

-- Questions
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_text TEXT NOT NULL,
    question_order INT NOT NULL
);

-- Answers
CREATE TABLE answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    option_text TEXT NOT NULL,
    trait_name VARCHAR(10) NOT NULL,
    score_impact INT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions (id)
);

