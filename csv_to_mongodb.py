import pandas as pd
from pymongo import MongoClient

# Read the CSV file
csv_file = './Attendance.csv'
data = pd.read_csv(csv_file)

# Connect to MongoDB
client = MongoClient('mongodb+srv://rupakchowdhury144:1234@rup11.66iibjt.mongodb.net/')  # Replace with your MongoDB URI
db = client['attendance_db']  # Replace with your database name
collection = db['entries']  # Replace with your collection name

# Convert DataFrame to dictionary
data_dict = data.to_dict("records")

# Insert or update data into MongoDB
for record in data_dict:
    try:
        result = collection.update_one(
            {'name': record['name'], 'timestamp': record['timestamp']},  # Replace with your unique fields
            {'$set': record},
            upsert=True
        )
        if result.upserted_id:
            print(f"Inserted new record: {record}")
        else:
            print(f"Updated existing record: {record}")
    except Exception as e:
        print(f"Error: {e}")

print("Data processed successfully into MongoDB")
