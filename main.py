import cv2
import numpy as np
import smtplib
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

def send_mail(from_id,to_id,password,message):
    server = smtplib.SMTP_SSL("smtp.gmail.com")
    server.login(from_id,password)
    message = f'vechical count is {message}'
    server.sendmail(from_id,to_id,message)
    server.quit()

def send_whatapp(name, message):
    driver = webdriver.Chrome('C:/Users/91728/Desktop/pythonProject/chromedriver.exe')
    driver.get("https://web.whatsapp.com/")
    time.sleep(15)
    message = f'vechical count is {message}'
    user = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//span[@title = "' + name + '"]'))).click()
    msg_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')))
    msg_box.send_keys(message)
    msg_box.send_keys(Keys.ENTER)

#largura_min training 80
#altura_min training 80
largura_min = 80
altura_min = 80
# offset training 6
offset = 6
#pos_linha training 550
pos_linha = 550
#delay training 60
delay = 60
detec = []
ctr = 0


def pega_centro(x, y, w, h):
    x1 =int( w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy



# Video Path 'C:/Users/91728/Downloads/video.mp4'
cap = cv2.VideoCapture('/Users/inukurthidileep/Downloads/vehicles on road .mp4')
subtractbg = cv2.bgsegm.createBackgroundSubtractorMOG()

while True:
    try:
        #trained video frame shape is (720 ,1280 3)
        ret, frame1 = cap.read()
        width = int(cap.get(3))
        heigth = int(cap.get(4))
        tempo = float(1 / delay)
        time.sleep(tempo)
        if heigth == 360:
            frame1 = cv2.resize(frame1,(0,0),fx = 2,fy = 2)
        elif heigth == 1080:
            frame1 = cv2.resize(frame1, (0, 0), fx=0.7, fy=0.7)
        elif heigth == 480:
            frame1 = cv2.resize(frame1, (0, 0), fx=1.2, fy = 1.6)
        #print(frame1.shape)
        grey_img = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        #blur scale on trained 3 3
        blur_img = cv2.GaussianBlur(grey_img, (3, 3), 5)

        img_sub = subtractbg.apply(blur_img)
        dilat = cv2.dilate(img_sub, np.ones((5, 5)))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
        dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
        dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
        contorno, h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (255, 127, 0), 3)
        for (i, c) in enumerate(contorno):
            (x, y, w, h) = cv2.boundingRect(c)
            validar_contorno = not ((w >= largura_min) and (h >= altura_min))
            if validar_contorno:
                continue

            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            centro = pega_centro(x, y, w, h)
            detec.append(centro)
            cv2.circle(frame1, centro, 4, (0, 0, 255), -1)

            for (x, y) in detec:
                #adjust base on test video
                if y < (pos_linha + offset) and y > (pos_linha - offset):
                    ctr += 1
                    cv2.line(frame1, (25, pos_linha), (1200, pos_linha), (0, 127, 255), 3)
                    detec.remove((x, y))

        # Left 450 70

        cv2.putText(frame1, "VEHICLE COUNT IS: " + str(ctr), (30, 70) , cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 5)
        cv2.putText(frame1, "RMKCET", (30, 500), cv2.FONT_ITALIC, 1, (255, 255, 0), 5)
        cv2.imshow("Vechical Detector", frame1)
        #cv2.imshow("Detector", dilatada)

        if cv2.waitKey(1) == 27 or cv2.waitKey(1) == ord('q'):
            break
    except:
        pass
print("Total detected cars: " + str(ctr))
#send_mail("ur@gmail.com","to","password",str(ctr))
send_whatapp("whatsapp_number",5)
#cv2.destroyAllWindows()
#cap.release()
exit()