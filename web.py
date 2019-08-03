from flask import Flask, render_template, request
from werkzeug import secure_filename
from models import ImageData
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
   if request.method == 'POST':
      f = request.files['file']
      image = ImageData(f)
      #f.save(secure_filename(f.filename))
      return render_template('index.html',image=image)
   elif request.method == 'GET':
      return render_template('index.html',image=False)
		


@app.context_processor
def image_processor():
   def im_plot(image):

      img = io.BytesIO()
      print(image)
      plt.imshow(image.mtx)
      plt.savefig(img, format='png')
      img.seek(0)

      plot_url = base64.b64encode(img.getvalue()).decode()

      return plot_url

   return dict(im_plot=im_plot)

if __name__ == '__main__':
   app.run(debug = True)