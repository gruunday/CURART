import img_manipulation as im
import data_mngmnt as dm
from flask import Flask, render_template, request
import tlsh
import urllib.request as ureq
from werkzeug import secure_filename
app = Flask(__name__)

@app.route('/upload')
def upload_file():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_filer():
   if request.method == 'POST':
      render_template('result.html')
      f = request.files['file']
      print(f.filename)
      f.save(secure_filename(f.filename))

      img = im.load_img(f.filename)
      kp, desc = im.get_keypoints(img)
      img_output = dm.pack_keypoints(kp, desc)
      img_hash = tlsh.hash(str(img_output).encode('utf-8'))
      result = dm.query_postgres(img_hash)
      if len(result) > 1:
        url = result[0][1]
        ureq.urlretrieve(url, 'static/img/download.jpg')
        return render_template('result.html')
      return render_template('nomatch.html')


if __name__ == '__main__':
   app.run(debug = True)
