from flask import Flask, render_template, request, url_for, redirect
from werkzeug import secure_filename
import matplotlib.pyplot as plt
import io,os,sys, base64, logging, uuid, random
from PIL import Image
from models import ImageData, MaskData
from operations import convolve,median

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
	if request.method == 'POST':
		f = request.files['file']
		filename = str(random.randint(100000,9999999)) +'.' + f.filename.rsplit('.', 1)[1]	
		f.save(secure_filename(filename))
		return redirect(url_for('image', imageid=filename))

	elif request.method == 'GET':
		return render_template('index.html',image=False)

@app.route('/image/<imageid>/', methods= ['GET','POST'])
def image(imageid):
	img = ImageData(imageid)
	masks = mask_list()
	transform = request.form.get('maskoptions')
	if transform:
		if transform == 'mediana33':
			newimg = median(img,3,3)
		elif transform == 'mediana55':
			newimg = median(img,5,5)
		elif transform == 'mediana77':
			newimg = median(img,7,7)
		else:
			msk = MaskData(masks[request.form.get('maskoptions')])
			newimg = convolve(img, msk)
	else:
		newimg = False
	print(transform)

	return render_template('image.html',image=img, newimage=newimg,imageid=imageid, masks=masks, transform=transform)




@app.context_processor
def image_processor():
	def im_plot(image):

		pil_img = Image.fromarray(image.mtx)
		buff = io.BytesIO()
		pil_img.save(buff, format="JPEG")
		buff.seek(0)
			
		return base64.b64encode(buff.getvalue()).decode()
		
	return dict(im_plot=im_plot)

def mask_list():
	"""retorna a lista de mascaras convolucionais"""
	masks = {}

	for subdir, _, files in os.walk('masks'):
		for file in files:
			filepath = subdir + os.sep + file
			
			if filepath.endswith(".txt"):
				masks[file] = filepath
		
	return masks
				
def img_to_b64(img):
	pil_img = Image.fromarray(img)
	buff = io.BytesIO()
	pil_img.save(buff, format="JPEG")
	buff.seek(0)

	return base64.b64encode(buff.getvalue()).decode()

if __name__ == '__main__':
	app.run(debug = True)