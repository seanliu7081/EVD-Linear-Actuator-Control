import cv2
import dlib
import numpy as np
import pyrealsense2
import math
from realsense_depth import DepthCamera


def calculate_vertical_displacement(distance_start, distance_end, pixel_displacement):

    vertical_displacement = 2 * (0.55*((distance_end+distance_start)/2))*(pixel_displacement/720)
    return vertical_displacement

def track_head_movement(model_path):
    # output_video_path = 'video.avi'
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(model_path)

    # Initialize DepthCamera
    dc = DepthCamera()

    
    initial_position = None
    end_position = None
    initial_distance = None
    end_distance = None
    # recording = False  # Flag to control recording

    # Define the codec and create VideoWriter object outside the loop
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = None  # Initialize out to None

    while True:
        ret, depth_frame, color_frame = dc.get_frame()
        if not ret:
            print("Failed to grab frame")
            break

        gray = cv2.cvtColor(color_frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            try:
                landmarks = predictor(gray, face)
                ear_point = (landmarks.part(0).x, landmarks.part(0).y)  # Right ear
                current_distance = depth_frame[ear_point[1], ear_point[0]] * 0.1  # Convert mm to cm
                
                # Visual feedback
                cv2.circle(color_frame, ear_point, 4, (255, 0, 0), -1)
                cv2.putText(color_frame, f"{current_distance:.1f} cm", (ear_point[0], ear_point[1] - 20),
                            cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
            except Exception as e:
                print(f"Error detecting landmarks: {e}")

        cv2.imshow("Color Frame", color_frame)

        # if recording:
        #     out.write(color_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            initial_position = ear_point
            initial_distance = current_distance
            print("Start position and distance set.")
            print(initial_distance)
            # out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (640, 480))
            # recording = True
            # fourcc = cv2.VideoWriter_fourcc(*'XVID')
            # out = cv2.VideoWriter(output_video_path, fourcc, 20.0, (640, 480))
        elif key == ord('e'):
            end_position = ear_point
            end_distance = current_distance
            print("End position and distance set.")
            print(end_distance)
            # out.write(color_frame)
            # recording = False
            break
        elif key == ord('q'):
            print("Quitting without setting end position.")
            break

    dc.release()
    cv2.destroyAllWindows()
    # out.release()
    # if out:
    #     out.release()

    if initial_position and end_position:
        vertical_movement_pixels = end_position[1] - initial_position[1]
        real_world_vertical_movement = calculate_vertical_displacement(initial_distance, end_distance, vertical_movement_pixels)
        # print(initial_distance, end_distance, vertical_movement_pixels)
        print(f"Vertical movement: {vertical_movement_pixels} pixels, {real_world_vertical_movement:.1f} cm")
        # return vertical_movement_pixels, real_world_vertical_movement
        return real_world_vertical_movement
    else:
        print("Start and/or end position not set.")
        return None, None
