import socket as sck
import threading as thr 
import time
import random
import string
import sqlite3
from datetime import datetime
import RPi.GPIO as GPIO
from flask import Flask, render_template, request, redirect, url_for, make_response
app = Flask(__name__)

sec=3

class AlphaBot(object): #classe per gestire il moviemento dell'AlphaBot
    def __init__(self, in1=13, in2=12, ena=6, in3=21, in4=20, enb=26):
        self.IN1 = in1
        self.IN2 = in2
        self.IN3 = in3
        self.IN4 = in4
        self.ENA = ena
        self.ENB = enb
        self.PA  = 25
        self.PB  = 25
        
        #setup iniziale del bot
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
        GPIO.setup(self.IN3, GPIO.OUT)
        GPIO.setup(self.IN4, GPIO.OUT)
        GPIO.setup(self.ENA, GPIO.OUT)
        GPIO.setup(self.ENB, GPIO.OUT)
        self.PWMA = GPIO.PWM(self.ENA,500)
        self.PWMB = GPIO.PWM(self.ENB,500)
        self.PWMA.start(self.PA)
        self.PWMB.start(self.PB)
        self.stop()

    def right(self, sec): #funzione che ruota sul posto verso destra il bot per "sec" secondi
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        time.sleep(sec) #continua a muoversi per la durata del moviemento indicata come parametro
        self.stop() #dopo aver concluso il movimento si ferma

    def stop(self): #funzione che ferma il bot
        self.PWMA.ChangeDutyCycle(0)
        self.PWMB.ChangeDutyCycle(0)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.LOW)

    def left(self, sec): #funzione che ruota sul posto verso sinistra il bot per "sec" secondi
        self.PWMA.ChangeDutyCycle(self.PA)
        self.PWMB.ChangeDutyCycle(self.PB)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        time.sleep(sec) #continua a muoversi per la durata del moviemento indicata come parametro
        self.stop() #dopo aver concluso il movimento si ferma

    def forward(self, sec, speed=30): #funzione che muove avanti il bot per "sec" secondi
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.LOW)
        GPIO.output(self.IN2, GPIO.HIGH)
        GPIO.output(self.IN3, GPIO.HIGH)
        GPIO.output(self.IN4, GPIO.LOW)
        time.sleep(sec) #continua a muoversi per la durata del moviemento indicata come parametro
        self.stop() #dopo aver concluso il movimento si ferma

    def backward(self, sec, speed=30): #funzione che muove indietro il bot per "sec" secondi
        self.PWMA.ChangeDutyCycle(speed)
        self.PWMB.ChangeDutyCycle(speed)
        GPIO.output(self.IN1, GPIO.HIGH)
        GPIO.output(self.IN2, GPIO.LOW)
        GPIO.output(self.IN3, GPIO.LOW)
        GPIO.output(self.IN4, GPIO.HIGH)
        time.sleep(sec) #continua a muoversi per la durata del moviemento indicata come parametro
        self.stop() #dopo aver concluso il movimento si ferma
    
    def runcommand(self,command):
        print(command)
        conn = sqlite3.connect("db.db") #crea una "connessione" col database
        cur = conn.cursor()
        cur.execute(f"SELECT sequenza FROM movements WHERE nome = '{command}'") #esegue la query indicata per trovare la sequenza giusta tramite il nome
        comandi = cur.fetchall()[0][0]
        l_comandi=comandi.split(":") #divide la sequenza in singoli comendi [movimento:tempo]
        for comando in l_comandi:
            c=comando[0] #preleva dalla stringa il movimento
            print(c)
            if c!="S":
                seconds=float(comando[1:]) #preleva dalla stringa i secondi e li mette float
            if c[0] == "F": #se il comando = F -> va avanti
                self.forward(seconds)
            elif c[0] == "S": #se il comando = S -> si ferma
                self.stop()
            elif c[0] == "B": #se il comando = B -> va indietro
                self.backward(seconds)
            elif c[0] == "R": #se il comando = R -> gira a destra
                self.right(seconds)
            elif c[0] == "L":  #se il comando = L -> gira a sinistra
                self.left(seconds)
            else:
                print("Errore di sintassi")
	    
    def set_pwm_a(self, value):
        self.PA = value
        self.PWMA.ChangeDutyCycle(self.PA)

    def set_pwm_b(self, value):
        self.PB = value
        self.PWMB.ChangeDutyCycle(self.PB)    
        
    def set_motor(self, left, right):
        if (right >= 0) and (right <= 100):
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            self.PWMA.ChangeDutyCycle(right)
        elif (right < 0) and (right >= -100):
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            self.PWMA.ChangeDutyCycle(0 - right)
        if (left >= 0) and (left <= 100):
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            self.PWMB.ChangeDutyCycle(left)
        elif (left < 0) and (left >= -100):
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            self.PWMB.ChangeDutyCycle(0 - left)

def validate(username, password):
    completion = False
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM Users")
    rows = cur.fetchall()
    for row in rows:
        dbUser = row[0]
        dbPass = row[1]
        if dbUser==username:
            completion=check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):
    return hashed_password == user_password

def dbAccesses(user):
    con = None
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    cur.execute(f"INSERT INTO Accesses ('User','Datetime') VALUES ('{user}','{datetime.now()}')")
    cur.execute("commit")
    con.close()

def dbActions(action,user):
    con = None
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    cur.execute(f"INSERT INTO Actions ('User','Action','Datetime') VALUES ('{user}','{action}','{datetime.now()}')")
    cur.execute("commit")
    con.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        completion = validate(username, password)
        if completion == False:
            error = 'Invalid Credentials. Please try again.'
        else:
            resp=make_response(redirect(url_for('control')))
            resp.set_cookie("username",username)
            return resp
    return render_template('login.html', error=error)

@app.route(f"/controlPage", methods=['GET', 'POST'])
def control():
    a=AlphaBot()
    dbAccesses(request.cookies.get("username"))
    if request.method == 'POST':
        if request.form.get('action1') == 'fw':
            a.forward(sec)
            action=f"fw"
        elif request.form.get('action2') == 'bw':
            a.backward(sec)
            action=f"bw"
        elif request.form.get('action3') == 'tr':
            a.right(sec)
            action=f"tr"
        elif request.form.get('action4') == 'tf':
            a.left(sec)
            action=f"tf"
        elif request.form.get('conf') == 'conf':
            command = request.form['commandbox']
            if command != "":    
                a.runcommand(command)
                action=command
            else:    
                action="error" 
        else:
            action="error"
        dbActions(action,request.cookies.get("username"))
    return render_template("index.html")

if __name__=="__main__":
    app.run(debug=True, host='192.168.0.141')