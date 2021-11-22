import cv2
import numpy as np

cap = cv2.VideoCapture('./videos/demo.mp4')

min_area = 0.0005
max_area = 0.95
mask_color = (0.0,0.0,0.0)

while cap.isOpened():
    ret, frame = cap.read()

    frame_count = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

    if ret:
        map = frame[675:1050, 25:500]

        # map_blur = cv2.medianBlur(map, 3)

        gray = cv2.cvtColor(map, cv2.COLOR_BGR2GRAY)

        blur = cv2.bilateralFilter(gray, 9, 75, 75)


        # ret1,thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        # wide = cv2.Canny(blur, 10, 200, L2gradient=True)
        mid = cv2.Canny(blur, 30, 100, L2gradient=True)
        # tight = cv2.Canny(blur, 240, 250, L2gradient=True)

        # canny = cv2.Canny(blur, 50, 130, apertureSize=3, L2gradient=True)

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        morph = cv2.morphologyEx(mid, cv2.MORPH_GRADIENT, kernel)

        # cv2.imshow("wcanny", wide)
        cv2.imshow("mcanny", morph)
        # cv2.imshow("tcanny", tight)
        #
        # lines = cv2.HoughLinesP(canny, 1, np.pi/180, 15, 30, 10)

        # print(lines[0][0])

        # lines = cv2.HoughLines(canny, 1, np.pi/180, 200)
        # for x in range(0, len(lines)):
        #     for x1,y1,x2,y2 in lines[x]:
        #         cv2.line(map,(x1,y1),(x2,y2),(0,255,0),2)

        # cv2.imshow("hough", map)

        # laplacian = cv2.Laplacian(thresh, cv2.CV_8UC1)

        # cv2.imshow("lap", laplacian)
        # filter = laplacian/laplacian.max()

        # print((laplacian/laplacian.max()).dtype())

        # abs_lap = cv2.convertScaleAbs(laplacian, alpha=255/laplacian.max(), beta=1)

        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # opening = cv2.morphologyEx(abs_lap, cv2.MORPH_OPEN, kernel)

        # thresh = cv2.adaptiveThreshold(opening, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 151, 1)

        # thresh = cv2.threshold(opening, 250, 255, cv2.THRESH_OTSU)[1]

        # blur = cv2.medianBlur(thresh, 3)

        # lines_filter = cv2.HoughLinesP(abs_lap, 1, np.pi/180, 15, 30, 10)
        #
        # for x in range(0, len(lines_filter)):
        #     for x1,y1,x2,y2 in lines_filter[x]:
        #         cv2.line(map,(x1,y1),(x2,y2),(0,255,0),2)
        # sobely = cv2.Sobel(abs_lap, cv2.CV_8UC1, 0, 1, ksize=31)

        contours, hierarchy = cv2.findContours(image=morph, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)

        # hull = []
        # for contour in contours:
        #     hull.append(cv2.convexHull(contour, False))
        #
        # for i in range(len(contours)):
        #     color_contours = (0, 255, 0)
        #     color = (255, 0, 0)

        if len(contours) > 0:
            cv2.drawContours(map, contours, -1, (0, 255, 0), 5)
            c = max(contours, key=cv2.contourArea)
            x,y,w,h = cv2.boundingRect(c)

            cv2.rectangle(map, (x,y), (x+w, y+h), (0, 0, 255), 8)
            # cv2.drawContours(map, hull, i, color, 1, 8)

        # find smallest location contour and biggest location contour to draw rectangle around

        # cv2.drawContours(image=map, contours=contours, contourIdx=-1, color=(0,255,0), thickness=2, lineType=cv2.FILLED)

        # cv2.imshow("lap", abs_lap)
        # cv2.imshow("open", opening)
        # cv2.imshow("thresh", thresh)
        cv2.imshow("map", map)



        # edges = cv2.Canny(gray, 100, 110)
        #
        # edges = cv2.dilate(edges, None)
        # edges = cv2.erode(edges, None)

        # contours, hierarchy = cv2.findContours(image=edges, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_SIMPLE)
        #
        # cv2.drawContours(image=edges, contours=contours, contourIdx=-1, color=(0,0,100), thickness=1, lineType=cv2.LINE_AA)
        #
        # contours, hierarchy = cv2.findContours(image=edges, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
        #
        # cv2.drawContours(image=edges, contours=contours, contourIdx=-1, color=(100,100,0), thickness=2, lineType=cv2.FILLED)

        # contour_info = [(c, cv2.contourArea(c),) for c in cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]]
        #
        # image_area = map.shape[0] * map.shape[1]
        #
        # max_area = max_area * image_area
        # min_area = min_area * image_area
        #
        # mask = np.zeros(edges.shape, dtype=np.uint8)
        #
        # for contour in contour_info:
        #     if contour[1] > min_area and contour[1] < max_area:
        #         # Add contour to mask
        #         mask = cv2.fillConvexPoly(mask, contour[0], (255))
        #
        #         # mask = cv2.dilate(mask, None, iterations=10)
        #         # mask = cv2.erode(mask, None, iterations=10)
        #
        # mask_stack = np.dstack([mask]*3)
        #
        # mask_stack = mask_stack.astype('float32') / 255.0
        # frame = map.astype('float32') / 255.0
        #
        # masked = (mask_stack * frame) + ((1-mask_stack) * mask_color)
        # masked = (masked * 255).astype('uint8')
        # cv2.imshow("mask", edges)










        # for contour in contours:
        #
        #     approx = cv2.approxPolyDP(contour, 0.1 * cv2.arcLength(contour, True), True)
        #
        #     hull = cv2.convexHull(approx)
        #
        #     x,y,w,h = cv2.boundingRect(hull)
        #     cv2.rectangle(map,(x,y),(x+w,y+h),(255,0,0),3)
        #
        #     if len(approx) == 4:
        #         cv2.drawContours(map, [approx], 0, (0, 0, 255), 5)
        #
        #         M = cv2.moments(contour)
        #         if M['m00'] != 0.0:
        #             x = int(M['m10']/M['m00'])
        #             y = int(M['m01']/M['m00'])
        #
        #
        # # cv2.imshow("thresh", thresh)
        # cv2.imshow("map", m)

    # text = pytesseract.image_to_string(equip, lang="eng", config="--psm 6 --oem 1").split('\n')[0]
    #
    # print(text)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
