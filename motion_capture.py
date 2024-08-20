import cv2
import dlib
import csv

def track_head_movement(model_path):
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(model_path)

    cap = cv2.VideoCapture(0)

    initial_position = None
    displacements = []  # List to store displacements

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        for face in faces:
            try:
                landmarks = predictor(gray, face)
                ear_point = (landmarks.part(0).x, landmarks.part(0).y)
                cv2.circle(frame, ear_point, 4, (255, 0, 0), -1)
                current_position = ear_point
            except:
                current_position = (face.left(), face.top())
                cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 2)

        if initial_position is not None and current_position is not None:
            displacement = (current_position[0] - initial_position[0], current_position[1] - initial_position[1])
            displacements.append(displacement)

        cv2.imshow("Frame", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):
            initial_position = current_position
            displacements = []  # Reset displacements list
            print("Start position set.")
        elif key == ord('e') and initial_position is not None:
            print("End position set. Saving displacements to CSV file.")
            break
        elif key == ord('q'):
            print("Quitting without saving to CSV.")
            break

    cap.release()
    cv2.destroyAllWindows()

    if displacements:
        # Writing to CSV file
        with open('head_movements.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Horizontal Displacement", "Vertical Displacement"])
            writer.writerows(displacements)
        print(f"Displacements recorded and saved: {len(displacements)}")
    else:
        print("Start and/or end position not set or no movement detected.")

track_head_movement('shape_predictor_68_face_landmarks.dat')
