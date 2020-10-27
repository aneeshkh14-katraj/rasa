import mysql.connector
from datetime import datetime


def DataUpdate(name, contact, email, pcm, cet, jee):
    # establishing the connection
    conn = mysql.connector.connect(
        host="localhost",
        port="3306",  # 3306 is the default port number
        user="root",
        passwd="",
        database="chatbot_data"
    )

    # Creating a cursor object using the cursor() method
    mycursor = conn.cursor(prepared=True)

    # Preparing SQL query to INSERT a record into the database.
    sql = """insert into student_data (student_name, student_contact, student_email, pcm_score, cet_score, jee_percentile, enquiry_dt_time) values (%s, %s, %s, %s, %s, %s, %s)"""

    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    InsertRow = (name, contact, email, pcm, cet, jee, formatted_date)

    try:
        # Executing the SQL command
        mycursor.execute(sql, InsertRow)
        # Commit your changes in the database
        conn.commit()
        print(mycursor.rowcount, "record inserted")

    except:
        # Rolling back in case of error
        conn.rollback()

    # Closing the connection
    conn.close()


if __name__ == "__main__":
    DataUpdate("test", 123, "abc@gmail.com", 245, 154)
