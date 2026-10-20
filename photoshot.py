import cv2
import time

cap = cv2.VideoCapture(0)

ret1, frame1 = cap.read()

cv2.imwrite('photo_'+str(time.time())+'.png', frame1)

cap.release()
cv2.destroyAllWindows()

