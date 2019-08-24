from PIL import Image, ImageFilter
from matplotlib import pyplot as plt


def imageprepare(argv):
	"""
	This function returns the pixel values.
	The imput is a png file location.
	"""
	im = Image.open(argv).convert('L')
	width = float(im.size[0])
	height = float(im.size[1])
	newImage = Image.new('L', (28, 28), (255))  # creates white canvas of 28x28 pixels

	if width > height:  # check which dimension is bigger
		# Width is bigger. Width becomes 20 pixels.
		nheight = int(round((20.0 / width * height), 0))  # resize height according to ratio width
		if (nheight == 0):  # rare case but minimum is 1 pixel
			nheight = 1
		img = im.resize((20, nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)  # resize and sharpen
		wtop = int(round(((28 - nheight) / 2), 0))  # calculate horizontal position
		newImage.paste(img, (4, wtop))  # paste resized image on white canvas
	else:
		# Height is bigger. Heigth becomes 20 pixels.
		nwidth = int(round((20.0 / height * width), 0))  # resize width according to ratio height
		if (nwidth == 0):  # rare case but minimum is 1 pixel
			nwidth = 1
		img = im.resize((nwidth, 20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)  # resize and sharpen
		wleft = int(round(((28 - nwidth) / 2), 0))  # caculate vertical pozition
		newImage.paste(img, (wleft, 4))  # paste resized image on white canvas
	tv = list(newImage.getdata())  # get pixel values
	tva = [(255.0 - x) * 1.0 / 255.0 for x in tv]
	return tva


def resizeImage(argv):
	"""
	This function resize the image to a 28x28.
	The imput is a png file location.
	"""
	try:
		size = (28,28)
		im = Image.open(argv).convert('L')
		im = im.resize(size, Image.NEAREST)
		return list(im.getdata())
	except IOError:
		print "cannot resize image '%s'" % argv
		return None


def convertirImagen(imagefile):
	"""
	This function resize the image to a 28x28.
	The imput is a png file location.
	"""
	x = [resizeImage(imagefile)]		#file path here
	# Now we convert 784 sized 1d array to 24x24 sized 2d array so that we can visualize it
	newArr = [[0 for d in range(28)] for y in range(28)]
	k = 0
	for i in range(28):
		for j in range(28):
			newArr[i][j] = 255.0 - x[0][k]
			k = k + 1
	return newArr
