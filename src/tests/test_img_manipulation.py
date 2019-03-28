import unittest
import img_manipulation as im

class TestImgManip(unittest.TestCase):

    def test_load_img(self):
        self.assertEqual(str(type(im.load_img('testImages/upside.jpg'))), \
                              "<class 'numpy.ndarray'>")
