import img_manipulation as im
import data_mngmnt as dm
from flask import Flask, render_template, request
import tlsh
import urllib.request as ureq
from werkzeug import secure_filename
import os
app = Flask(__name__)

FILE_PREFIX = 'tmp/'


@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_filer():
   if request.method == 'POST':
      render_template('result.html')
      f = request.files['file']
      f.save(f'{FILE_PREFIX}{secure_filename(f.filename)}')

      # Process Image
      img = im.load_img(f'{FILE_PREFIX}{f.filename}')
      os.remove(f'{FILE_PREFIX}{f.filename}')
      kp, desc = im.get_keypoints(img)
      img_output = dm.pack_keypoints(kp, desc)
      img_hash = tlsh.hash(str(img_output).encode('utf-8'))
      result = dm.query_postgres(img_hash)

      # Return Results
      if len(result) > 0:
        url = result[0][1]
        ureq.urlretrieve(url, 'static/img/download.jpg')
        return render_template('result.html')
      return render_template('nomatch.html')


if __name__ == '__main__':
   app.run(debug = True)
