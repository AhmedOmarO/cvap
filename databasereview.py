import sqlite3

def show_tables():
    conn = sqlite3.connect('./instance/faq_responses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'; ")
    print(cursor.fetchall())
    conn.close()


def show_submitted_question():
    conn = sqlite3.connect('./instance/faq_responses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT *  FROM submitted_question ; ")
    print(cursor.fetchall())
    conn.close()

show_submitted_question()

