import os
import io
import curart
import unittesta
import PIL

class CurartTestCase(unittest.TestCase):

    def setUp(self):
        curart.app.testing = True
        self.app = curart.app.test_client()

    def test_home_page(self):
        rv = self.app.get('/')
        assert rv.status_code == 200

    def test_upload_page(self):
        d = {}
        d['file'] = (io.BytesIO(b'test'), 'testImages/upside.jpg')
        rv = self.app.post('/uploader', data=d, follow_redirects=True, content_type='multipart/form-data')
        assert True

