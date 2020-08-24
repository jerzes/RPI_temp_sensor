import smbus2
import bme280
import datetime
import time
import logging

log_format = '%(ascitime)s %(levelname)s * %(message)s' 
logging.basicConfig(filename="tempsensor.log", format=log_format)
logger = logging.getLogger('tempsensor')

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)


from influxdb import InfluxDBClient


try:
    client = InfluxDBClient(host='localhost', port=8086)
except:
    raise Exception("err")
    logger.error('database connection error')
try:
    client.switch_database('tempsensor')
except:
    raise Exception("err")
    logger.error('database connection error')

while True:
  stamp = datetime.datetime.utcnow()
  data = bme280.sample(bus, address, calibration_params)
  json_body = [
    {
        "measurement": "temperature",
        "tags": {
            "unit": "Celsius"
        },
        "time": stamp,
        "fields": {
            "temperature": data.temperature
         }
        },
        {        "measurement": "humidity",
        "tags": {
            "unit": "Percent"
        },
        "time": stamp,
        "fields": {
            "humidity": data.humidity
        }
    },
    {
        "measurement": "pressure",
        "tags": {
            "unit": "hPa"
            },
        "time": stamp,
        "fields": {
            "presure": data.pressure
            }
        } ]
  
  try:
    client.write_points(json_body)
    time.sleep(5)
  except:
    logger.error('cant write to database')
    time.sleep(20)
