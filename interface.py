import time
import board
import adafruit_dht
import boto3
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from flask import Flask, render_template, jsonify
from threading import Thread

# Initialize the DHT22 sensor on GPIO4
dht_device = adafruit_dht.DHT22(board.D4)

# Set up DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('DHT')  # Replace with your table name

# Function to safely convert floats to Decimals
def safe_decimal(value):
    try:
        return Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # Limiting precision to 2 decimal places
    except Exception as e:
        print(f"Error converting value {value} to Decimal: {e}")
        return Decimal('0.00')  # Return a default value if conversion fails

# Flask setup
app = Flask(__name__)

# Data storage
sensor_data = {'temperature': None, 'humidity': None, 'timestamp': None}

# Function to update the data from the sensor and DynamoDB
def update_sensor_data():
    global sensor_data
    while True:
        # Try to get the temperature and humidity from the sensor
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        if temperature is not None and humidity is not None:
            if temperature is not None and humidity is not None:
            # Get the current local time
                timestamp = datetime.now()

            # Convert it to a custom format
            formatted_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")

            # Update the data
            sensor_data = {
                'temperature': safe_decimal(temperature),
                'humidity': safe_decimal(humidity),
                'timestamp': formatted_timestamp
            }

            # Prepare data to be inserted into DynamoDB
            data = {
                'ID': formatted_timestamp,
                'Timestamp': formatted_timestamp,
                'temperature': sensor_data['temperature'],
                'humidity': sensor_data['humidity']
            }

            # Insert data into DynamoDB table
            try:
                table.put_item(Item=data)
                print("Data successfully written to DynamoDB")
            except Exception as e:
                print(f"Error writing to DynamoDB: {e}")
        else:
            print("Failed to retrieve data from the sensor")
        
        time.sleep(5)  # Wait for 10 seconds before the next reading

# Flask route to serve the sensor data
@app.route('/get_sensor_data')
def get_sensor_data():
    return jsonify(sensor_data)
# Flask route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Run the background thread to update sensor data
if __name__ == '__main__':
    # Start the background task in a separate thread
    thread = Thread(target=update_sensor_data)
    thread.daemon = True
    thread.start()

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)
