import cv2
from cvzone.HandTrackingModule import HandDetector

# inicia a captura de video da webcam
cap = cv2.VideoCapture(0)
# define os tamanhos da captura
cap.set(3, 1280)
cap.set(4, 720)

# inicia o detector da mão usando o HandTrackingModule do cvzone
detector = HandDetector(detectionCon=0.7)
# variável que define a distância entre as mãos
startDist = None
# fator de escala do zoom, iniciado em 0
scale = 0
# coordenadas do inicio da imagem
cx, cy = 0, 0


while True:
    success, img = cap.read()

    # detecção das mãoes
    hands, img = detector.findHands(img)
    img1 = cv2.imread("oculos.png")

    # confere se as duas mãos estão visíveis na tela
    if len(hands) == 2:
        # confere os posicionamento dos dedos
        # print(detector.fingersUp(hands[0]))

        if detector.fingersUp(hands[0]) == [1, 1, 0, 0, 0] and \
                detector.fingersUp(hands[1]) == [1, 1, 0, 0, 0]:
            lmList1 = hands[0]["lmList"]
            lmList2 = hands[1]["lmList"]
            
            
            # calcula a distância entre as mãos
            if startDist is None:
                length, info, img = detector.findDistance(hands[0]["center"], hands[1]["center"], img)
                startDist = length

            # define a nova escala para a imagem conforme a distância entre as mãos
            length, info, img = detector.findDistance(hands[0]["center"], hands[1]["center"], img)
            scale = int((length - startDist)/2)
            cx, cy = info[4:]
    else:
        startDist = None

    try:
        # redefine a imagem com a nova escala
        h1, w1, _= img1.shape
        newH, newW = ((h1+scale)//2)*2, ((w1+scale)//2)*2
        img1 = cv2.resize(img1, (newW,newH))

        # posiciona a imagem gerada sob a imagem capturada a webcam
        img[cy-newH//2:cy+ newH//2, cx-newW//2:cx+ newW//2] = img1
    except:
        pass

    # espelhando a imagem horizontalmente para melhor localização
    img = cv2.flip(img, 1)

    cv2.imshow("Image", img)
    # caso a tecla 'q' seja pressionada, o loop encerra
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
