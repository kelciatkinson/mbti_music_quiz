-- Music Personality Quiz Data

USE music_quiz;

-- MBTI Personality Traits
-- INSERT INTO personality_traits (name, description) VALUES
-- ('E', 'Extraversion - Focuses energy outward and gets energized by social interactions'),
-- ('I', 'Introversion - Focuses energy inward and gets energized by time alone'),
-- ('S', 'Sensing - Takes in information through the five senses, focusing on concrete facts'),
-- ('N', 'Intuition - Takes in information through patterns and impressions, focusing on meaning'),
-- ('T', 'Thinking - Makes decisions based on logic and objective analysis'),
-- ('F', 'Feeling - Makes decisions based on personal values and how actions affect others'),
-- ('J', 'Judging - Prefers structure, order, and resolution'),
-- ('P', 'Perceiving - Prefers flexibility, spontaneity, and keeping options open');

-- Questions (5 for each dimension)
INSERT INTO questions (question_order, question_text) VALUES
-- E vs I questions
(1, 'After a long day, you prefer to:'),
(2, 'At parties or gatherings, you typically:'),
(3, 'When listening to music, you often:'),
(4, 'You prefer concerts that are:'),
(5, 'Your ideal music listening experience involves:');

-- E vs I answers
INSERT INTO answers (question_id, option_text, trait_name, score_impact) VALUES
(1, 'Meet friends or go to a social event', 'E', 1),
(1, 'Spend quiet time alone', 'I', 1),
(2, 'Talk to many different people', 'E', 1),
(2, 'Speak with a few people you know well', 'I', 1),
(3, 'Play it in the background during social activities', 'E', 1),
(3, 'Listen attentively with headphones', 'I', 1),
(4, 'High-energy with large crowds', 'E', 1),
(4, 'Intimate venues with focused performances', 'I', 1),
(5, 'Dancing or singing along with others', 'E', 1),
(5, 'Deeply analyzing the music on your own', 'I', 1);

-- S vs N questions
INSERT INTO questions (question_order, question_text) VALUES
(6, 'You''re drawn to lyrics that:'),
(7, 'When discovering new music, you typically:'),
(8, 'You prefer songs that:'),
(9, 'When you hear a new song, you first notice:'),
(10, 'You appreciate artists who:');

-- S vs N answers
INSERT INTO answers (question_id, option_text, trait_name, score_impact) VALUES
(6, 'Tell concrete stories with specific details', 'S', 1),
(6, 'Use metaphors and explore abstract concepts', 'N', 1),
(7, 'Focus on the sound quality and technical aspects', 'S', 1),
(7, 'Look for innovative approaches and unique ideas', 'N', 1),
(8, 'Have clear, traditional structures', 'S', 1),
(8, 'Experiment with unconventional patterns', 'N', 1),
(9, 'The specific instruments and production details', 'S', 1),
(9, 'The overall mood and what it reminds you of', 'N', 1),
(10, 'Perfect their craft and maintain a consistent style', 'S', 1),
(10, 'Constantly reinvent themselves and evolve', 'N', 1);

-- T vs F questions
INSERT INTO questions (question_order, question_text) VALUES
(11, 'You value music that:'),
(12, 'When evaluating a song, you focus on:'),
(13, 'You''re more drawn to music that:'),
(14, 'When choosing music for others, you consider:'),
(15, 'You''re drawn to artists who:');

-- T vs F answers
INSERT INTO answers (question_id, option_text, trait_name, score_impact) VALUES
(11, 'Shows technical skill and precision', 'T', 0.7),
(11, 'Conveys authentic emotion and connects emotionally', 'F', 1),
(12, 'How well it''s constructed and performed', 'T', 1),
(12, 'How it makes you and others feel', 'F', 1),
(13, 'Demonstrates complex arrangements and structures', 'T', 1),
(13, 'Expresses deep personal feelings and experiences', 'F', 1),
(14, 'What objectively fits the occasion or activity', 'T', 1),
(14, 'What would make everyone feel good and connected', 'F', 1),
(15, 'Display masterful technique and logical composition', 'T', 1),
(15, 'Express personal values and emotional experiences', 'F', 1);

-- J vs P questions
INSERT INTO questions (question_order, question_text) VALUES
(16, 'Your music collection is:'),
(17, 'When at a concert, you prefer:'),
(18, 'Your approach to finding new music is:'),
(19, 'When creating a playlist, you typically:'),
(20, 'You prefer music that:');

-- J vs P answers
INSERT INTO answers (question_id, option_text, trait_name, score_impact) VALUES
(16, 'Well-organized by genre, artist, or playlist', 'J', 1),
(16, 'Eclectic and constantly evolving', 'P', 1),
(17, 'Knowing the setlist in advance', 'J', 1),
(17, 'Being surprised by unexpected performances', 'P', 1),
(18, 'Following a structured method (certain blogs, review sites)', 'J', 1),
(18, 'Spontaneously discovering through various channels', 'P', 1),
(19, 'Plan it carefully with a specific theme or purpose', 'J', 1),
(19, 'Add songs as inspiration strikes, letting it develop naturally', 'P', 1),
(20, 'Has clear resolution and satisfying conclusions', 'J', 1),
(20, 'Leaves room for interpretation and improvisation', 'P', 1);

-- Artists
INSERT INTO artist (name, genres) VALUES
('Pink Floyd', '["Progressive Rock", "Rock"]'),
('Radiohead', '["Alternative Rock", "Experimental"]'),
('Miles Davis', '["Jazz"]'),
('Bob Dylan', '["Folk", "Rock"]'),
('Beatles', '["Rock", "Pop"]'),
('Kendrick Lamar', '["Hip-Hop", "Rap"]'),
('Daft Punk', '["Electronic", "Dance"]'),
('Fleetwood Mac', '["Rock", "Pop"]'),
('Johnny Cash', '["Country", "Folk"]'),
('Tame Impala', '["Psychedelic Rock", "Alternative"]'),
('Frank Ocean', '["R&B", "Soul"]'),
('David Bowie', '["Rock", "Art Rock"]');

-- Songs
INSERT INTO song (title, artist_id, album, genre) VALUES
('Comfortably Numb', 1, 'The Wall', 'Progressive Rock'),
('Wish You Were Here', 1, 'Wish You Were Here', 'Progressive Rock'),
('Paranoid Android', 2, 'OK Computer', 'Alternative Rock'),
('Karma Police', 2, 'OK Computer', 'Alternative Rock'),
('So What', 3, 'Kind of Blue', 'Jazz'),
('Blue in Green', 3, 'Kind of Blue', 'Jazz'),
('Blowin'' in the Wind', 4, 'The Freewheelin'' Bob Dylan', 'Folk'),
('Like a Rolling Stone', 4, 'Highway 61 Revisited', 'Rock'),
('Hey Jude', 5, 'The Beatles (White Album)', 'Rock'),
('Let It Be', 5, 'Let It Be', 'Pop'),
('HUMBLE.', 6, 'DAMN.', 'Hip-Hop'),
('Alright', 6, 'To Pimp a Butterfly', 'Hip-Hop'),
('Get Lucky', 7, 'Random Access Memories', 'Electronic'),
('Around the World', 7, 'Homework', 'Electronic'),
('Dreams', 8, 'Rumours', 'Rock'),
('Go Your Own Way', 8, 'Rumours', 'Rock'),
('Ring of Fire', 9, 'Ring of Fire: The Best of Johnny Cash', 'Country'),
('Hurt', 9, 'American IV: The Man Comes Around', 'Country'),
('The Less I Know The Better', 10, 'Currents', 'Psychedelic Rock'),
('Let It Happen', 10, 'Currents', 'Psychedelic Rock'),
('Thinking Bout You', 11, 'Channel Orange', 'R&B'),
('Pyramids', 11, 'Channel Orange', 'R&B'),
('Heroes', 12, 'Heroes', 'Art Rock'),
('Space Oddity', 12, 'Space Oddity', 'Art Rock');

-- Types and genres
INSERT INTO mbti_genre_affinities (mbti_type, genre, affinity_score) VALUES

-- INTJ
('INTJ', 'Progressive Rock', 3),
('INTJ', 'Experimental', 2),
('INTJ', 'Electronic', 1),

-- INTP
('INTP', 'Electronic', 3),
('INTP', 'Jazz', 2),
('INTP', 'Alternative Rock', 1),

-- INFJ
('INFJ', 'Folk', 3),
('INFJ', 'Psychedelic Rock', 2),
('INFJ', 'Ambient', 1),

-- INFP
('INFP', 'Folk', 3),
('INFP', 'Alternative Rock', 2),
('INFP', 'R&B', 1),

-- ISTJ
('ISTJ', 'Jazz', 3),
('ISTJ', 'Rock', 2),
('ISTJ', 'Country', 1),

-- ISFJ
('ISFJ', 'Folk', 3),
('ISFJ', 'Pop', 2),
('ISFJ', 'Country', 1),

-- ISTP
('ISTP', 'Rock', 3),
('ISTP', 'Electronic', 2),
('ISTP', 'Hip-Hop', 1),

-- ISFP
('ISFP', 'Pop', 3),
('ISFP', 'Folk', 2),
('ISFP', 'Jazz', 1),

-- ENTJ
('ENTJ', 'Art Rock', 3),
('ENTJ', 'Rock', 2),
('ENTJ', 'Hip-Hop', 1),

-- ENTP
('ENTP', 'Alternative Rock', 3),
('ENTP', 'Hip-Hop', 2),
('ENTP', 'Electronic', 1),

-- ENFJ
('ENFJ', 'Pop', 3),
('ENFJ', 'Rock', 2),
('ENFJ', 'Folk', 1),

-- ENFP
('ENFP', 'Pop', 3),
('ENFP', 'Electronic', 2),
('ENFP', 'Folk', 1),


-- ESTJ
('ESTJ', 'Rock', 3),
('ESTJ', 'Country', 2),
('ESTJ', 'Pop', 1),

-- ESFJ
('ESFJ', 'Pop', 3),
('ESFJ', 'Rock', 2),
('ESFJ', 'Country', 1),

-- ESTP
('ESTP', 'Hip-Hop', 3),
('ESTP', 'Electronic', 2),
('ESTP', 'Rock', 1),

-- ESFP
('ESFP', 'Pop', 3),
('ESFP', 'Electronic', 2),
('ESFP', 'Hip-Hop', 1);
