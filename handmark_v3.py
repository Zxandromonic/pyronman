import cv2
import mediapipe as mp
import pyautogui



WIDTH = 1920
HEIGHT = 1080


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

pyautogui.PAUSE = 0.02

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

with mp_hands.Hands(
  model_complexity=0,
  max_num_hands=1,
  min_detection_confidence=.5,
  min_tracking_confidence=.5,) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      break

    # To improve performance, optionally mark the image as not writeable to pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
          image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style()
          )
        
        current_mouse_position = pyautogui.position()

        index_x = WIDTH-(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * WIDTH)
        index_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * HEIGHT

        thumb_x = WIDTH-(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * WIDTH)
        thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * HEIGHT

        pinky_x = WIDTH-(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * WIDTH)
        pinky_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * HEIGHT

        middle_x = WIDTH-(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * WIDTH)
        middle_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * HEIGHT

        ring_x = WIDTH-(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * WIDTH)
        ring_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * HEIGHT

        pyautogui.moveTo(index_x, index_y)
        print(f"coords: {index_x}, {index_y}")

        if abs(middle_x - thumb_x) <= 50 and abs(middle_y - thumb_y) <= 50:
          pyautogui.click(index_x, index_y)
          print("lc")

        if abs(pinky_x - thumb_x) <= 80 and abs(pinky_y - thumb_y) <= 80:
          pyautogui.rightClick(index_x, index_y)
          print("rc")


    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
