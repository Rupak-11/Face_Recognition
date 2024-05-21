import pandas as pd
from pymongo import MongoClient

# Read the CSV file
csv_file = './Attendance.csv'
data = pd.read_csv(csv_file)

# Print the DataFrame columns to ensure they match what we expect
print("Columns in the CSV file:", data.columns)

# Connect to MongoDB
client = MongoClient('mongodb+srv://rupakchowdhury144:1234@rup11.66iibjt.mongodb.net/')  # Replace with your MongoDB URI
db = client['attendance_db']  # Replace with your database name
collection = db['entries']  # Replace with your collection name

# Convert DataFrame to dictionary
data_dict = data.to_dict("records")

# Debug: Print the first few records to verify their structure
print("First few records from the CSV:", data_dict[:5])

# Insert or update data into MongoDB
for record in data_dict:
    try:
        # Debug: Print the record being processed
        print("Processing record:", record)
        
        result = collection.update_one(
            {'name': record['Name'], 'timestamp': record['Time']},  # Ensure these match your CSV column names
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
