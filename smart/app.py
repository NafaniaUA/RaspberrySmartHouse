
from flask import Flask, render_template, redirect, send_file, send_from_directory
import RPi.GPIO as GPIO
import os
from temp import temperature 

import sqlite3
from datetime import date, datetime
app = Flask(__name__)


ledPin = 23
outletPin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(outletPin,GPIO.OUT)



@app.route('/')
def index():
	
	with open("text.txt", "r") as f:
		read = f.read()

	return render_template('home.html', content = read)


@app.route('/getfile/<name>')
def get_output_file(name):
    return send_file(name, as_attachment=True)

@app.route('/delfile/')
def dellog():
	open("text.txt", "w").close()
	return redirect('/')
		


@app.route('/light/')
def light():
	return render_template('light.html')

@app.route('/on/')
def on():
	GPIO.output(ledPin,1)
	return render_template('light.html')

@app.route('/off/')
def off():
	GPIO.output(ledPin,0)
	return render_template('light.html')

@app.route('/onoutlet/')
def onoutlet():
	GPIO.output(outletPin,1)
	return render_template('light.html')

@app.route('/offoutlet/')
def offoutlet():
	GPIO.output(outletPin,0)
	return render_template('light.html')

@app.route('/print_database/')
def print_items():
    con = sqlite3.connect('database.db')
    cur = con.cursor() 
	#cur.execute('DELETE FROM indicators WHERE huminity=0')
    cur.execute('SELECT temperature, huminity, date FROM indicators')
	       
    return render_template('print_database.html',  items = cur.fetchall())


#@app.route('/del_database/')
#def print_items():
#    con = sqlite3.connect('database.db')
 #   cur = con.cursor() 
#	sql = "DELETE FROM indicators WHERE temperature = '0'"
	##cur.execute('DELETE * FROM indicators')

#	cur.execute(sql,sss)

  #  com.commit()   

    ##cur.execute('SELECT temperature, huminity, date FROM indicators')
	       
 #   return redirect('/print_database/')





@app.route('/temperature/')
def temp():
	return temperature()
	#return render_template('temperature.html')



if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')
