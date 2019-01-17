import numpy as np
import cv2

VIDEO_URL = "/home/millan/wsp/worms/reversed.avi"
MIN_AREA = 200
# VIDEO_URL = "test.mkv"

def find_and_draw_circles(frame):
    gray = frame # cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2, 10, minRadius=20, maxRadius=30)
    if circles is not None:
        # convert the (x, y) coordinates and radius of the circles to integers
        circles = np.round(circles[0, :]).astype("int")
    
        # loop over the (x, y) coordinates and radius of the circles
        for (x, y, r) in circles:
            # draw the circle in the output image, then draw a rectangle
            # corresponding to the center of the circle
            cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            cv2.rectangle(frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    return circles

def get_rectangles(frame, circles):
    out = []
    for (x, y, r) in circles:
        out.append({"frame": frame[y-r:y+r, x-r:x+r], "position": [x, y, r]})
    return out


def main():
    cap = cv2.VideoCapture(VIDEO_URL)

    previous_frame = None

    ret, first_frame = cap.read()
    first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2GRAY)
    circles = find_and_draw_circles(first_frame)
    rectangles = get_rectangles(first_frame, circles)
    cv2.imshow("Rectangle", rectangles[0]["frame"])

    while cap.isOpened():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Our operations on the frame come here
        # find_and_draw_circles(frame)

        for (x, y, r) in circles:
            cv2.rectangle(frame, (x-r, y-r), (x+r, y+r), (0, 255, 0), 2)

        new_rectangles = get_rectangles(frame, circles)

        for i, new_rect in enumerate(new_rectangles):
            # compute the absolute difference between the current frame and
            # first frame

            frameDelta = cv2.absdiff(rectangles[i]["frame"], new_rect["frame"])
            
            thresh = cv2.threshold(frameDelta, 150, 255, cv2.THRESH_BINARY)[1]
            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image
            # thresh = cv2.dilate(thresh, None, iterations=2)
            contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) < MIN_AREA:
                    continue
                (x, y, w, h) = cv2.boundingRect(contour)
                rectangles[i]["position"][2] *= 2
                cv2.rectangle(frame, (rectangles[i]["position"][0] - rectangles[i]["position"][2], rectangles[i]["position"][1] - rectangles[i]["position"][2]), (rectangles[i]["position"][0] + rectangles[i]["position"][2], rectangles[i]["position"][1] + rectangles[i]["position"][2]), (0, 255, 0), 12)
                
                # print('movement')

        # rectangles = new_rectangles

        # Display the resulting frame
        cv2.imshow('frame', frame)

        # previous_frame = gray

        if cv2.waitKey(50) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__=="__main__":
    main()