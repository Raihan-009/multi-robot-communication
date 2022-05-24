import cv2


cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if ret:
        cv2.imshow("Streaming", frame)
    else:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
cam.release()