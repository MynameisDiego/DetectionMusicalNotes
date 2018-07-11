import cv2
import numpy as np
import math

imagen = cv2.imread("d:/INTENTOFINALPDI/fire.jpg",0)
#gris = cv2.cvtColor(imagen,cv2.COLOR_BGR2GRAY)
_, thresholded = cv2.threshold(imagen,160, 255, cv2.THRESH_BINARY)
im_with_blobs = thresholded.copy()
im_inv = (255 - im_with_blobs)
kernel = cv2.getStructuringElement(ksize=(1, int(im_inv.shape[0] / 500)), shape=cv2.MORPH_RECT)
horizontal_lines = cv2.morphologyEx(im_inv, cv2.MORPH_OPEN, kernel)
horizontal_lines = (255 - horizontal_lines)
kernel = cv2.getStructuringElement(ksize=(int(im_inv.shape[1] /350), 1), shape=cv2.MORPH_RECT)
vertical_lines = cv2.morphologyEx(255 - horizontal_lines, cv2.MORPH_OPEN, kernel)
vertical_lines = (255 - vertical_lines)

cv2.imwrite("d:/INTENTOFINALPDI/final.png",horizontal_lines)
#Encontrando Notas
#quarter_recs = locate_images(img_gray, quarter_imgs, quarter_lower, quarter_upper, quarter_thresh)
class Rectangle(object):
    def __init__(self, x, y, w, h):
        self.x = x;
        self.y = y;
        self.w = w;
        self.h = h;
        self.middle = self.x + self.w/2, self.y + self.h/2
        self.area = self.w * self.h

    def overlap(self, other):
        overlap_x = max(0, min(self.x + self.w, other.x + other.w) - max(self.x, other.x));
        overlap_y = max(0, min(self.y + self.h, other.y + other.h) - max(self.y, other.y));
        overlap_area = overlap_x * overlap_y
        return overlap_area / self.area

    def distance(self, other):
        dx = self.middle[0] - other.middle[0]
        dy = self.middle[1] - other.middle[1]
        return math.sqrt(dx*dx + dy*dy)

    def merge(self, other):
        x = min(self.x, other.x)
        y = min(self.y, other.y)
        w = max(self.x + self.w, other.x + other.w) - x
        h = max(self.y + self.h, other.y + other.h) - y
        return Rectangle(x, y, w, h)

    def draw(self, img, color, thickness):
        pos = ((int)(self.x), (int)(self.y))
        size = ((int)(self.x + self.w), (int)(self.y + self.h))
        cv2.rectangle(img, pos, size, color, thickness)

negras = ["d:/IntentoFINALPDI/templateNegra.png"]
negras = [cv2.imread(negra,0) for negra in negras]
soles = [cv2.imread("d:/IntentoFINALPDI/templateSol.png",0)]
#sol = [""d:/IntentoFINALPDI/templateNegra.png"]


def buscarNota(notas, threshold):
    mejorContador = -1
    mejorUbicacion = []
    ubicacion = []
    contador = 0
    
    for nota in notas:
        match = cv2.matchTemplate(horizontal_lines,nota,cv2.TM_CCOEFF_NORMED)
        match = np.where(match >= threshold)
        contador += len(match[0])
        ubicacion += [match]
        
    if (contador > mejorContador):
        mejorContador = contador
        mejorUbicacion = ubicacion
    
    elif(contador < mejorContador):
        pass
    
    
    ubicaciones = []
    for i in range(len(notas)):
        ancho , alto = notas[i].shape[::-1]
        ubicaciones.append([Rectangle(pt[0], pt[1],ancho,alto) for pt in zip(*mejorUbicacion[i][::-1])])
    
    ubicacionesTotal = [j for i in ubicaciones for j in i]
    imagenOriginal = horizontal_lines.copy()
    for r in ubicacionesTotal:
        r.draw(imagenOriginal, (0,0,255),2)
       
    return imagenOriginal


NegrasTotal = buscarNota(negras,0.70)
cv2.imwrite('negras.png',NegrasTotal )
SolTotal = buscarNota(soles,0.70)
cv2.imwrite('soles.png',SolTotal)