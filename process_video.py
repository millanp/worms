import numpy as np
import cv2

VIDEO_URL = "/home/millan/wsp/worms/reversed.avi"
# VIDEO_URL = "test.mkv"

def find_and_draw_circles(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2, 10, minRadius=20, maxRadius=30)
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
    
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            print(r)
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    return


def main():
    cap = cv2.VideoCapture(VIDEO_URL)

    previous_frame = None

    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()

        if not ret:
            break

        # Our operations on the frame come here
        find_and_draw_circles(frame)

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # previous_frame = gray

        if cv2.waitKey(500) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()