"""
Module containing functions for interacting with the SQLite database (e.g., CRUD operations on passwords).
"""

import sqlite3

# Sqlite DB file. (TODO: Move it to environment)
DB_FILE = "../db/key-guardian.db"


def create_password_table():
    """Create the password table"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
		CREATE TABLE IF NOT EXISTS passwords (
			id INTEGER PRIMARY KEY,
			user_id INTEGER,
			website TEXT,
			username TEXT,
			password TEXT,
			notes TEXT,
            salt TEXT,
			FOREIGN KEY(user_id) REFERENCES users(id)
		)
	"""
    )

    conn.commit()
    conn.close()


def store_password(user_id, website, username, password, salt, notes=""):
    """Store a new password"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
		INSERT INTO passwords (user_id, website, username, password, notes, salt)
		VALUES (?, ?, ?, ?, ?, ?)
	""",
        (user_id, website, username, password, notes, salt),
    )

    conn.commit()
    conn.close()


def get_passwords(user_id):
    """Retrieve all passwords for a user"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT website, username, password, notes, salt FROM passwords WHERE user_id = ?",
        (user_id,),
    )
    passwords = cursor.fetchall()

    conn.close()
    return passwords


def get_salt(user_id, website):
    """Retrieve salt for a password based on user_id and website"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT salt FROM passwords WHERE user_id = ? AND website = ?",
        (user_id, website),
    )
    salt = cursor.fetchone()

    conn.close()
    return salt[0]


def update_password(user_id, website, new_password):
    """Update an existing password"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
		UPDATE passwords 
		SET password = ? 
		WHERE user_id = ? AND website = ?
	""",
        (new_password, user_id, website),
    )

    conn.commit()
    conn.close()


def delete_password(user_id, website):
    """Delete a password"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM passwords WHERE user_id = ? AND website = ?", (user_id, website)
    )

    conn.commit()
    conn.close()
