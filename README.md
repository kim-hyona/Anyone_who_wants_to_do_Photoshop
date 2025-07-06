
# 🖼 Photoshop-Like Features Using OpenCV

(Filtering, Partial Mosaic, Face Retouching)

### ⚠️ Note: This project was developed as part of a university course assignment. Please consider it as a prototype or reference only — functionality is still limited.
We plan to enhance and expand the features in the future, with the goal of making them usable directly on the web!

🎨 Features
✅ Various Filters

Basic image filters applied using OpenCV
Comparison between original and filtered images

## 📸 Original Image vs. Filtered Versions
![image](https://github.com/kim-hyona/opencv/assets/148624727/0a9dc734-f7ae-4b5d-887b-67537267eba7)

## 🎭 Cartoon Effect

Converts images into a cartoon-like illustration using edge detection and bilateral filtering in OpenCV
Produces stylized output by simplifying colors and emphasizing edges
Fun and creative feature for stylizing portraits or landscapes

![image](https://github.com/kim-hyona/opencv/assets/148624727/6237e740-01de-499b-ac39-e2d1e6fed911)


## ✏️ Sketch Effect

Transforms an image into a pencil sketch-style rendering
Achieved using grayscale conversion, Gaussian blur, and color dodge blending in OpenCV
Gives a hand-drawn, black-and-white sketch appearance

![image](https://github.com/kim-hyona/opencv/assets/148624727/cced3ba7-2f5b-4e95-a9a2-0f68a0ca9c72)


## 🪨 Emboss Effect

Applies an emboss filter to create a raised, 3D texture effect on the image
Highlights edges and gives the image a carved or stamped appearance
Implemented using custom convolution kernels in OpenCV

![image](https://github.com/kim-hyona/opencv/assets/148624727/e2c41e38-a0a5-4f3f-a3f3-0d46347c982e)




------
## 🟫 Partial Mosaic (Censoring Specific Areas)

Applied mosaic (pixelation) to selected areas of an image using OpenCV
Useful for blurring faces, license plates, or sensitive content
Region selection done manually in this version
📸 Example: Face region blurred with mosaic effect


![image](https://github.com/kim-hyona/opencv/assets/148624727/d3c127c6-2d06-407c-9f95-6f10c206ca56)
![image](https://github.com/kim-hyona/opencv/assets/148624727/79881619-6ec0-4d30-835d-b73c778ef739)


------

## 💄 Face Retouching (Liquify Effect)

Used dlib for facial landmark detection
Implemented a Liquify-style function to adjust and refine the jawline area
Simulates a subtle face-slimming or reshaping effect, similar to tools found in Photoshop

![스크린샷 2024-06-10 154403](https://github.com/kim-hyona/opencv/assets/148624727/77c2d053-227c-43e6-a462-d1eeeea6032a)

