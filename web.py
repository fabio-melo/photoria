from flask import Flask, render_template, request, url_for, redirect
from werkzeug import secure_filename 
import matplotlib.pyplot as plt
import io,os,sys, base64, logging, uuid, random
from time import time
from PIL import Image

from processing.loaders import load_image, load_cfilter
from processing.colors import to_red, to_green, to_blue, to_monochrome, negative, \
	add_brightness, add_brightness_yiq, limiar, mul_brightness, mul_brightness_yiq,negative_rgb, to_monochrome_2D
from processing.convolution import convolve
from processing.median import median
from processing.sobel import sobel

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
	t0 = time()
	# Cores
	if 'cores' in request.form.keys():
		cm = request.form.get("cores")
		if   cm == 'R': new = to_red(new); transform.append('Red')
		elif cm == 'G': new = to_green(new); transform.append('Green')
		elif cm == 'B': new = to_blue(new); transform.append('Blue')
		elif cm == 'Mono': new = to_monochrome(new); transform.append('Mono')
		elif cm == 'Mono2d': new = to_monochrome_2D(new); transform.append('Mono2d')


	if 'negative' in request.form.keys():
		new = negative(new);transform.append('Negative')

	if 'negativergb' in request.form.keys():
		new = negative_rgb(new);transform.append('NegativeRGB')



	if 'limiar' in request.form.keys():
		cm = request.form.get('limiar_qt')
		if cm:
			new = limiar(new, int(cm)); transform.append(f'Limiar {cm}')
		else:
			new = limiar(new); transform.append('Limiar 127')

	if 'brilhom' in request.form.keys():
		cm = request.form.get('brilho_mul')
		if cm:
			new = mul_brightness(new, float(cm)); transform.append(f'Brilho Mul {cm}')

	if 'brilhoadd' in request.form.keys():
		cm = request.form.get('brilho_add')
		if cm:
			new = add_brightness(new, float(cm)); transform.append(f'Brilho Add {cm}')
	
	if 'brilhomultyiq' in request.form.keys():
		cm = request.form.get('brilho_mul_yiq')
		if cm:
			new = mul_brightness_yiq(new, float(cm)); transform.append(f'Brilho Mul yiq {cm}')

	if 'brilhoadd' in request.form.keys():
		cm = request.form.get('brilho_add_yiq')
		if cm:
			new = add_brightness_yiq(new, float(cm)); transform.append(f'Brilho Add {cm}')
	
	if 'mediana' in request.form.keys():
		sx = request.form.get('medianax')
		sy = request.form.get('medianay')
		if sx and sy:
			new = median(new,krn_y=int(sy), krn_x=int(sx)); transform.append(f'Mediana {sy} X {sx}')
	
	if 'sobel' in request.form.keys():
		new = sobel(new); transform.append(f'Sobel')

	for kn in request.form.keys():

		if kn in kernels:
			print(kernels[kn], file=sys.stderr)
			krn = load_cfilter(kernels[kn])
			new = convolve(new, krn)
			transform.append(kn)
	
	t1 = time()
	timeexec = str(round(t1 - t0, 4)) 
	if not transform:
		new = False
		transform = False

	print(transform)

	return render_template('image.html',image=img, newimage=new,imageid=imageid, kernels=kernels, transform=transform, timeexec=timeexec)



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