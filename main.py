import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector

video_capture = cv2.VideoCapture(0)

face_detector = FaceMeshDetector(maxFaces=1)

while True:
    success, frame = video_capture.read()  

    frame, face_mesh = face_detector.findFaceMesh(frame, draw=False)

    if face_mesh:
        face_points = face_mesh[0]

        # Extract key points for measuring the distance (left and right eye balls)
        left_eye_point = face_points[145]
        right_eye_point = face_points[374]

         # Measure the pixel distance between the points
        pixel_distance, _ = face_detector.findDistance(left_eye_point, right_eye_point)

        # Real-world width of the object (distance between the eyes in cm)
        real_world_width = 6.3

        # Comment out the below lines to calculate the focal length
        # focal_length = (pixel_distance * distance_to_face)/real_world_width
        # print(focal_length)

        # Focal length (previously calculated)
        focal_length = 530

        # Calculate the approximate distance from the camera to the face
        distance_to_face = (real_world_width * focal_length) / pixel_distance

        if distance_to_face < 50:
            cvzone.putTextRect(frame, f'Distance: {int(distance_to_face)} cm', 
                            (face_points[10][0] - 75, face_points[10][1] - 50), scale=2, colorR=(0, 0, 255), 
                            font=cv2.FONT_HERSHEY_PLAIN)
        elif 50 <= distance_to_face <= 76:
            # Display the calculated distance on the frame
            cvzone.putTextRect(frame, f'Distance: {int(distance_to_face)} cm', 
                            (face_points[10][0] - 75, face_points[10][1] - 50), scale=2, colorR=(0, 255, 0), 
                            font=cv2.FONT_HERSHEY_PLAIN)
        else:
            cvzone.putTextRect(frame, f'Distance: {int(distance_to_face)} cm', 
                            (face_points[10][0] - 75, face_points[10][1] - 50), scale=2, colorR=(255, 0, 0), 
                            font=cv2.FONT_HERSHEY_PLAIN)

            # Show the processed video frame
        cv2.imshow("Face Distance Measurement", frame)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the video capture and close any OpenCV windows
video_capture.release()
cv2.destroyAllWindows()