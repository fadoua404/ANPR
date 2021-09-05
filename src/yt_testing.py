import cv2
import pytesseract
import numpy as np



pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

cascade=cv2.CascadeClassifier("src\data\haarcascade_russian_plate_number.xml")



def extract_num(img_name):
    global text
    img=cv2.imread(img_name)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    nplate=cascade.detectMultiScale(gray,1.1,4) #number-plate detection

    #cropping the plate
    for (x,y,w,h) in  nplate :
        a,b=(int(0.02*img.shape[0]) ,int(0.025*img.shape[1]))
        plate=img[y+a:y+h-a , x+b:x+w-b, :]

        #image processing (on the cropped image)
        kernel=np.ones((1,1) , np.uint8)
        plate=cv2.dilate(plate,kernel,iterations=1)
        plate=cv2.erode(plate,kernel,iterations=1)

        # convertion the plate image to the gray scale
        plate_gray=cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
        #convertion the plate image to black&white only 1
        (thresh , plate)=cv2.threshold(plate_gray,127,255,cv2.THRESH_BINARY)

        img_item= "plate.png"
        cv2.imwrite(img_item,plate)
        #cv2.imshow("threshold-image" , plate)
        #cv2.imwrite("temp.png",plate)

        #convertion the plate image to a text 
        text=pytesseract.image_to_string(plate)
        #deleting spaces
        text=''.join(e for e in text if e.isalnum())
        print(text)
        
        #drawing a rectangle around the plate
        cv2.rectangle(img , (x,y) , (x+w,y+h) ,(51,51,255), 2)
        cv2.rectangle(img , (x, y-40) ,(x+w,y) ,(51,51,255),-1)

        #put the text on the rectangle
        cv2.putText(img,text,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv2.LINE_AA)
        cv2.imshow("Plate",plate)



        cv2.imshow("Result",img)
        cv2.imwrite("Result.jpg",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

extract_num('src\images\car_1.jpg')




        

        


        