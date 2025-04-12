import numpy as np
import cv2
import time

subRegionsPerRow = 20
colorCloseness = 0.10
numOfRequiredSkinPixels = 5

def doloci_barvo_koze(slika, spodnjaMeja = np.array([0, 0, 0]), zgornjaMeja = np.array([0, 0, 0])):
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            color = slika[y, x]
            spodnjaMeja[:] = np.clip(color - color * colorCloseness, 0, 255)
            zgornjaMeja[:] = np.clip(color + color * colorCloseness, 0, 255)

    cv2.setMouseCallback("ORV vaja 1", mouse_callback)
    return (spodnjaMeja,zgornjaMeja)

def zmanjsaj_sliko(slika,sirina,visina):
    pomanjsana_slika = cv2.resize(slika, (sirina, visina))
    return pomanjsana_slika

def obdelaj_sliko_s_skatlami(slika, sirina_skatle, visina_skatle, barva_koze):
    subBoxes = []
    for i in range(0, slika.shape[0], visina_skatle):
        for j in range(0, slika.shape[1], sirina_skatle):
            topLeft = (j, i)
            bottomRight = (j + sirina_skatle, i + visina_skatle)
            numOfSkinPixels = prestej_piksle_z_barvo_koze((slika[topLeft[1]:bottomRight[1], topLeft[0]:bottomRight[0]]),barva_koze)
            subBoxes.append((topLeft, bottomRight, numOfSkinPixels))

    return subBoxes

def prestej_piksle_z_barvo_koze(slika, barva_koze):
    spodnjaMeja, zgornjaMeja = barva_koze
    mask = cv2.inRange(slika, spodnjaMeja, zgornjaMeja)
    return cv2.countNonZero(mask)

def main():
    window_name = "ORV vaja 1"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    spodnjaMeja = np.array([0, 0, 0])
    zgornjaMeja = np.array([255, 255, 255])
    prev_time = time.time()
    while True:
        img = cv2.imread("test.png")
        img = zmanjsaj_sliko(img, 260, 300)
        cv2.waitKey(10)

        spodnjaMeja, zgornjaMeja = doloci_barvo_koze(img, spodnjaMeja, zgornjaMeja)

        subBoxes = obdelaj_sliko_s_skatlami(img, 260//subRegionsPerRow, 300//subRegionsPerRow, (spodnjaMeja, zgornjaMeja))
        for i in subBoxes:
            topLeft = i[0]
            bottomRight = i[1]
            numOfSkinPixels = i[2]
            if numOfSkinPixels > numOfRequiredSkinPixels:
                cv2.rectangle(img, topLeft, bottomRight, (0, 255, 0), 1)

        current_time = time.time()
        fps = 1 / (current_time - prev_time)
        prev_time = current_time

        cv2.imshow(window_name, img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()