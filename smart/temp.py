
from flask import Flask, render_template,redirect

import sqlite3
import mysql.connector
import RPi.GPIO as GPIO
import dht11
import time

import calendar
from datetime import datetime,date



app = Flask(__name__)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()


instance = dht11.DHT11(pin=22)

    
@app.route("/temperature/")
def temperature():
    weekday = calendar.day_name[date.today().weekday()]
    monthdate = date.today()
    datetimetoday = datetime.now()
    result = instance.read()
    temp = result.temperature
    hum = result.humidity
    
   
    try:
        con = sqlite3.connect('database.db')
        cur = con.cursor()  
        print ("Connected")
        

        cur.execute('INSERT INTO indicators VALUES (?,?,?)', (temp,hum,datetimetoday))
        con.commit()
        
        
        cur.close()

    except:
        return "mistake"
        
    
    return render_template("temperature.html",temp=temp, hum = hum, weekday=weekday, monthdate=monthdate)	



if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0")
	



