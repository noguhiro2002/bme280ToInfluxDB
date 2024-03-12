import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from bme280_get_params import bme280Reader 
import json


config_path = './bme280ToInfluxdb_config.json'

# 設定ファイルの読み込み
with open(config_path, 'r') as config_file:
    config = json.load(config_file)

token = config['INFLUXDB_TOKEN']
org = config['INFLUXDB_ORG']
url = config['INFLUXDB_URL']
bucket = config['INFLUXDB_BUCKET']

measurementName=config['INFLUXDB_MEASUREMENT']
tag_roomName=config['INFLUXDB_tag_roomName']
tag_deviceName=config['INFLUXDB_tag_deviceName']
data_interval_sec=int(config['data_interval_sec'])


sensor = bme280Reader()  # with default pass number and I2C address 


## Start Process ##
# Init influxdb client
write_client = InfluxDBClient(url=url, token=token, org=org)
write_api = write_client.write_api(write_options=SYNCHRONOUS)

while True:
    try:
        sensorValue = sensor.readData()
        point = (
            Point(measurementName)
            .tag("roomName", tag_roomName)
            .tag("deviceName", tag_deviceName)
            .field("temperature_degCel", float(sensorValue["temp_degCel"]))
            .field("humidity_percent", float(sensorValue["hum_percent"]))
            .field("pressure_hPa",float(sensorValue["pressure_hPa"]))
        )
        write_api.write(bucket=bucket, org=org, record=point)
    except Exception as e:
        print(f"Error: {e}")  # ログ出力
    time.sleep(data_interval_sec)
