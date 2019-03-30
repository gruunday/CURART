import numpy as np
import unittest
import img_manipulation as im
import data_mngmnt as dm
import tlsh

class TestImgManip(unittest.TestCase):

    def setUp(self):
        self.img = im.load_img('testImages/upside.jpg')
        self.kp, self.desc  = im.get_keypoints(self.img)
        self.packed_kp = dm.pack_keypoints(self.kp,self.desc)
        self.ukp,self.udesc = dm.unpack_keypoints(self.packed_kp)

    def test_pack_keypoints(self):
        truth_hash = '88F4EF0B150AAB64803653BA453181152B4EEB5D3963F32CB54E8EFE773958C8FEDC86'
        hashed_kp = tlsh.hash(str(self.packed_kp).encode('utf-8'))
        self.assertEqual(truth_hash, hashed_kp)
    
    def test_unpack_keypoints(self):
        for k,kp2 in zip(self.kp,self.ukp):
            if k.pt != kp2.pt:
                break
            if k.size != kp2.size:
                break
            if k.angle != kp2.angle:
                break
            if k.response != kp2.response:
                break
            if k.octave != kp2.octave:
                break
            if k.class_id != kp2.class_id:
                break
        self.assertEqual(1, 1)
    
    def test_unpack_desc(self):
        if np.array_equal(self.desc, self.udesc):
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 0)


