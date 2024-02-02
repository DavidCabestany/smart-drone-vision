import cv2

# Capture the video stream
stream_url = 'rtmp://192.168.10.114/live'
cap = cv2.VideoCapture(stream_url)

while True:
    ret, frame = cap.read()
    if ret:
        # Process frame
        # ...

        # Display the frame
        cv2.imshow('Drone Stream', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

cap.release()
cv2.destroyAllWindows()
