import serial
import time
# from headMotionTracking import track_head_movement
from track_with_depthV3 import track_head_movement
# Establish serial connection
arduino = serial.Serial('COM7', 115200)
time.sleep(2)  # Give time for the connection to establish
model_path = 'shape_predictor_68_face_landmarks.dat'

try:
    while True:
        inputNum = track_head_movement(model_path)
        print(f"get input{inputNum}")
        scaledInput = round((-inputNum), 2) # Scale and convert to string
        print(f"scaled {scaledInput}")
        inputDis = str(scaledInput)
        print(f"input distance {inputDis}")

        # arduino.write(scaledInput.encode())  # Send the scaled distance command
        arduino.write(inputDis.encode())

        # Wait for the Arduino to acknowledge completion
        while arduino.in_waiting == 0:
            pass  # Wait for data to be received

        response = arduino.readline().decode().strip()  # Read Arduino's response
        print(f"Arduino response: {response}")
except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    arduino.close()  # Ensure the serial connection is closed on exit
