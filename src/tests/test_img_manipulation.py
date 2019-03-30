import numpy as np
import unittest
import img_manipulation as im

class TestImgManip(unittest.TestCase):

    def setUp(self):
        self.img = im.load_img('testImages/upside.jpg')

    def test_load_img(self):
        self.assertEqual(str(type(im.load_img('testImages/upside.jpg'))), \
                              "<class 'numpy.ndarray'>")

    def test_get_keypoints_len_one(self):
        self.assertGreaterEqual(len(im.get_keypoints(self.img)[0]), 930)

    def test_get_keypoints_len_two(self):
        self.assertGreaterEqual(len(im.get_keypoints(self.img)[1]), 930)
    
    def test_get_keypoints_type(self):
        key_lst = im.get_keypoints(self.img)[0]
        for i in range(len(key_lst)):
            self.assertEqual(str(type(key_lst[i])), "<class 'cv2.KeyPoint'>")
    
    def test_rotate_img(self):
        self.assertEqual(len(self.img), len(im.rotate_img(self.img)))

    def test_match_images_different(self):
        rotated_img = im.rotate_img(self.img)
        self.assertGreaterEqual(im.match_images(self.img, rotated_img), 2)

    def test_match_images_identical(self):
        match_result = im.match_images(self.img, self.img)
        self.assertGreaterEqual(match_result, "Images Exactly Identical")
