import socket
import threading
import cv2
import struct
import time
import serial
import lgpio as GPIO
import csv
#for doc https://rpi-lgpio.readthedocs.io/en/latest/api.html#RPi.GPIO.SERIAL
#manual for step motor driver (OK2D60BH) https://www.oyostepper.es/images/upload/File/OK2D60BH-manual.pdf
 
host = "192.168.137.162"
#host = "127.0.1.1"
port_joy_stick = 9999
port_camera_1 = 9998
port_camera_2 = 9997

running = True

width = 640
height = 480

#global yaw_rotate,pitch_rotate,trigger,lever_pull,pump_toggle

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket_3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind((host, port_joy_stick))
server_socket_2.bind((host, port_camera_1))
server_socket_3.bind((host, port_camera_2))

server_socket.listen(1)
server_socket_2.listen(1)
server_socket_3.listen(1)

print(f"Waiting for connection 1 on {host}:{port_joy_stick}...")
print(f"Waiting for connection 2 on {host}:{port_camera_1}...")
print(f"Waiting for connection 3 on {host}:{port_camera_2}...")

conn, addr = server_socket.accept()
conn_2, addr_2 = server_socket_2.accept()
conn_3, addr_3 = server_socket_3.accept()

print("Connected by", addr)

class pi_to_pc:
    def __init__(self,conn,conn_2,conn_3):
        self.conn = conn
        self.conn_2 = conn_2
        self.conn_3 = conn_3
       
    def send_video_1(self):
        cap_1 = cv2.VideoCapture(0)
        cap_1.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap_1.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        cap_1.set(cv2.CAP_PROP_FPS, 30)

        while running:
            ret, frame = cap_1.read()
            if not ret:
                break
            frame = cv2.resize(frame, (width, height))
            _, buffer = cv2.imencode('.jpg', frame)
            data = buffer.tobytes()
            size = len(data)
            try:
                self.conn_2.sendall(struct.pack('!I', size))
                self.conn_2.sendall(data)
            except:
                break
        cap_1.release()

    def send_video_2(self):
        cap_2 = cv2.VideoCapture(2)
        cap_2.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap_2.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        cap_2.set(cv2.CAP_PROP_FPS, 30)

        while running:
            ret, frame = cap_2.read()
            if not ret:
                break
            frame = cv2.resize(frame, (width, height))
            _, buffer = cv2.imencode('.jpg', frame)
            data = buffer.tobytes()
            size = len(data)
            try:
                self.conn_3.sendall(struct.pack('!I', size))
                self.conn_3.sendall(data)
            except:
                break
        cap_2.release()

class pi_to_motor:
    def __init__(self,conn):
        self.conn = conn
        self.pump_toggle = 0.0
        self.toggle_sw = 0.0
        self.previous_pump_toggle = 0.0
        self.yaw_rotate = 0.0
        self.pitch_rotate = 0.0
        self.trigger = 0.0
        self.lever_pull = 0.0
        self.forward_assist = 0.0
        self.running = running
    
    def receive_joystick(self):
        while self.running:
            try:
                joy_data = self.conn.recv(24)# 6 floats (4 bytes each)
                if not joy_data:
                    break
                self.yaw_rotate,self.pitch_rotate,self.trigger,self.lever_pull,self.pump_toggle,self.forward_assist = struct.unpack('ffffff', joy_data)     
                #print(f"yaw={self.yaw_rotate:.2f}, pitch={self.pitch_rotate:.2f} trigger={self.trigger:.2f}, lever={self.lever_pull:.2f}, pump={self.toggle_sw:.2f} forward_assist : {self.forward_assist:.2f}")
                          
            except:
                break

    def toggle_switch(self) :
        
        while self.running : # to make toggle switch
            if self.previous_pump_toggle == 0 and self.pump_toggle == 1 : #pump toggle start from 0
                self.toggle_sw = 1-self.toggle_sw#self.toggle_sw will be 1 in the first loop
                # print(f"Toggle switch state: {self.toggle_sw}")
            self.previous_pump_toggle = self.pump_toggle#this makeprev_toggle ius update to go to new loop of if condition
            time.sleep(0.02)
    
    def send_data_to_arduino(self):
        old_yaw = None
        old_pitch = None
        old_trigger = None
        old_lock = None
        old_data = None
        yaw = None
        pitch = None
        trigger = None
        lock = None  
        data = None

        try:
            # Initialize the serial connection once
            ser = serial.Serial(
                port='/dev/ttyUSB0',
                baudrate=9600,
                timeout=0.5
            )
            print("Serial connection to Arduino established.")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            return

        while running:
            yaw = f"yaw_rotate{self.yaw_rotate:.2f}\n"
            pitch = f"pitch_rotate{self.pitch_rotate:.2f}\n"
            trigger = f"trigger{self.trigger:.1f}\n"
            lock = f"lock{self.lever_pull:.1f}\n"
            #data = f"data{self.forward_assist:.1f}\n"
            
            try:
                    
                if  yaw != old_yaw :
                    ser.write(yaw.encode('utf-8'))
                    print(f"Sent: {yaw.strip()}")
                else :
                    pass

                if pitch != old_pitch :
                    ser.write(pitch.encode('utf-8'))
                    print(f"Sent: {pitch.strip()}")
                else :
                    pass

                if trigger != old_trigger :
                    ser.write(trigger.encode('utf-8'))
                    print(f"Sent: {trigger.strip()}")
                else :
                    pass
                
                if lock != old_lock :
                    ser.write(lock.encode('utf-8'))
                    print(f"Sent: {lock.strip()}")
                else :
                    pass

                """if data != old_data :
                    ser.write(data.encode('utf-8'))
                    print(f"Sent: {data.strip()}")"""
                
                old_yaw = yaw
                old_pitch = pitch
                old_trigger = trigger
                old_lock = lock
                old_data = data

                #time.sleep(0.01)#to send data not too fast

                if ser.in_waiting > 0:
                    response = ser.readline().decode('utf-8', errors='ignore').rstrip()
                    print(f"Received: {response}")
                else :
                    pass
       
            except Exception as e:
                print(f"Error during serial communication: {e}")
                break

    def send_data_to_step_motor_yaw(self):
        # Initialize GPIO for stepper motor control
        GPIO.GPIO.setmode(GPIO.BOARD)
        GPIO.GPIO.setup(18, GPIO.GPIO.OUT)  # Example pin for step control
        GPIO.GPIO.setup(23, GPIO.GPIO.OUT)  # Example pin for direction control

    def send_data_to_step_motor_pitch(self):
        # Initialize GPIO for stepper motor control
        GPIO.GPIO.setmode(GPIO.BOARD)
        GPIO.GPIO.setup(24, GPIO.GPIO.OUT)  # Example pin for step control
        GPIO.GPIO.setup(25, GPIO.GPIO.OUT)  # Example pin for direction control

class arduino_to_pi:
    def __init__(self,conn):
        self.conn = conn

    def receive_loadcell_from_arduino(self):
        while True:
            try:
                ser = serial.Serial(
                    port='/dev/ttyUSB0',
                    baudrate=9600,
                    timeout=10 #0.5
                )
                print("Serial connection to Arduino for load cell established.")
                
                while True:
                    if ser.in_waiting > 0:
                        loadcell_data = ser.readline().decode('utf-8', errors='ignore').rstrip()
                        #print(f"Load Cell Data: {loadcell_data}")
                        # Here you can send loadcell_data back to PC if needed
                        #self.conn.sendall(loadcell_data.encode('utf-8'))
                        # this you can also log the data to a file ifpreferred
                        with open('loadcell_data.csv', mode='w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow([time.time(), loadcell_data])
                            file.flush()

                    else:
                        time.sleep(0.1)  # Avoid busy waiting

                    time.sleep(0.1)

            except KeyboardInterrupt:
                print("Arduino connection stopped by user.")
                break
            
pc = pi_to_pc(conn,conn_2,conn_3)
to_Arduino = pi_to_motor(conn)
arduino_go_to_pi = arduino_to_pi(conn)

t1 = threading.Thread(target=pc.send_video_1, daemon=True)
t2 = threading.Thread(target=to_Arduino.receive_joystick, daemon=True)
t3 = threading.Thread(target=to_Arduino.toggle_switch, daemon=True)
t4 = threading.Thread(target=to_Arduino.send_data_to_arduino, daemon=True)
t5 = threading.Thread(target=pc.send_video_2, daemon=True)
t6 = threading.Thread(target = arduino_go_to_pi.receive_loadcell_from_arduino, daemon=True)

t1.start()
t5.start()
t2.start()
t3.start()
t4.start()
t6.start()

t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()

conn.close()
conn_2.close()
conn_3.close()

server_socket.close()
server_socket_2.close()
server_socket_3.close()
