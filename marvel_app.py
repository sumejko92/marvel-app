import cv2
import numpy as np
import imutils
import Tkinter as tki
from PIL import Image
from PIL import ImageTk
import threading
import time

hlow = 0
slow = 0
vlow = 0
hup = 0
sup = 0
vup = 0
i = 0
panel = 0
paint = 'None'


# Function for edge detection
def auto_canny(image):
    sigma = 0.33
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

# Capture the webcam video
cap = cv2.VideoCapture(0)
# kernel = np.ones((3,3),np.uint8)


def video_loop(value):
    global panel

    choice = value
    print choice
    var = 0
    kernel = np.ones((3, 3), np.uint8)

    try:

        while 1:
            # Capture frame-by-frame
            ret, frame = cap.read()
            # resize frame
            frame = imutils.resize(frame, width=400)
            # convert to hsv
            smoothed = cv2.GaussianBlur(frame, (3, 3), 0)
            hsv = cv2.cvtColor(smoothed, cv2.COLOR_BGR2HSV)
            backup = hsv
            #hsv = cv2.GaussianBlur(hsv, (5, 5), 0)

            # define range of skin color in HSV
            lower_red = np.array([int(hlow), int(slow), int(vlow)])
            upper_red = np.array([int(hup), int(sup), int(vup)])

            # previous fixed values
            # lower_red = np.array([8, 48, 80])
            # upper_red = np.array([19, 255, 255])

            # blue green and red color in bgr
            mid1 = np.array([0, 255, 0])
            mid2 = np.array([255, 0, 0])
            mid3 = np.array([0, 0, 255])

            # Threshold the HSV image to get only skin colors
            # inRange returns a binary image where pixels between the limits are shown as white pixels
            mask = cv2.inRange(hsv, lower_red, upper_red)

            # Closing for filling small noise holes
            mask = cv2.dilate(mask, kernel, iterations=2)
            mask = cv2.erode(mask, kernel, iterations=2)


            # Bitwise-AND mask and original image colored
            res = cv2.bitwise_and(frame, frame, mask=mask)
            green = cv2.bitwise_and(frame, mid1, mask=mask)
            blue = cv2.bitwise_and(frame, mid2, mask=mask)
            red = cv2.bitwise_and(frame, mid3, mask=mask)

            if int(i) == 1:
                cv2.destroyAllWindows()
                break

            if choice == 'Camera':
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if panel is None:
                    panel = tki.Label(image=image)
                    panel.image = image
                    panel.grid(row=3, column=5)

                # otherwise, simply update the panel
                else:
                    panel.configure(image=image)
                    panel.image = image

            elif choice == 'Skin':
                image = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if panel is None:
                    panel = tki.Label(image=image)
                    panel.image = image
                    panel.grid(row=3, column=5)

                # otherwise, simply update the panel
                else:
                    panel.configure(image=image)
                    panel.image = image

            elif choice == 'Mask':
                image = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if panel is None:
                    panel = tki.Label(image=image)
                    panel.image = image
                    panel.grid(row=3, column=5)

                # otherwise, simply update the panel
                else:
                    panel.configure(image=image)
                    panel.image = image

            elif choice == 'Green skin':
                backup[mask > 0, 0] = 55
                image = cv2.cvtColor(backup, cv2.COLOR_HSV2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if panel is None:
                    panel = tki.Label(image=image)
                    panel.image = image
                    panel.grid(row=3, column=5)

                # otherwise, simply update the panel
                else:
                    panel.configure(image=image)
                    panel.image = image

            elif choice == 'Green mask':
                image = cv2.cvtColor(green, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if panel is None:
                    panel = tki.Label(image=image)
                    panel.image = image
                    panel.grid(row=3, column=5)

                # otherwise, simply update the panel
                else:
                    panel.configure(image=image)
                    panel.image = image

            elif choice == 'Blue mask':
                image = cv2.cvtColor(blue, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if panel is None:
                    panel = tki.Label(image=image)
                    panel.image = image
                    panel.grid(row=3, column=5)

                # otherwise, simply update the panel
                else:
                    panel.configure(image=image)
                    panel.image = image

            elif choice == 'Red mask':
                image = cv2.cvtColor(red, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if panel is None:
                    panel = tki.Label(image=image)
                    panel.image = image
                    panel.grid(row=3, column=5)

                # otherwise, simply update the panel
                else:
                    panel.configure(image=image)
                    panel.image = image

            elif choice == 'Edge1':
                edg1 = auto_canny(frame)

                edg1_bgr = cv2.cvtColor(edg1, cv2.COLOR_GRAY2BGR)
                maska = edg1

                if paint == 'None':
                    var = np.array([255, 255, 255])
                elif paint == 'Blue':
                    var = mid2
                elif paint == 'Green':
                    var = mid1
                elif paint == 'Red':
                    var = mid3

                # Colors white edges in green
                color_edge = cv2.bitwise_and(edg1_bgr, var, mask=maska)

                image = cv2.cvtColor(color_edge, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if panel is None:
                    panel = tki.Label(image=image)
                    panel.image = image
                    panel.grid(row=3, column=5)

                # otherwise, simply update the panel
                else:
                    panel.configure(image=image)
                    panel.image = image

            elif choice == 'Edge2':
                edg2 = cv2.Canny(frame, 50, 100)

                edg2_bgr = cv2.cvtColor(edg2, cv2.COLOR_GRAY2BGR)
                maska = edg2

                if paint == 'None':
                    var = np.array([255, 255, 255])
                elif paint == 'Blue':
                    var = mid2
                elif paint == 'Green':
                    var = mid1
                elif paint == 'Red':
                    var = mid3

                color_edge = cv2.bitwise_and(edg2_bgr, var, mask=maska)

                image = cv2.cvtColor(color_edge, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if panel is None:
                    panel = tki.Label(image=image)
                    panel.image = image
                    panel.grid(row=3, column=5)

                # otherwise, simply update the panel
                else:
                    panel.configure(image=image)
                    panel.image = image

            elif choice == 'YCrCb':
                # Cr > 150 && Cr < 200 && Cb > 100 && Cb < 150.
                # old
                # min_YCrCb = np.array([0, 133, 77], np.uint8)
                # max_YCrCb = np.array([255, 173, 127], np.uint8)

                min_YCrCb = np.array([0,  140, 80], np.uint8)
                max_YCrCb = np.array([255, 180, 131], np.uint8)

                # BGR backup1
                backup1 = frame

                # BGR to YCrCb , also works with BGR2YCR_CB
                imageYCrCb = cv2.cvtColor(backup1, cv2.COLOR_BGR2YCrCb)

                # Find region with skin tone in YCrCb image
                skinregion = cv2.inRange(imageYCrCb, min_YCrCb, max_YCrCb)
                im = cv2.bitwise_and(backup1, backup1, mask=skinregion)

                # preparing for gui display
                image = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if panel is None:
                    panel = tki.Label(image=image)
                    panel.image = image
                    panel.grid(row=3, column=5)

                # otherwise, simply update the panel
                else:
                    panel.configure(image=image)
                    panel.image = image

            elif choice == 'YCrCb Green':
                # Cr > 150 && Cr < 200 && Cb > 100 && Cb < 150.
                # old
                # min_YCrCb = np.array([0, 133, 77], np.uint8)
                # max_YCrCb = np.array([255, 173, 127], np.uint8)

                min_YCrCb = np.array([0,  140, 80], np.uint8)
                max_YCrCb = np.array([255, 180, 131], np.uint8)

                #BGR backup1
                backup1 = frame

                # BGR to YCrCb , also works with BGR2YCR_CB
                imageYCrCb = cv2.cvtColor(backup1, cv2.COLOR_BGR2YCrCb)

                # Find region with skin tone in YCrCb image
                skinregion_mask = cv2.inRange(imageYCrCb, min_YCrCb, max_YCrCb)

                # Color skin regions in green
                imageYCrCb[skinregion_mask > 0, 1] = 100

                # preparing for gui display
                image = cv2.cvtColor(imageYCrCb, cv2.COLOR_YCrCb2RGB)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)

                if panel is None:
                    panel = tki.Label(image=image)
                    panel.image = image
                    panel.grid(row=3, column=5)

                # otherwise, simply update the panel
                else:
                    panel.configure(image=image)
                    panel.image = image

            if cv2.waitKey(1) == 27 or int(i) == 1:
                cv2.destroyAllWindows()
                break

    except RuntimeError, e:
        print("[INFO] caught a RuntimeError")


# Function for changing video and threading
def change(value):
    global i
    # i is used for closing previous thread
    i = 1
    time.sleep(0.1)
    i = 0
    a = var1.get()
    t1 = threading.Thread(target=video_loop, args=(a,))
    t1.start()

# Function for changing edge color
def change_color(value):
    global paint
    paint = var2.get()

# Function for closing gui
def close_window():
    global i
    i = 1
    root.destroy()
    # root.quit


# Function for setting default values
def reset():

    s1.set(0)
    s2.set(48)
    s3.set(80)

    s4.set(19)
    s5.set(255)
    s6.set(255)


# Slider values
def h_low(hl1):
    global hlow
    hlow = hl1


def s_low(sl1):
    global slow
    slow = sl1


def v_low(vl1):
    global vlow
    vlow = vl1


def h_up(hu1):
    global hup
    hup = hu1


def s_up(su1):
    global sup
    sup = su1


def v_up(vu1):
    global vup
    vup = vu1


frame = None
root = tki.Tk()
panel = None

hl = tki.IntVar()
sl = tki.IntVar()
vl = tki.IntVar()

hu = tki.IntVar()
su = tki.IntVar()
vu = tki.IntVar()

# canvas = Canvas(root, width = 600, height = 400)
# canvas.grid(row=3,column=3)
root.geometry("1000x550")

# Create blank image area where the video will be stored
blank_image = np.ones((300, 400, 3), np.uint8)*255
blank_image = Image.fromarray(blank_image)
blank_image = ImageTk.PhotoImage(blank_image)

if panel is None:
    panel = tki.Label(image=blank_image)
    panel.image = blank_image
    panel.grid(row=3, column=5)

# otherwise, simply update the panel
else:
    panel.configure(image=blank_image)
    panel.image = blank_image

# Drop list 1
var1 = tki.StringVar(root)
var1.set("Camera")
tki.Label(root, text="Choose a video").grid(row=1, column=1)
drop = tki.OptionMenu(root, var1, 'Camera', 'Skin', 'Mask', 'Green skin', 'Green mask',
                      'Blue mask', 'Red mask', 'Edge1', 'Edge2', 'YCrCb', 'YCrCb Green', command=change)
drop.grid(row=2, column=1)
# drop.pack(side="left", fill="none", expand="no", padx="5", pady="5")

# Drop list 2
var2 = tki.StringVar(root)
var2.set("None")
tki.Label(root, text="Edge Color").grid(row=1, column=10)
drop_edge = tki.OptionMenu(root, var2, 'None', 'Blue', 'Green', 'Red', command=change_color)
drop_edge.grid(row=2, column=10)


# Button for closing gui
btn1 = tki.Button(root, text="Close window", command=close_window)
btn1.grid(row=20, column=1)

# Button to reset to default values
btn2 = tki.Button(root, text="Reset default values", command=reset)
btn2.grid(row=20, column=5)

# slider lower H value
tki.Label(root, text=" Lower H value").grid(row=15, column=4)
s1 = tki.Scale(root, from_=0, to=255, tickinterval=51, length=200, resolution=1,
               orient=tki.HORIZONTAL, command=h_low, variable=hl)
s1.set(0)
s1.grid(row=16, column=4)
# slider lower S value
tki.Label(root, text=" Lower S value").grid(row=15, column=5)
s2 = tki.Scale(root, from_=0, to=255, tickinterval=51, length=200, resolution=1,
               orient=tki.HORIZONTAL, command=s_low, variable=sl)
s2.set(48)
s2.grid(row=16, column=5)
# slider lower V value
tki.Label(root, text=" Lower V value").grid(row=15, column=6)
s3 = tki.Scale(root, from_=0, to=255, tickinterval=51, length=200, resolution=1,
               orient=tki.HORIZONTAL, command=v_low, variable=vl)
s3.set(80)
s3.grid(row=16, column=6)

# slider upper H value
tki.Label(root, text=" Upper H value").grid(row=17, column=4)
s4 = tki.Scale(root, from_=0, to=255, tickinterval=51, length=200, resolution=1,
               orient=tki.HORIZONTAL, command=h_up, variable=hu)
s4.set(19)
s4.grid(row=18, column=4)
# slider upper S value
tki.Label(root, text=" Upper S value").grid(row=17, column=5)
s5 = tki.Scale(root, from_=0, to=255, tickinterval=51, length=200, resolution=1,
               orient=tki.HORIZONTAL, command=s_up, variable=su)
s5.set(255)
s5.grid(row=18, column=5)
# slider upper V value
tki.Label(root, text=" Upper V value").grid(row=17, column=6)
s6 = tki.Scale(root, from_=0, to=255, tickinterval=51, length=200, resolution=1,
               orient=tki.HORIZONTAL, command=v_up, variable=vu)
s6.set(255)
s6.grid(row=18, column=6)


root.mainloop()

cv2.destroyAllWindows()
cap.release()
