from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import socket

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sensordata.sqlite3'

db = SQLAlchemy(app)

def get_ip_address():
	ip_address = '';
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8",80))
	ip_address = s.getsockname()[0]
	s.close()
	return ip_address

class SensorData(db.Model):
	id = db.Column('sensordata_id', db.Integer, primary_key=True)
	datetime = db.Column(db.DateTime, default=datetime.utcnow)
	temperature = db.Column(db.Integer,nullable=False)
	humidity = db.Column(db.Integer, nullable=False)
	is_gas_detected  = db.Column(db.Boolean, default=False, nullable=False)
	is_metal_detected  = db.Column(db.Boolean, default=False, nullable=False)
	
	def __repr__(self):
		return f'Temperature: {self.temperature}\nHummidity: {self.humidity}\nGas:{self.is_gas_detected}\nMetal: {self.is_metal_detected}'

@app.route('/')
def home():
	sensor_reading = SensorData.query.order_by(SensorData.datetime).first()
	print(sensor_reading)
	return render_template('index.html', data=sensor_reading)


@app.route('/sensor_history')
def sensor_history():
	sensor_data = reversed(SensorData.query.all())
	print(sensor_data)
	return render_template('sensor_history.html', sensor_data=sensor_data)
	
	
@app.route('/add_sensor_data', methods=['GET','POST'])
def add_sensor_data():
	if request.method == 'POST':
		temperature = request.form.get('temperature')
		humidity = request.form.get('humidity')
		is_gas_detected = bool(request.form.get('is_gas_detected'))
		is_metal_detected = bool(request.form.get('is_metal_detected'))
		sensor_data = SensorData(temperature=temperature, humidity=humidity, is_gas_detected=is_gas_detected, is_metal_detected=is_metal_detected)
		try:
			db.session.add(sensor_data)
			db.session.commit()
			print("Sensor data added successfully to the database.")
			return "Sensor data added successfully to the database."
		except Exception as e:
			print(f'Error occured: {e}')
			return "Cannot add data to database."
	return "Add sensor data via POST method."
	
	

	
if __name__ == "__main__":
	ip_address = get_ip_address()
	PORT = 5000
	app.run(host=ip_address, port=PORT, debug=True)
