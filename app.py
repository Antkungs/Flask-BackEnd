from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)


DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'your_database')
DB_USER = os.getenv('DB_USER', 'your_username')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'your_password')

def  connect():
    connection = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return connection
    
@app.route('/', methods=['GET'])
def index():
    return "hello"

@app.route('/voice_analysis', methods=['GET'])
def voice_analysis():
    try:
        # เชื่อมต่อฐานข้อมูล
        conn = connect()  # ใช้ฟังก์ชันที่เชื่อมต่อกับฐานข้อมูล
        if conn is None:
            return jsonify({"error": "Failed to connect to the database"}), 500
        
        cursor = conn.cursor()

        # ดึงข้อมูลทั้งหมดจากตาราง voice_analysis
        cursor.execute("SELECT * FROM voice_analysis")
        db_results = cursor.fetchall()  # ใช้ fetchall() เพื่อดึงข้อมูลทั้งหมด

        # สร้างลิสต์สำหรับเก็บข้อมูลที่ดึงมา
        analysis_data = []
        male_count = 0
        female_count = 0
        total_confidence = 0
        total_entries = 0

        for row in db_results:
            analysis_data.append({
                'id': row[0],  # ID (Primary key)
                'timestamp': row[1],  # Timestamp ของการทำนาย
                'predicted_gender': row[2],  # เพศที่ทำนาย
                'confidence_score': row[3],  # คะแนนความมั่นใจ
            })

            if row[2].lower() == 'male':  # Assuming 'male' is the predicted gender
                    male_count += 1
            elif row[2].lower() == 'female':  # Assuming 'female' is the predicted gender
                female_count += 1

            total_confidence += row[3]
            total_entries += 1

        # คำนวณค่าเฉลี่ยของคะแนนความมั่นใจ
        avg_confidence = total_confidence / total_entries if total_entries > 0 else 0
        # ปิดการเชื่อมต่อ
        cursor.close()
        conn.close()
        # ส่งข้อมูลกลับในรูปแบบ JSON
        return jsonify({'analysis_data': analysis_data,
            'average_confidence_score': avg_confidence,
            'male_count': male_count,
            'female_count': female_count
            })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def insert_message(text, received_at):
    try:
        conn = connect()
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO mqtt_messages (text, received_at)
        VALUES (%s, %s)
        """
        cursor.execute(insert_query, (text, received_at))
        conn.commit()

        print("Message inserted successfully")

    except Exception as e:
        print(f"Error inserting message: {str(e)}")

    finally:
        cursor.close()
        conn.close()
        
def insert_voice_analysis(timestamp,predicted_gender, confidence_score):
    try:
        conn = connect()
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO voice_analysis (timestamp, predicted_gender, confidence_score)
        VALUES (%s, %s, %s)
        """

        cursor.execute(insert_query, (timestamp, predicted_gender, confidence_score))
        conn.commit()

        print("Voice analysis inserted successfully")

    except Exception as e:
        print(f"Error inserting data: {str(e)}")

    finally:
        cursor.close()
        conn.close()
    
if __name__ == "__main__":
    app.run(host="0.0.0.0" ,port=5000,debug=True)
