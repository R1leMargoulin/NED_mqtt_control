from vision_src.image_functions import *
from vision_src.markers_detection import *
from vision_src.CalibrationObject import *
import cv2
import numpy as np


def cut_img(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    img_thresh = cv2.adaptiveThreshold(gray, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
                                        thresholdType=cv2.THRESH_BINARY, blockSize=15, C=25)
    list_good_candidates = find_markers_from_img_thresh(img_thresh)
    if len(list_good_candidates) == 4:
        list_good_candidates = sort_markers_detection(list_good_candidates)
    else:
        list_good_candidates = complicated_sort_markers(list_good_candidates)



    im_cut = extract_sub_img(image, list_good_candidates)
    return im_cut

def get_matrix_position(im_cut, nb_contours=8, nb_to_delete = 1):

    gray_cut = cv2.cvtColor(im_cut, cv2.COLOR_BGR2GRAY)
    edged_cut = cv2.adaptiveThreshold(gray_cut, maxValue=255, adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
                                        thresholdType=cv2.THRESH_BINARY, blockSize=15, C=25)
    findcontours = cv2.findContours(edged_cut,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2]


    #Il faut que le nombre de "biggest_contours_finder" soit supérieur de 3 par rapport aux nombres de contours que l'on veut détecter (exemple : si on veut détecter 2 contours dans la zone il faudra mettre 5 dans la fonction)
    ctrs =biggest_contours_finder(edged_cut, nb_contours +3)
    for i in range(nb_to_delete):
        ctrs.pop(0)

    barycenters=[]

    for c in ctrs:
        coords = get_contour_barycenter(c)
        verif = True
        for b in barycenters:
            if((coords[0] < b[0]+10 and coords[0] > b[0] -10) and (coords[1] < b[1]+10 and coords[1] > b[1]-10)):
                verif = False
        if (verif == True):
            barycenters.append(coords)

    #on met les y dans un dictionnaire pour pouvoir les trier en fonction de l'axe y
    ydict = {}
    for i in range(len(barycenters)):
        ydict.update({i:barycenters[i][1]})
    ydicttri = {k: v for k, v in sorted(ydict.items(), key=lambda item: item[1])}
    #print("dico Y trie : " + str(ydicttri))
    #on separe notre tableau en 2 lignes de matrices


    ligne1 = []
    ligne2 = []
    for i in ydicttri.items():
        if(i[0]<=(len(ydicttri)/2)):
            ligne1.append(barycenters[i[0]])
        else:
            ligne2.append(barycenters[i[0]])
    matrix = [ligne1, ligne2]

    #on tri les lignes de notre matrice en fonction de l'axe x cette fois
    for l in range(len(matrix)):
        xdict = {}
        for i in range(len(matrix[l])):
            xdict.update({i:matrix[l][i][0]})
        xdictTri = {k: v for k, v in sorted(xdict.items(), key=lambda item: item[1])}
        newligne = []
        for i in xdictTri.items():
            newligne.append(matrix[l][i[0]])
        matrix[l] = newligne

    print(matrix)
    return matrix

if __name__ == "__main__":
    img = cv2.imread('C:/Users/aerisay/Documents/Projet_Niryo/Images/Zone_niryo.png')
    get_matrix_position(img, 4)