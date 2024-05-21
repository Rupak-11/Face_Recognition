import pandas as pd
from pymongo import MongoClient


csv_file = './Attendance.csv'
data = pd.read_csv(csv_file)

print("Columns in the CSV file:", data.columns)

# Connect to MongoDB
client = MongoClient('mongodb+srv://rupakchowdhury144:1234@rup11.66iibjt.mongodb.net/')  # Replace with your MongoDB URI
db = client['attendance_db']  
collection = db['entries']  

# Convert DataFrame to dictionary
data_dict = data.to_dict("records")

# Debug: Print the first few records to verify their structure
print("First few records from the CSV:", data_dict[:5])

# Insert or update data into MongoDB
for record in data_dict:
    try:
        
        print("Processing record:", record)
        
        result = collection.update_one(
            {'name': record['Name'], 'timestamp': record['Time']},  
            {'$set': record},
            upsert=True
        )
        if result.upserted_id:
            print(f"Inserted new record: {record}")
        else:
            print(f"Updated existing record: {record}")
    except KeyError as ke:
        print(f"KeyError: {ke} in record {record}")
    except Exception as e:
        print(f"Error: {e}")

print("Data processed successfully into MongoDB")
