import psutil
import mysql.connector
import datetime
import os

db = mysql.connector.connect(
    host=os.getenv("DB_HOST", "172.31.8.18"),
    user=os.getenv("DB_USER", "devops"),
    password=os.getenv("DB_PASS", "rootpassword"),
    database=os.getenv("DB_NAME", "syslogs")
    # Try using 'devops' first, then fallback to 'root' if it fails
def connect_to_db():
    try:
        return mysql.connector.connect(
            host="172.31.8.18",
            user="devops",
            password="rootpassword",
            database="syslogs"
        )
    except mysql.connector.Error:
        print("⚠️ DevOps user failed, switching to root...")
        return mysql.connector.connect(
            host="172.31.8.18",
            user="root",
            password="rootpassword",
            database="syslogs"
        )
)

cursor = db.cursor()
cpu = psutil.cpu_percent()
mem = psutil.virtual_memory().percent
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
user_name = "Ibinabo" 
custom_message = "Group5, I am getting better in DevOps" 

cursor.execute("INSERT INTO stats (timestamp, cpu_usage, memory_usage, user_name, custom_message) VALUES (%s, %s, %s, %s, %s)",
               (timestamp, cpu, mem, user_name, custom_message))
db.commit()
cursor.close()
db.close()
print(f"Logged at {timestamp} | CPU: {cpu}%, MEM: {mem}%")
