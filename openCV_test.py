import unittest
import numpy as np
import cv2
from openCV import prestej_piksle_z_barvo_koze

class TestOpenCVFunctions(unittest.TestCase):
    def test_prestej_piksle_z_barvo_koze(self):
        img = cv2.imread("test.png")
        if img is None:
            self.fail("test.png not found or could not be loaded.")

        spodnjaMeja = np.array([0, 48, 80], dtype=np.uint8)
        zgornjaMeja = np.array([20, 255, 255], dtype=np.uint8)

        num_skin_pixels = prestej_piksle_z_barvo_koze(img, (spodnjaMeja, zgornjaMeja))

        mask = cv2.inRange(img, spodnjaMeja, zgornjaMeja)
        expected_num_skin_pixels = cv2.countNonZero(mask)

        self.assertEqual(num_skin_pixels, expected_num_skin_pixels)

    def test_zmanjsaj_sliko(self):
        img = cv2.imread("test.png")
        if img is None:
            self.fail("test.png not found or could not be loaded.")

        resized_img = cv2.resize(img, (100, 100))

        self.assertEqual(resized_img.shape[0], 100)
        self.assertEqual(resized_img.shape[1], 100)

    #def test_fail(self):
        #self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()