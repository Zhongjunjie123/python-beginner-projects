import cv2
import numpy as np
from pyzbar.pyzbar import decode


def decoder(image):
    # Creating a black and white style image to avoid confusion
    gray_img = cv2.cvtColor(image, 0)#0并不是灰度转换代码，而是 BGR 转 BGRA？
    # Decoding the gray image to some binary(二进制) image matrix
    barcode = decode(gray_img)#decode() 是 pyzbar 提供的识别函数。它接收图像，尝试识别其中的二维码或条形码。识别成功后，会返回一个包含识别结果的列表。例如，一张图片中有两个二维码，那么就可能返回两个识别结果
#obj.data	二维码存储的内容
#obj.type	二维码或条形码的类型
#obj.rect	二维码所在的矩形区域
#obj.polygon	二维码轮廓的顶点坐标
#第三方库的一个函数，可能一次性返回很多信息，但你的程序不一定需要使用全部信息
    
    # Algorithm to scan the obtained image
    for obj in barcode:                   #每一个 obj 都代表一个被识别出来的二维码或条形码对象
        points = obj.polygon              #获取二维码轮廓的多个顶点坐标？
        (x, y, w, h) = obj.rect           #获取二维码所在的矩形区域x：矩形左上角的横坐标。y：矩形左上角的纵坐标。w：矩形宽度。h：矩形高度。
        pts = np.array(poindts, np.int32)# 将points转为int32 32位整数矩阵（cv2.polylines需要用整数坐标确认画图位置）
        pts = pts.reshape((-1, 1, 2))    #这里的三个维度分别表示三个轴（Axis）上的元素数量（维度的含义取决于上下文）。OpenCV 的绘图 API，它要求轮廓点采用类似 (N, 1, 2) 的数组结构
        cv2.polylines(image, [pts], True, (0, 255, 0), 3) #[pts]代表画框的位置，用[]是因为可以同时画多个框。第三个参数true是框是否要闭合，第四个参数是BGR 颜色顺序，第五个参数代表框线的宽度

        barcodeData = obj.data.decode("utf-8")#.decode() 是 Python 字节对象自带的方法,指定使用 UTF-8 编码规则进行解码
        barcodeType = obj.type
        string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)

        cv2.putText(                          # OpenCV 提供的 putText() 函数，在图像上添加文字,第一个参数什么图，第二个参数写string,第三个参数在什么位置，第四个参数用什么字体，第五个参数字体大小，第六个参数什么颜色，第七个参数字体粗细
            frame, string, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2
        )
        print("Barcode: " + barcodeData + " | Type: " + barcodeType)


# Getting user's choice of usage
choice = int(input("1. Scan via image\n2. Scan via WebCam\n Choice: "))
if choice == 2:
    # Accessing webcam for images
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        decoder(frame)
        cv2.imshow("Image", frame)
        code = cv2.waitKey(10)
        if code == ord("q"):
            break
else:
    # Scanning the qrcode in locally available image
    img_path = input("Enter Image path: ")
    img = cv2.imread(img_path)
    detector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = detector.detectAndDecode(img)
    print("QRCode Encoded Data: ", data)
