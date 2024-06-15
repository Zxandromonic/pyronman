import cv2
import mediapipe as mp
import pyautogui


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

TOL = 50
# For webcam input:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      continue

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
            mp_drawing_styles.get_default_hand_connections_style())
        image_width = 1440
        image_height = 900
        current_mouse_position = pyautogui.position()
        pyautogui.moveTo(1440-(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width),hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height)

        current_mouse_position = pyautogui.position()
        index_x = 1440-(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width)
        index_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height
        thumb_x = 1440-(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * image_width)
        thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * image_height
        pinky_x = 1440-(hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].x * image_width)
        pinky_y = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y * image_height
        middle_x = 1440-(hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * image_width)
        middle_y = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * image_height
        ring_x = 1440-(hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * image_width)
        ring_y = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * image_height

        if (pinky_x > thumb_x): 
          pyautogui.moveTo(index_x, index_y)
          print(f'coords: ({index_x}, {index_y})')

          if abs(middle_x - thumb_x) <= TOL and abs(middle_y - thumb_y) <= TOL:
            pyautogui.click(index_x, index_y)
            print("lc")

          if abs(ring_x - thumb_x) <= TOL and abs(ring_y - thumb_y) <= TOL:
            pyautogui.rightClick(index_x, index_y)
            print("rc")
        
#          if abs(ring_x - pinky_x) <= TOL-40 and abs(ring_y - ring_y) <= TOL-30:
#            pyautogui.scroll(4)
#            print("scu")
#
#          if abs(middle_x - ring_x) <= TOL-40 and abs(middle_y - middle_y) <= TOL-30:
#            pyautogui.scroll(-4)
#            print("scd")
          
          if abs(ring_x - pinky_x) <= TOL-20 and abs(ring_y -pinky_y) >=TOL+40 and abs(thumb_x - pinky_y) <TOL+500:
            pyautogui.scroll(-4)
            print("scd")    
          if abs(ring_x - pinky_x) <= TOL-20 and abs(ring_y -pinky_y) <=TOL+5 and abs(thumb_x - pinky_y) <TOL+500:
            pyautogui.scroll(4)
            print("scu")           

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow("Jarvis and Friday ain't got shit on us", cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
