# User authentication
# MBTI quiz flow
# Calculating personality results
# Serving these through RESTful API endpoints

from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
import os
import uuid
from datetime import datetime
import logging

# logging
if not os.path.exists('logs'):
    os.mkdir('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# database setup
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',
    'database': 'music_quiz'
}

# Initializes Flask app
app = Flask(__name__)

def get_db_connection():
    """
    Creates a connection to the MySQL database.
    
    :return: MySQL database connection
    :rtype: mysql.connector.connection.MySQLConnection
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        logger.error(f"Database connection error: {e}")
        raise

def generate_mbti_playlist(cursor, mbti_type):
    """
    Generates a 10-song playist based on MBTI type with proportional distribution:
    - 5 songs from primary genre (affinity=3)
    - 3 songs from secondary genre (affinity=2)
    - 2 songs from tertiary genre (affinity=1)
    
    :param cursor: Database cursor
    :param mbti_type: Four-letter MBTI type (e.g., "INFJ")
    :return: List of song dictionaries
    """
    # Gets the three genres associated with this MBTI type
    cursor.execute(
        """
        SELECT genre, affinity_score
        FROM mbti_genre_affinities
        WHERE mbti_type = %s
        ORDER BY affinity_score DESC
        """,
        (mbti_type,)
    )
    genres = cursor.fetchall()
    
    if len(genres) < 3:
        raise ValueError(f"Not enough genres defined for MBTI type {mbti_type}")
    
    primary_genre = genres[0]['genre']
    secondary_genre = genres[1]['genre']
    tertiary_genre = genres[2]['genre']
    
    # Gets songs from each genre
    songs = []
    
    # Gets primary genre songs (5)
    cursor.execute(
        """
        SELECT s.id, s.title, a.name as artist, s.genre
        FROM song s
        JOIN artist a ON s.artist_id = a.id
        WHERE s.genre = %s
        ORDER BY RAND()
        LIMIT 5
        """,
        (primary_genre,)
    )
    primary_songs = cursor.fetchall()
    
    # Gets genre songs (3)
    cursor.execute(
        """
        SELECT s.id, s.title, a.name as artist, s.genre
        FROM song s
        JOIN artist a ON s.artist_id = a.id
        WHERE s.genre = %s
        ORDER BY RAND()
        LIMIT 3
        """,
        (secondary_genre,)
    )
    secondary_songs = cursor.fetchall()
    
    # Gets genre songs (2)
    cursor.execute(
        """
        SELECT s.id, s.title, a.name as artist, s.genre
        FROM song s
        JOIN artist a ON s.artist_id = a.id
        WHERE s.genre = %s
        ORDER BY RAND()
        LIMIT 2
        """,
        (tertiary_genre,)
    )
    tertiary_songs = cursor.fetchall()
    
    # Combine all songs and add match reasons
    for song in primary_songs:
        song['match_reason'] = f"Your primary genre match: {primary_genre}"
        songs.append(song)
        
    for song in secondary_songs:
        song['match_reason'] = f"Your secondary genre match: {secondary_genre}"
        songs.append(song)
        
    for song in tertiary_songs:
        song['match_reason'] = f"Your tertiary genre match: {tertiary_genre}"
        songs.append(song)
    
    return songs

# API Routes

# nshows quiz_id started_at total_questions
@app.route('/api/quiz/start', methods=['POST'])
def start_quiz():
    """
    Start a new quiz session.
    
    This endpoint returns info about the available questions.
    
    :return: JSON with quiz details
    :rtype: flask.Response
    
    :statuscode 201: Quiz info retrieved
    :statuscode 500: Server error
    """
    logger.info("Starting new quiz")
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Gets question count
        cursor.execute("SELECT COUNT(*) as count FROM questions")
        total_questions = cursor.fetchone()['count']
        
        cursor.close()
        conn.close()
        
        # Generates a unique ID
        frontend_id = str(uuid.uuid4())
        
        logger.info(f"Quiz info retrieved: {total_questions} questions")
        return jsonify({
            # Just for the frontend to track the quiz!
            "quiz_id": frontend_id,
            "total_questions": total_questions,
            "started_at": datetime.utcnow().isoformat()
        }), 201
        
    except Error as e:
        logger.error(f"Error getting quiz info: {e}")
        return jsonify({"message": "Failed to get quiz info", "error": str(e)}), 500

# not working - The requested URL was not found on the server. 
@app.route('/api/quiz/questions/<int:question_number>', methods=['GET'])
def get_question(question_number):
    """
    Get a specific question by its order number.
    
    :param question_number: The question order number (1-based)
    :type question_number: int
    :return: JSON with question detais and answer options
    :rtype: flask.Response
    
    :statuscode 200: Question retrieved successfully
    :statuscode 404: Question not found
    :statuscode 500: Server error
    """
    logger.info(f"Getting question number: {question_number}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Gets question by order
        cursor.execute(
            """
            SELECT id, question_text, question_order
            FROM questions
            WHERE question_order = %s
            """,
            (question_number,)
        )
        question = cursor.fetchone()
        
        if not question:
            cursor.close()
            conn.close()
            return jsonify({"message": f"Question number {question_number} not found"}), 404
        
        # Get options for this question
        cursor.execute(
            """
            SELECT id, option_text
            FROM answers
            WHERE question_id = %s
            """,
            (question['id'],)
        )
        options = [{"id": row['id'], "text": row['option_text']} for row in cursor.fetchall()]
        
        # Gets total question counts
        cursor.execute("SELECT COUNT(*) as count FROM questions")
        total_questions = cursor.fetchone()['count']
        
        cursor.close()
        conn.close()
        
        logger.info(f"Returning question {question['id']} (number {question_number})")
        return jsonify({
            "question_id": question['id'],
            "question_text": question['question_text'],
            "options": options,
            "question_number": question_number,
            "total_questions": total_questions
        }), 200
        
    except Error as e:
        logger.error(f"Error fetching question: {e}")
        return jsonify({"message": "Failed to fetch question", "error": str(e)}), 500

# unsupported Media Type
@app.route('/api/quiz/process-answers', methods=['POST'])
def process_answers():
    """
    Process all answers at once and get personality results and music recommendations.
    
    This endpoint takes an array of answers, calculates the MBTI personality type,
    and generates personalized music recommendations based on the results.
    
    :return: JSON with personality profile and music recommendations
    :rtype: flask.Response
    
    :statuscode 200: Answers processed successfully with results
    :statuscode 400: Invalid request format
    :statuscode 500: Server error
    
    **Example request**:
    
    .. sourcecode:: http
    
       POST /api/quiz/process-answers HTTP/1.1
       Host: example.com
       Accept: application/json
       Content-Type: application/json
       
       {
         "answers": [
           {"question_id": 1, "selected_option_id": 2},
           {"question_id": 2, "selected_option_id": 4},
           ...
         ]
       }
    """
    logger.info("Processing quiz answers")
    try:
        data = request.json
        
        if not data or 'answers' not in data or not isinstance(data['answers'], list):
            return jsonify({"message": "Invalid request. Missing answers array"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Extract the option IDs
        option_ids = [answer['selected_option_id'] for answer in data['answers'] 
                      if 'selected_option_id' in answer]
        

        if not option_ids:
            cursor.close()
            conn.close()
            return jsonify({"message": "No valid answer options provided"}), 400
        
        # Gets trait impacts for the selected options
        format_strings = ','.join(['%s'] * len(option_ids))
        cursor.execute(
            f"""
            SELECT trait_name, SUM(score_impact) as total_score
            FROM answers
            WHERE id IN ({format_strings})
            GROUP BY trait_name
            """,
            tuple(option_ids)
        )
        trait_scores = {row['trait_name']: row['total_score'] for row in cursor.fetchall()}
        
        # Calculates MBTI personality type
        e_score = trait_scores.get('E', 0)
        i_score = trait_scores.get('I', 0)
        s_score = trait_scores.get('S', 0)
        n_score = trait_scores.get('N', 0)
        t_score = trait_scores.get('T', 0)
        f_score = trait_scores.get('F', 0)
        j_score = trait_scores.get('J', 0)
        p_score = trait_scores.get('P', 0)
        
        # Determines each dimension
        ei_dimension = 'I' if i_score > e_score else 'E'
        sn_dimension = 'N' if n_score > s_score else 'S'
        tf_dimension = 'F' if f_score > t_score else 'T'
        jp_dimension = 'J' if j_score > p_score else 'P'
        
        # Combine into MBTI type
        mbti_type = f"{ei_dimension}{sn_dimension}{tf_dimension}{jp_dimension}"
        
        # Generates playlist with function that distributes songs by genre
        recommended_songs = generate_mbti_playlist(cursor, mbti_type)
        
        # Creatse playlist entry
        playlist_id = str(uuid.uuid4())
        playlist_name = f"{mbti_type} Music Mix"
        playlist_description = f"Music recommendations based on your {mbti_type} personality type"
        
        cursor.execute(
            """
            INSERT INTO playlist (id, mbti_type, name, description)
            VALUES (%s, %s, %s, %s)
            """,
            (playlist_id, mbti_type, playlist_name, playlist_description)
        )
        
        # Adds songs to the playlist
        for position, song in enumerate(recommended_songs, 1):
            cursor.execute(
                """
                INSERT INTO playlist_songs (playlist_id, song_id)
                VALUES (%s, %s)
                """,
                (playlist_id, song['id'])
            )
        
        conn.commit()
        
        # Formats the result for a response
        personality_profile = {
            "mbti_type": mbti_type,
            "dimensions": [
                {"name": "Introversion-Extraversion", "letter": ei_dimension, 
                 "score": abs(i_score - e_score)},
                {"name": "Intuition-Sensing", "letter": sn_dimension, 
                 "score": abs(n_score - s_score)},
                {"name": "Feeling-Thinking", "letter": tf_dimension, 
                 "score": abs(f_score - t_score)},
                {"name": "Judging-Perceiving", "letter": jp_dimension, 
                 "score": abs(j_score - p_score)}
            ]
        }
        
        # Formats songs for response
        recommended_tracks = []
        for song in recommended_songs:
            recommended_tracks.append({
                "id": song['id'],
                "title": song['title'],
                "artist": song['artist'],
                "genre": song['genre'],
                "match_reason": song['match_reason']
            })
        
        cursor.close()
        conn.close()
        
        logger.info(f"Quiz processed with MBTI type {mbti_type}")
        return jsonify({
            "personality_profile": personality_profile,
            "playlist": {
                "id": playlist_id,
                "name": playlist_name,
                "description": playlist_description,
                "tracks": recommended_tracks
            }
        }), 200
        
    except Error as e:
        logger.error(f"Error processing answers: {e}")
        return jsonify({"message": "Failed to process answers", "error": str(e)}), 500

# playlist not found
@app.route('/api/playlists/<string:playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    """
    Get a specific playlist with its songs.
    
    This endpoint retrieves the details of a specific playlist.
    
    :param playlist_id: The ID of the playlist
    :type playlist_id: str
    :return: JSON with playlist details and tracks
    :rtype: flask.Response
    
    :statuscode 200: Playlist retrieved successfully
    :statuscode 404: Playlist not found
    :statuscode 500: Server error
    """
    logger.info(f"Getting playlist: {playlist_id}")
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Checks if playist exists
        cursor.execute(
            """
            SELECT * FROM playlist WHERE id = %s
            """,
            (playlist_id,)
        )
        playlist = cursor.fetchone()
        
        if not playlist:
            cursor.close()
            conn.close()
            return jsonify({"message": "Playlist not found"}), 404
        
        # Get songs in playlist
        cursor.execute(
            """
            SELECT ps.*, s.title, a.name as artist, s.genre
            FROM playlist_songs ps
            JOIN song s ON ps.song_id = s.id
            JOIN artist a ON s.artist_id = a.id
            WHERE ps.playlist_id = %s
            """,
            (playlist_id,)
        )
        songs = []
        for row in cursor.fetchall():
            song_genre = row['genre']
            # Shows match reason based on genre and MBTI type
            cursor.execute(
                """
                SELECT affinity_score FROM mbti_genre_affinities 
                WHERE mbti_type = %s AND genre = %s
                """,
                (playlist['mbti_type'], song_genre)
            )
            affinity = cursor.fetchone()
            if affinity:
                if affinity['affinity_score'] == 3:
                    match_reason = f"Your primary genre match: {song_genre}"
                elif affinity['affinity_score'] == 2:
                    match_reason = f"Your secondary genre match: {song_genre}"
                else:
                    match_reason = f"Your tertiary genre match: {song_genre}"
            else:
                match_reason = f"Matches your {playlist['mbti_type']} music preferences"
            
            songs.append({
                "id": row['song_id'],
                "title": row['title'],
                "artist": row['artist'],
                "genre": row['genre'],
                "match_reason": match_reason
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({
            "id": playlist['id'],
            "name": playlist['name'],
            "description": playlist['description'],
            "mbti_type": playlist['mbti_type'],
            "tracks": songs
        }), 200
        
    except Error as e:
        logger.error(f"Error fetching playlist: {e}")
        return jsonify({"message": "Failed to fetch playlist", "error": str(e)}), 500

# Shows the correct output
@app.route('/api/mbti-types', methods=['GET'])
def get_mbti_types():
    """
    Get information about all MBTI personality types.
    
    This endpoint provides a summary of all 16 MBTI personality types
    and their associated music preferences.
    
    :return: JSON with MBTI types and their music preferences
    :rtype: flask.Response
    
    :statuscode 200: MBTI types retrieved successfully
    :statuscode 500: Server error
    """
    logger.info("Getting MBTI types info")
    try:
        # Dictionary of MBTI type names
        mbti_names = {
            "INTJ": "The Architect",
            "INTP": "The Logician",
            "ENTJ": "The Commander",
            "ENTP": "The Debater",
            "INFJ": "The Advocate",
            "INFP": "The Mediator",
            "ENFJ": "The Protagonist",
            "ENFP": "The Campaigner",
            "ISTJ": "The Logistician",
            "ISFJ": "The Defender",
            "ESTJ": "The Executive",
            "ESFJ": "The Consul",
            "ISTP": "The Virtuoso",
            "ISFP": "The Adventurer",
            "ESTP": "The Entrepreneur",
            "ESFP": "The Entertainer"
        }
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Get preferred genres for each MBTI type
        mbti_types = []
        for mbti_type, name in mbti_names.items():
            cursor.execute(
                """
                SELECT genre
                FROM mbti_genre_affinities
                WHERE mbti_type = %s
                ORDER BY affinity_score DESC
                LIMIT 3
                """,
                (mbti_type,)
            )
            genres = [row['genre'] for row in cursor.fetchall()]
            
            mbti_types.append({
                "type": mbti_type,
                "name": name,
                "preferred_genres": genres
            })
        
        cursor.close()
        conn.close()
        
        return jsonify({"mbti_types": mbti_types}), 200
        
    except Error as e:
        logger.error(f"Error fetching MBTI types: {e}")
        return jsonify({"message": "Failed to fetch MBTI types", "error": str(e)}), 500

# Shoes correct output
@app.route('/')
def index():
    """
    Root endpoint that returns basic API info.
    
    :return: JSON with API information
    :rtype: flask.Response
    
    :statuscode 200: API info retrieved successfully
    """
    return jsonify({
        "name": "Music Personality Quiz API",
        "description": "Discover your music preferences based on MBTI personality type",
        "endpoints": {
            "get_question": "/api/quiz/questions/{question_number}",
            "process_answers": "/api/quiz/process-answers",
            "get_mbti_types": "/api/mbti-types"
        }
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
