import cv2
import numpy

class ImgProcess:
	def imgDecode(img_str):
		data = numpy.fromstring(img_str, dtype = 'unint8')
		img = cv2.imdecode(data, 1)

		return img

	def imgToString(imgName):
		fd = open("image/" + imgName, 'rb')
		img_str = str(fd.read())
		fd.close()

		return img_str

	def imgSave(imgName, img):
		cv2.imwrite("image/" + imgName, img)
