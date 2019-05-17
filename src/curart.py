import img_manipulation as im
import data_mngmnt as dm
from flask import Flask, render_template, request
import tlsh
import urllib.request as ureq
from werkzeug import secure_filename
import os, io
import random
import string
app = Flask(__name__)

FILE_PREFIX = 'tmp/'


@app.route('/')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_filer():
   print(flask.__version__)
   if request.method == 'POST':
      f = request.files['file']
      f.save(f'{FILE_PREFIX}{secure_filename(f.filename)}')

      # Process Image
      img = im.load_img(f'{FILE_PREFIX}{secure_filename(f.filename)}')
      kp, desc = im.get_keypoints(img)
      img_output = dm.pack_keypoints(kp, desc)
      img_hash = tlsh.hash(str(img_output).encode('utf-8'))
      result = dm.query_postgres(img_hash)
      f = open('panic.log', 'w')
      
      matches = {}
      for item in result:
          tmp_kp, tmp_desc = dm.unpack_keypoints(item[2])
          match_score = im.get_match(desc, tmp_desc)
          #print(match_score)
          matches[item[1]] = len(match_score)
      f.write(f'{matches}')
      f.write(f'{len(matches)}')
      f.close()
      # Return Results
      if len(matches) > 0:
        url = max(matches, key=matches.get)
        # Generate random string for filename 
        # This can help prevent browser caching of an image that has changed
        filename = ''.join(random.choice(string.ascii_letters) for i in range(10))
        ureq.urlretrieve(url, f'static/img/{filename}')
        img_2 = im.load_img(f'static/img/{filename}')
        os.remove(f'static/img/{filename}')

        return render_template('result.html', value=url)
      return render_template('nomatch.html')

if __name__ == '__main__':
   app.run(debug = True)
