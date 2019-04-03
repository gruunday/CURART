import img_manipulation as im
import data_mngmnt as dm
from flask import Flask, render_template, request
import tlsh
import urllib.request as ureq
from werkzeug import secure_filename
import os
import random
import string
app = Flask(__name__)

FILE_PREFIX = 'tmp/'


@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_filer():
   if request.method == 'POST':
      loading()
      f = request.files['file']
      f.save(f'{FILE_PREFIX}{secure_filename(f.filename)}')

      # Process Image
      img = im.load_img(f'{FILE_PREFIX}{f.filename}')
      os.remove(f'{FILE_PREFIX}{f.filename}')
      kp, desc = im.get_keypoints(img)
      img_output = dm.pack_keypoints(kp, desc)
      img_hash = tlsh.hash(str(img_output).encode('utf-8'))
      result = dm.query_postgres(img_hash)

      matches = {}
      for item in result:
          tmp_kp, tmp_desc = dm.unpack_keypoints(item[2])
          match_score = im.get_match(desc, tmp_desc)
          matches[item[1]] = len(match_score)

      # Return Results
      if len(matches) > 0:
        url = max(matches, key=matches.get)
        filename = ''.join(random.choice(string.ascii_letters) for i in range(10))
        ureq.urlretrieve(url, f'static/img/{filename}')
        return render_template('result.html', value=filename)
      return render_template('nomatch.html')

def loading():
    return render_template('loading.html')

if __name__ == '__main__':
   app.run(debug = True)
