import Adafruit_DHT

# Set the sensor type and GPIO pin
sensor = Adafruit_DHT.DHT22
pin = 4  # GPIO4 (you can change this if you're using a different GPIO pin)

# Try to read the sensor
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

if humidity is not None and temperature is not None:
    print(f'Temperature: {temperature:.1f}°C')
    print(f'Humidity: {humidity:.1f}%')
else:
    print('Failed to read sensor data. Try again!')
