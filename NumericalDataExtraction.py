import numpy as np
import os
import cv2
import pandas as pd
'''
Ο παρακάτω κώδικας, διαβάζει τις εικόνες που περιέχονται στους φακέλους σε 3D numpy arrays (μήκος χ πλάτος χ χρώμα (RGB)).
Από κάθε 3d πίνακα προκύπτουν 3 2d πίνακες, όπου μετράμε το πλήθος των pixel με τιμή από 0-255 και την eCDF για χ <= value:

       Red          Blue           Green
------------------------------------------
   Pixels | CDF  Pixels | CDF   Pixels | CDF 
0    x       Y      x      Y      x       Y
1 
2
3     .   ..    ..  . . . .   .   ..  . . .
4
5


Τα αποτελέσματα αποθηκεύονται σε 2 csv για κάθε χρώμα (Cancer_hist_red ή healthy_cdf_blue πχ) με μορφή:
*Cancer_hist_red.csv*

       Εικ. 1          Εικ. 2           Εικ. 3
------------------------------------------
   Pixels             Pixels          Pixels    
0    x                  x                x       
1 
2
3     .   ..    ..  . . . .   .   ..  . . .
4
5

*Healthy_cdf_blue.csv*

       Εικ. 1          Εικ. 2           Εικ. 3
------------------------------------------
   CDF                 CDF              CDF    
0    x                  x                x       
1 
2
3     .   ..    ..  . . . .   .   ..  . . .
4
5

'''


def parseImages():
    path_healthy = 'complete_mednode_dataset/naevus' 
    path_cancer = 'complete_mednode_dataset/melanoma'
    cancerImageList = []
    healthyImageList = []
    paths = [path_cancer, path_healthy]
    names = []
    global cancerImageNames, healthyImageNames
    for path in paths:
        for name in os.walk(path):
            names.append(name[2])

    cancerImageNames = names[0]
    healthyImageNames = names[1]

    for image in cancerImageNames:
        #cancerImageList.append(Image.open(os.path.join(path_cancer, image), 'r'))
        cancerImageList.append(cv2.imread(os.path.join(path_cancer, image)))
    for image in healthyImageNames:
        healthyImageList.append(cv2.imread(os.path.join(path_healthy, image)))
    return (healthyImageList, cancerImageList)

def histCdfData(image): #image = 2D numpy array
    image = image.ravel() # 2D -> 1D
    image.sort()
    values = np.arange(0, 256, 1)
    cdf = image.searchsorted(values, side = 'right') # TODO write cdf = np.append(x, [image.size-x[-1])
    hist = np.zeros(256)

    hist[0] = cdf[0] #the number of pixels with value 0
    for i in range(1, 256):
        hist[i] = cdf[i] - cdf[i-1]

    hist = hist/image.size # Normalisation
    cdf = cdf/ image.size
    data = np.vstack((hist,cdf))
    if data.shape == (2, 256):
        data = np.transpose(data)

    #SAVE np.savetxt('name ', data, delimiter = ',', header = "Pixel Ratio, CDF")
    print(data[:,0].shape)
    return data


if __name__ == '__main__':
    (healthy, cancer) = parseImages() # the tuple contains numpy arrays
    hCdf = np.empty((256,len(healthy)))
    hHist = np.empty((256,len(healthy)))
    cCdf = np.empty((256,len(cancer)))
    cHist = np.empty((256,len(cancer)))
    Channels = {0 : 'Blue',
                1 : 'Green',
                2 : 'Red'} # add more for other color spaces
    for j in range(len(Channels.keys())): # {0, 1, 2} -> {B, G, R}
        for i in range(0, min(len(healthy), len(cancer))):
            cData = histCdfData(cancer[i][:, :, j])
            hData = histCdfData(healthy[i][:, :, j])
            hHist[:, i] = hData[:, 0]
            hCdf[:, i] = hData[:, 1]
            cHist[:, i] = cData[:, 0]
            cCdf[:, i] = cData[:, 1]
        if len(healthy) < len(cancer):
            for i in range(min(len(healthy), len(cancer)), max(len(healthy), len(cancer))):
                cData = histCdfData(cancer[i][:, :, j])
                cHist[:, i] = cData[:, 0]
                cCdf[:, i] = cData[:, 1]
        elif len(healthy) > len(cancer):
            for i in range(min(len(healthy), len(cancer)), max(len(healthy), len(cancer))):
                hData = histCdfData(healthy[i][:, :, j])
                hHist[:, i] = hData[:, 0]
                hCdf[:, i] = hData[:, 1]

        print(cCdf.shape, len(cancer))


        np.savetxt('Cancer_cdf' + Channels[j] + '.csv', cCdf, delimiter=',', header = ','.join(cancerImageNames))
        np.savetxt('Cancer_hist' + Channels[j] + '.csv', cHist, delimiter=',', header = ','.join(cancerImageNames))
        np.savetxt('Healthy_cdf' + Channels[j] + '.csv', hCdf, delimiter=',', header = ','.join(healthyImageNames))
        np.savetxt('Healthy_hist' + Channels[j] + '.csv', hHist, delimiter=',', header = ','.join(healthyImageNames))

