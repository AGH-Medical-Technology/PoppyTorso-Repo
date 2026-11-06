from picamera2 import Picamera2

picam2 = Picamera2()
picam2.start()
print("Camera started successfully!")
picam2.stop()
