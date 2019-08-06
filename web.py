from flask import Flask, render_template, request, url_for, redirect
from werkzeug import secure_filename #pylint:off
import matplotlib.pyplot as plt
import io,os,sys, base64, logging, uuid, random
from PIL import Image

from processing.loaders import load_image, load_cfilter
from processing.colors import to_red, to_green, to_blue, to_monochrome, negative
from processing.convolution import convolve
from processing.median import median
from processing.presets import laplace


app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def home():
	if request.method == 'POST':
		f = request.files['file']
		filename =  str(random.randint(100000,9999999)) +'.' + f.filename.rsplit('.', 1)[1]	
		f.save(secure_filename(filename))
		return redirect(url_for('image', imageid=filename))

	elif request.method == 'GET':
		return render_template('index.html',image=False)


@app.route('/image/<imageid>/', methods= ['GET','POST'])
def image(imageid):
	img = load_image(imageid)
	kernels = kernel_list()

	transform = []
	print(request.form, file=sys.stderr)
	
	new = img

	# Cores
	if 'cores' in request.form.keys():
		cm = request.form.get("cores")
		if   cm == 'R': new = to_red(new); transform.append('Red')
		elif cm == 'G': new = to_green(new); transform.append('Green')
		elif cm == 'B': new = to_blue(new); transform.append('Blue')
		elif cm == 'Mono': new = to_monochrome(new); transform.append('Mono')

	#Efeitos
	for kn in request.form.keys():
		pass

	for kn in request.form.keys():
			

		if kn == 'laplace': 
			new = laplace(new)
			transform.append(kn)
		elif kn == 'to_red':
			new = to_red(new)
			transform.append(kn)
		elif kn == 'to_green':
			new = to_green(new)
			transform.append(kn)
		elif kn == 'to_blue':
			new = to_blue(new)
			transform.append(kn)
		elif kn == 'monochrome':
			new = to_monochrome(new)
			transform.append(kn)
		elif kn == 'negative':
			new = negative(new)
			transform.append('Negative')


		elif kn in kernels:
			print(kernels[kn], file=sys.stderr)
			krn = load_cfilter(kernels[kn])
			new = convolve(new, krn)
			transform.append(kn)
	if not transform:
		new = False
		transform = False

	print(transform)

	return render_template('image.html',image=img, newimage=new,imageid=imageid, kernels=kernels, transform=transform)



# UTILS -------------------------------------------------


@app.context_processor
def image_processor():
	def im_plot(image):

		pil_img = Image.fromarray(image.astype('uint8'))
		buff = io.BytesIO()
		pil_img.save(buff, format="JPEG")
		buff.seek(0)
			
		return base64.b64encode(buff.getvalue()).decode()
		
	return dict(im_plot=im_plot)


def kernel_list():
	"""retorna a lista de mascaras convolucionais"""
	kernels = {}

	for subdir, _, files in os.walk('kernels'):
		for file in files:
			filepath = subdir + os.sep + file
			
			if filepath.endswith(".txt"):
				kernels[file] = filepath

	return kernels
				
			
# ------------------ STARTUP -------------------------#

if __name__ == '__main__':
	app.run(debug = True) #pylint: off