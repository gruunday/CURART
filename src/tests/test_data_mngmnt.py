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
        self.packed_kp = str(dm.sanatise(self.packed_kp))
        self.ukp,self.udesc = dm.unpack_keypoints(self.packed_kp)

    def test_pack_keypoints(self):
        self.assertGreater(len(self.packed_kp), 408900)
    
    def test_unpack_keypoints(self):
        for k,kp2 in zip(self.kp,self.ukp):
            if k.pt != kp2.pt:
                self.assertEqual(1, 0)
            if k.size != kp2.size:
                self.assertEqual(1, 0)
            if k.angle != kp2.angle:
                self.assertEqual(1, 0)
            if k.response != kp2.response:
                self.assertEqual(1, 0)
            if k.octave != kp2.octave:
                self.assertEqual(1, 0)
            if k.class_id != kp2.class_id:
                self.assertEqual(1, 0)
        self.assertEqual(1, 1)
    
    def test_unpack_desc(self):
        if np.array_equal(self.desc, self.udesc):
            self.assertEqual(1, 1)
        else:
            self.assertEqual(1, 0)
        #for one,two in zip(self.desc, self.udesc):
        #    print(one, ' == ', two)
