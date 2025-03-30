import time
import board
import adafruit_dht

# Initialize the DHT22 sensor on GPIO4
dht_device = adafruit_dht.DHT22(board.D4)

try:
    while True:
        # Try to get the temperature and humidity from the sensor
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        if temperature is not None and humidity is not None:
            print(f"Temp: {temperature}C  Humidity: {humidity}%")
        else:
            print("Failed to retrieve data from the sensor")

        # Wait for 2 seconds before the next reading
        time.sleep(5)

except KeyboardInterrupt:
    print("Program interrupted. Cleaning up...")
    # Cleanup the sensor when the program is interrupted
    dht_device.exit()