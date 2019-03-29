import unittest
import img_manipulation as im

class TestImgManip(unittest.TestCase):

    def setUp(self):
        self.img = im.load_img('testImages/upside.jpg')

    def test_load_img(self):
        self.assertEqual(str(type(im.load_img('testImages/upside.jpg'))), \
                              "<class 'numpy.ndarray'>")

    def test_get_keypoints_len_one(self):
        self.assertEqual(len(im.get_keypoints(self.img)[0]), 940)

    def test_get_keypoints_len_two(self):
        self.assertEqual(len(im.get_keypoints(self.img)[1]), 940)
    
    def test_get_keypoints_type(self):
        key_lst = im.get_keypoints(self.img)[0]
        for i in range(len(key_lst)):
            self.assertEqual(str(type(key_lst[i])), "<class 'cv2.KeyPoint'>")
