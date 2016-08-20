import cv2
import numpy

class ImgProcess:
	def imgDecode(imgStr):
		data = numpy.fromstring(imgStr, dtype = 'unint8')
		img = cv2.imdecode(data, 1)

		return img

	def imgToString(imgName):
		img = cv2.imread("image/" + imgName)
		imgStr = cv2.imencode('.jpg', img)[1].tostring()

		imgLen = str(len(imgStr))
		imgStr = "image" + "*" imgName + "*" + imgLen + "*" + imgStr

		return imgStr

	def imgSave(imgName, img):
		cv2.imwrite("image/" + imgName, img)
