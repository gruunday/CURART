import sys
import img_manipulation as im
import data_mngmnt as dm
import urllib.request as ureq
import tlsh
import os

def main():
    if len(sys.argv) >= 2:
        input_file = sys.argv[1]
    else:
        print('Forgot file name as arg')

    with open(input_file, 'r') as f:
        urls = f.readlines()

    for u in urls:
        ureq.urlretrieve(u, 'tmp_download.jpg')
        img = im.load_img('tmp_download.jpg')
        os.remove('tmp_download.jpg')
        kp,desc = im.get_keypoints(img)
        pack = dm.pack_keypoints(kp, desc)
        img_hash = tlsh.hash(str(pack).encode('utf-8'))

        dm.write_postgres(img_hash, pack, u)
        print(f'Added: {u}')


if __name__ == '__main__':
    main()
