import os
import io
import curart
import unittest
import glob

class CurartTestCase(unittest.TestCase):

    def setUp(self):
        curart.app.testing = True
        self.app = curart.app.test_client()

    def test_upload_page(self):
        d = {}
        print('Dir contents')
        print(glob.glob("tmp/*"))
        with open('testImages/upside.jpg', 'rb') as image:
            d['file'] = (io.BytesIO(image.read()), 'testImages/upside.jpg')
            rv = self.app.post('/uploader', data=d, follow_redirects=True, content_type='multipart/form-data')
            assert True

