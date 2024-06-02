import cv2
import dlib
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

# dlib의 얼굴 탐지기와 랜드마크 예측기 초기화
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

# Tkinter 윈도우 설정
root = Tk()
root.title("Face Editor")
root.geometry("1000x800")

# 글로벌 변수 초기화
img = None
tk_img = None
start_x = start_y = 0
landmarks = None
dragging = False
applying_mosaic = False
mosaic_start_x = mosaic_start_y = mosaic_end_x = mosaic_end_y = 0

def load_image(file_path=None):
    global img, tk_img, canvas, landmarks
    if file_path is None:
        file_path = filedialog.askopenfilename()
    if not file_path:
        return
    img = cv2.imread(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    if len(faces) == 0:
        print("No faces detected.")
        return
    landmarks = predictor(gray, faces[0])
    for i in range(68):
        cv2.circle(img, (landmarks.part(i).x, landmarks.part(i).y), 1, (255, 0, 0), -1)  # 빨간색 점, 크기 1
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = img.resize((800, 600), Image.LANCZOS)
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor=NW, image=tk_img)
    canvas.config(scrollregion=canvas.bbox(ALL))

def liquify_image(x1, y1, x2, y2):
    global img, tk_img, canvas
    if img is None:
        return

    np_img = np.array(img)
    grid_x, grid_y = np.meshgrid(np.arange(np_img.shape[1]), np.arange(np_img.shape[0]))

    d = np.sqrt((grid_x - x1)**2 + (grid_y - y1)**2)
    sigma = 30
    alpha = 0.5

    displacement_x = alpha * np.exp(-(d**2) / (2 * sigma**2)) * (x2 - x1)
    displacement_y = alpha * np.exp(-(d**2) / (2 * sigma**2)) * (y2 - y1)

    map_x = (grid_x + displacement_x).astype(np.float32)
    map_y = (grid_y + displacement_y).astype(np.float32)

    warped = cv2.remap(np_img, map_x, map_y, interpolation=cv2.INTER_LINEAR)
    img = Image.fromarray(warped)
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor=NW, image=tk_img)
    canvas.config(scrollregion=canvas.bbox(ALL))

def apply_filter(filter_name):
    global img, tk_img, canvas
    if img is None:
        return
    np_img = np.array(img)
    if filter_name == "gray":
        np_img = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
        np_img = cv2.cvtColor(np_img, cv2.COLOR_GRAY2RGB)
    elif filter_name == "blur":
        np_img = cv2.GaussianBlur(np_img, (15, 15), 0)
    elif filter_name == "sharpen":
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        np_img = cv2.filter2D(np_img, -1, kernel)
    elif filter_name == "emboss":
        kernel = np.array([[0, -1, -1], [1, 0, -1], [1, 1, 0]])
        np_img = cv2.filter2D(np_img, -1, kernel)
    elif filter_name == "cartoon":
        gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(np_img, 9, 300, 300)
        np_img = cv2.bitwise_and(color, color, mask=edges)
    elif filter_name == "edges":
        np_img = cv2.Canny(np_img, 100, 200)
        np_img = cv2.cvtColor(np_img, cv2.COLOR_GRAY2RGB)
    elif filter_name == "sketch":
        gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
        inv_gray = 255 - gray
        blur = cv2.GaussianBlur(inv_gray, (21, 21), 0)
        np_img = cv2.divide(gray, 255 - blur, scale=256)
        np_img = cv2.cvtColor(np_img, cv2.COLOR_GRAY2RGB)

    img = Image.fromarray(np_img)
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor=NW, image=tk_img)
    canvas.config(scrollregion=canvas.bbox(ALL))

def apply_mosaic(start_x, start_y, end_x, end_y):
    global img, tk_img, canvas
    if img is None:
        return
    start_x = max(0, start_x)
    start_y = max(0, start_y)
    end_x = min(img.width, end_x)
    end_y = min(img.height, end_y)
    
    if start_x >= end_x or start_y >= end_y:
        return

    np_img = np.array(img)
    sub_img = np_img[start_y:end_y, start_x:end_x]
    if sub_img.size == 0:
        return

    sub_img = cv2.resize(sub_img, (10, 10), interpolation=cv2.INTER_LINEAR)
    sub_img = cv2.resize(sub_img, (end_x - start_x, end_y - start_y), interpolation=cv2.INTER_NEAREST)
    np_img[start_y:end_y, start_x:end_x] = sub_img
    img = Image.fromarray(np_img)
    tk_img = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, anchor=NW, image=tk_img)
    canvas.config(scrollregion=canvas.bbox(ALL))

def on_button_press(event):
    global start_x, start_y, dragging, applying_mosaic, mosaic_start_x, mosaic_start_y
    start_x, start_y = event.x, event.y
    dragging = True
    if applying_mosaic:
        mosaic_start_x, mosaic_start_y = event.x, event.y

def on_move_press(event):
    global start_x, start_y, dragging, applying_mosaic, mosaic_start_x, mosaic_start_y
    if dragging:
        end_x, end_y = event.x, event.y
        if applying_mosaic:
            mosaic_end_x, mosaic_end_y = end_x, end_y
            apply_mosaic(mosaic_start_x, mosaic_start_y, mosaic_end_x, mosaic_end_y)
        else:
            liquify_image(start_x, start_y, end_x, end_y)
        start_x, start_y = end_x, end_y  # Update start coordinates

def on_button_release(event):
    global dragging, applying_mosaic
    dragging = False
    if applying_mosaic:
        apply_mosaic(mosaic_start_x, mosaic_start_y, event.x, event.y)
        applying_mosaic = False

def start_mosaic():
    global applying_mosaic
    applying_mosaic = True

# Tkinter 위젯 설정
canvas = Canvas(root, cursor="cross")
canvas.pack(side="top", fill="both", expand=True)

btn_load = Button(root, text="Load Image", command=lambda: load_image())
btn_load.pack(side="left", padx=10, pady=10)

btn_gray = Button(root, text="Gray", command=lambda: apply_filter("gray"))
btn_gray.pack(side="left", padx=10, pady=10)

btn_blur = Button(root, text="Blur", command=lambda: apply_filter("blur"))
btn_blur.pack(side="left", padx=10, pady=10)

btn_sharpen = Button(root, text="Sharpen", command=lambda: apply_filter("sharpen"))
btn_sharpen.pack(side="left", padx=10, pady=10)

btn_emboss = Button(root, text="Emboss", command=lambda: apply_filter("emboss"))
btn_emboss.pack(side="left", padx=10, pady=10)

btn_cartoon = Button(root, text="Cartoon", command=lambda: apply_filter("cartoon"))
btn_cartoon.pack(side="left", padx=10, pady=10)

btn_edges = Button(root, text="Edges", command=lambda: apply_filter("edges"))
btn_edges.pack(side="left", padx=10, pady=10)

btn_sketch = Button(root, text="Sketch", command=lambda: apply_filter("sketch"))
btn_sketch.pack(side="left", padx=10, pady=10)

btn_mosaic = Button(root, text="Mosaic", command=start_mosaic)
btn_mosaic.pack(side="left", padx=10, pady=10)

canvas.bind("<ButtonPress-1>", on_button_press)
canvas.bind("<B1-Motion>", on_move_press)
canvas.bind("<ButtonRelease-1>", on_button_release)

root.mainloop()
