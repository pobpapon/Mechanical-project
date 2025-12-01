import socket
import pygame
import time
import struct
import sys
import threading
import numpy
import cv2
import ultralytics
#import lgpio for control stepp motor if needed
#https://rpi-lgpio.readthedocs.io/en/latest/api.html#RPi.GPIO.SERIAL
#manual for step motor driver (OK2D60BH) https://www.oyostepper.es/images/upload/File/OK2D60BH-manual.pdf

host = "192.168.137.162"    # Raspberry Pi IP
port = 9999                 # joystick port
port_camera_1 = 9998
port_camera_2 = 9997

width = 1080
height = 720

running = True

# --- sockets ---
pc_socket = socket.socket()
pc_socket.connect((host, port))

pc_socket_1 = socket.socket()
pc_socket_1.connect((host, port_camera_1))

pc_socket_2 = socket.socket()
pc_socket_2.connect((host, port_camera_2))

# --- joystick init ---
pygame.init()
pygame.display.set_caption("pop camera stream v3.0")
pygame.joystick.init()
joysticks = []
for i in range(pygame.joystick.get_count()):
    j = pygame.joystick.Joystick(i)
    j.init()
    joysticks.append(j)

if not joysticks:
    print("No joystick found!")
    #sys.exit(1)

print("Joystick count:", len(joysticks))

# --- image processor class ---
class img_processing:
    def __init__(self, pc_socket, pc_socket_1, pc_socket_2, width=1080, height=720):
        # load model once
        self.model = ultralytics.YOLO("yolov8n.pt")
        self.running = True
        self.pc_socket = pc_socket
        self.pc_socket_1 = pc_socket_1
        self.pc_socket_2 = pc_socket_2
        self.frame = None
        self.frame_2 = None
        self.width = width
        self.height = height
        self.out = None

        # used to avoid running inference on same frame repeatedly
        self._frame_idx = 0
        self._frame2_idx = 0
        self._last_processed_idx = -1
        self._last_processed_idx2 = -1
        
#_________________crosshair setting_________________________

        self.center_x = (width // 2)
        self.center_y = (height // 2)
        self.crosshair_color = (0, 0, 255) #(B, G, R) #set for red crosshair
        self.thickness = 2
        self.length = 15  # Length of crosshair lines
        self.clickpos = None
        self.radius_crosshair = 20
        self.center_line_thickness = 1
        self.center_line_color = (190,253,65) #(B, G, R) #set for light green centre line
#___________________________________________________________
        
    def plus_crosshair(self,frame_for_crosshair) :
        #documentation :
        #https://www.geeksforgeeks.org/python/python-opencv-cv2-line-method/
        
        # Draw crosshair at the center
        # Horizontal line
        cv2.line(frame_for_crosshair, (self.center_x - self.length, self.center_y), (self.center_x + self.length, self.center_y), self.color, self.thickness)

        # Vertical line
        cv2.line(frame_for_crosshair, (self.center_x, self.center_y - self.length), (self.center_x, self.center_y + self.length), self.color, self.thickness)
        
    def circle_crosshair(self,frame_for_crosshair) :
        #documentation :
        #https://www.geeksforgeeks.org/python/python-opencv-cv2-circle-method/
        
        cv2.circle(frame_for_crosshair,center = (self.center_x, self.center_y), radius = 10, color = self.crosshair_color, thickness = self.thickness)

    def plus_and_circle_crosshair(self,frame_for_crosshair) :
        #documentation :
        #https://www.geeksforgeeks.org/python/python-opencv-cv2-circle-method/
        
        # Draw crosshair at the center
        # Horizontal line
        cv2.line(frame_for_crosshair, (self.center_x - self.length, self.center_y), (self.center_x + self.length, self.center_y), self.crosshair_color, self.thickness)

        # Vertical line
        cv2.line(frame_for_crosshair, (self.center_x, self.center_y - self.length), (self.center_x, self.center_y + self.length), self.crosshair_color, self.thickness)
        
        cv2.circle(frame_for_crosshair,center = (self.center_x, self.center_y), radius = self.radius_crosshair, color = self.crosshair_color, thickness = self.thickness)
        
    # -------------------------------------- Receive camera 1 -----------------------------------------------------------------------
    def receive_frame_1(self):
        while self.running:
            try:
                packed_size = self.pc_socket_1.recv(4)
                if not packed_size:
                    print("Camera1 connection closed")
                    break
                size = struct.unpack('!I', packed_size)[0]

                data = b''
                while len(data) < size:
                    packet = self.pc_socket_1.recv(min(4096, size - len(data)))
                    if not packet:
                        break
                    data += packet
                if len(data) != size:
                    print("Incomplete frame1 received")
                    continue

                image = numpy.frombuffer(data, dtype=numpy.uint8)
                frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
                if frame is not None:
                    self.frame = frame
                    self._frame_idx += 1
            except Exception as e:
                print("Error in receive_frame_1:", e)
                break
#------------------------------------------------------------------------------------------------------------------------------

# -------------------------------------- Receive camera 2 -----------------------------------------------------------------------
    def receive_frame_2(self):
        while self.running:
            try:
                packed_size = self.pc_socket_2.recv(4)
                if not packed_size:
                    print("Camera2 connection closed")
                    break
                size = struct.unpack('!I', packed_size)[0]

                data = b''
                while len(data) < size:
                    packet = self.pc_socket_2.recv(min(4096, size - len(data)))
                    if not packet:
                        break
                    data += packet
                if len(data) != size:
                    print("Incomplete frame2 received")
                    continue

                image = numpy.frombuffer(data, dtype=numpy.uint8)
                frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
                if frame is not None:
                    self.frame_2 = frame
                    self._frame2_idx += 1
            except Exception as e:
                print("Error in receive_frame_2:", e)
                break
#------------------------------------------------------------------------------------------------------------------------------           


# --------------------------------------- YOLO process + display for camera1 ----------------------------------------------
    def img_on_img_progress_and_show_1(self):
        adjust = 0  # vertical offset

        if not hasattr(self, 'clicked_pos') or self.clicked_pos_cam1 is None:
            self.clicked_pos_cam1 = (self.center_x, self.center_y)

        # Mouse callback function
        def mouse_event(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.clicked_pos_cam1 = (x, y)
                print(f"Mouse clicked at: {self.clicked_pos_cam1}")

        cv2.namedWindow('img progess by pop - cam1')
        cv2.setMouseCallback('img progess by pop - cam1', mouse_event)

        while self.running:
            if self.frame is None:
                time.sleep(0.0005)
                continue

            if self._frame_idx == self._last_processed_idx:
                time.sleep(0.0005)
                continue

            start_time = time.time()
            
            try:
                result = self.model(self.frame, verbose=False)
                annotated = result[0].plot() if result and len(result) > 0 else self.frame.copy()
            except Exception as e:
                print("YOLO error (cam1):", e)
                annotated = self.frame.copy()

            end_time = time.time()
            delay_ms = (end_time - start_time) * 1000
            fps = 1000 / delay_ms if delay_ms > 0 else 0

            cv2.putText(annotated, f'Delay: {delay_ms:.0f} ms | FPS: {fps:.2f}', (5, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
            cv2.putText(annotated, 'press q to Terminate program', (5, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

            annotated = cv2.resize(annotated, (self.width, self.height), interpolation=cv2.INTER_CUBIC)

            cx, cy = self.clicked_pos_cam1
            #create centre line
            cv2.line(annotated,(0,self.center_y), (self.width,self.center_y), self.center_line_color, self.center_line_thickness)
            cv2.line(annotated,(self.center_x,0), (self.center_x,self.height), self.center_line_color, self.center_line_thickness)
            
            #create crosshair
            cv2.line(annotated, (cx - self.length, cy ), (cx + self.length, cy),self.crosshair_color, self.thickness)
            cv2.line(annotated, (cx, cy  - self.length), (cx, cy  + self.length),self.crosshair_color, self.thickness)
            cv2.circle(annotated, center=(cx, cy + adjust), radius=self.radius_crosshair, color=self.crosshair_color, thickness=self.thickness)

            cv2.imshow('img progess by pop - cam1', annotated)

            self._last_processed_idx = self._frame_idx

            if cv2.waitKey(1) == ord('q'):
                self.running = False
                break

        cv2.destroyWindow('img progess by pop - cam1')
        
#------------------------------------------------------------------------------------------------------------------------------


# --------------------------------------- YOLO process + display for camera2 ----------------------------------------------
    def img_on_img_progress_and_show_2(self):
        
        if not hasattr(self, 'clicked_pos') or self.clicked_pos_cam2 is None:
            self.clicked_pos_cam2 = (self.center_x, self.center_y)

        # Mouse callback function
        def mouse_event(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                self.clicked_pos_cam2 = (x, y)
                print(f"Mouse clicked at: {self.clicked_pos_cam2}")

        cv2.namedWindow('img progess by pop - cam2')
        cv2.setMouseCallback('img progess by pop - cam2', mouse_event)

        while self.running:
            if self.frame_2 is None:
                time.sleep(0.0005)
                continue

            if self._frame2_idx == self._last_processed_idx2:
                time.sleep(0.0005)
                continue

            start_time = time.time()
            try:
                result = self.model(self.frame_2, verbose=False)
                annotated = result[0].plot() if result and len(result) > 0 else self.frame_2.copy()
            except Exception as e:
                print("YOLO error (cam2):", e)
                annotated = self.frame_2.copy()

            end_time = time.time()
            delay_ms = (end_time - start_time) * 1000
            fps = 1000 / delay_ms if delay_ms > 0 else 0

            cv2.putText(annotated, f'Delay: {delay_ms:.0f} ms | FPS: {fps:.2f}', (5, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)
            cv2.putText(annotated, 'press q to Terminate program', (5, 50),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 1)

            annotated = cv2.resize(annotated, (self.width, self.height), interpolation=cv2.INTER_CUBIC)

            cx, cy = self.clicked_pos_cam2
            A = 0  # Vertical offset
            
            #create centre line
            cv2.line(annotated,(0,self.center_y), (self.width,self.center_y), self.center_line_color, self.center_line_thickness)
            cv2.line(annotated,(self.center_x,0), (self.center_x,self.height), self.center_line_color, self.center_line_thickness)
            
            #create crosshair
            cv2.line(annotated, (cx - self.length, cy + A), (cx + self.length, cy + A),self.crosshair_color, self.thickness)
            cv2.line(annotated, (cx, cy + A - self.length), (cx, cy + A + self.length),self.crosshair_color, self.thickness)
            cv2.circle(annotated, center=(cx, cy + A), radius=self.radius_crosshair, color=self.crosshair_color, thickness=self.thickness)

            cv2.imshow('img progess by pop - cam2', annotated)

            self._last_processed_idx2 = self._frame2_idx

            if cv2.waitKey(1) == ord('q'):
                self.running = False
                break

        cv2.destroyWindow('img progess by pop - cam2')
        
#------------------------------------------------------------------------------------------------------------------------------

# --- send joystick ---
def send_joystick():
    global running
    while running:
        pygame.event.pump()
        j = joysticks[0]

        left_right = j.get_axis(0)
        forward_backward = j.get_axis(1)
        torsion = j.get_axis(2)
        sensitivity_raw = j.get_axis(3)

        button_1 = j.get_button(0)
        button_2 = j.get_button(1)
        button_3 = j.get_button(2)
        button_4 = j.get_button(3)

        sensitivity = 1 - ((sensitivity_raw + 1) / 2)  # Normalize sensitivity
        yaw_rotate = sensitivity * ((left_right * 90) + (torsion * 10))
        pitch_rotate = (sensitivity * (forward_backward * 100)) * -1

        pump_toggle = float(button_4)
        trigger = float(button_1)
        lever_pull = float(button_3)
        forward_assist = float(button_2)

        # debug print
        print(f"yaw:{yaw_rotate:.2f} pitch:{pitch_rotate:.2f} trig:{trigger:.0f} pump:{pump_toggle:.0f}    ", end="\r", flush=True)

        try:
            data = struct.pack('ffffff', float(yaw_rotate), float(pitch_rotate),
                               float(trigger), float(lever_pull),
                               float(pump_toggle), float(forward_assist))
            pc_socket.sendall(data)
            
        except Exception as e:
            print("Joystick send error:", e)
            running = False
            break

        time.sleep(0.002)

# --- instantiate and start threads (order matters) ---
processor = img_processing(pc_socket, pc_socket_1, pc_socket_2, width=width, height=height)

# Start receivers first
t_recv1 = threading.Thread(target=processor.receive_frame_1, daemon=True)
t_recv2 = threading.Thread(target=processor.receive_frame_2, daemon=True)
t_recv1.start()
t_recv2.start()

# Then start processing/display threads
t_proc1 = threading.Thread(target=processor.img_on_img_progress_and_show_1, daemon=True)
t_proc2 = threading.Thread(target=processor.img_on_img_progress_and_show_2, daemon=True)
t_proc1.start()
t_proc2.start()

# Start joystick sender
t_js = threading.Thread(target=send_joystick, daemon=True)
t_js.start()

# main loop (keeps pygame event loop alive)
try:
    while running:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        time.sleep(0.01)
finally:
    running = False
    t_recv1.join(timeout=1.0)
    t_recv2.join(timeout=1.0)
    t_proc1.join(timeout=1.0)
    t_proc2.join(timeout=1.0)
    t_js.join(timeout=1.0)
    pc_socket.close()
    pc_socket_1.close()
    pc_socket_2.close()
    pygame.quit()
    sys.exit(0)
