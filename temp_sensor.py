import smbus2
import bme280
import time

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
#data = bme280.sample(bus, address, calibration_params)

# the compensated_reading class has the following attributes
#print(data.id)
#print(data.timestamp)
#print(data.temperature)
#print(data.pressure)
#print(data.humidity)

# there is a handy string representation too
#print(data)

from influxdb import InfluxDBClient

client = InfluxDBClient(host='localhost', port=8086)

client.switch_database('tempsensor')

while True:
  data = bme280.sample(bus, address, calibration_params)
  json_body = [
    {
        "measurement": "temperature",
        "tags": {
            "unit": "Celsius"
        },
        "time": data.timestamp,
        "fields": {
            "temperature": data.temperature
         }
        },
        {        "measurement": "humidity",
        "tags": {
            "unit": "Percent"
        },
        "time": data.timestamp,
        "fields": {
            "humidity": data.humidity
        }
    },
    {
        "measurement": "pressure",
        "tags": {
            "unit": "hPa"
            },
        "time": data.timestamp,
        "fields": {
            "presure": data.pressure
            }
        } ]
  print(data)
  client.write_points(json_body)
  time.sleep(5)

