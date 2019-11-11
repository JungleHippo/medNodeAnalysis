import numpy as np
import matplotlib.pyplot as plt
import os
from skimage import io
from PIL import Image
import cv2
from sklearn.preprocessing import MinMaxScaler
from skimage import data, img_as_float
from skimage import exposure
import sys

'''Parsing images and adding them to lists, reshaped
at 224x224 pixels.
Returns a tuple (healthyImageList, cancerImageList).'''
def parseImages():
    path_no = 'complete_mednode_dataset/naevus'
    path_yes = 'complete_mednode_dataset/melanoma'
    cancerImageList = []
    healthyImageList = []
    paths = [path_yes, path_no]
    names = []
    global cancer, healthy
    for path in paths:
        for name in os.walk(path):
            names.append(name[2])

    cancer = names[0]
    healthy = names[1]

    for image in cancer:
        cancerImageList.append(Image.open(os.path.join(path_yes, image), 'r').resize((224, 224)))

    for image in healthy:
        healthyImageList.append(Image.open(os.path.join(path_no, image), 'r').resize((224, 224)))
    return (healthyImageList, cancerImageList)
'''End of function definition'''

'''RGB to YIQ. Returns a tuple (YIQ)'''
def rgb_to_yiq(r, g, b):
    y = 0.30*r + 0.59*g + 0.11*b
    i = 0.60*r - 0.28*g - 0.32*b
    q = 0.21*r - 0.52*g + 0.31*b
    return (y, i, q)
'''End of function definition'''

'''Converts the image(an numpy array) from rgb to yiq
To be used with an iterator for the complete directories.
Returns a 3D numpy array (YIQ)'''
def imageConversionToYIQ(image):
    image = np.array(image)

    shape = np.array(image).shape[:2]
    ivydeli = []
    ivydelii= []
    ivydeliii = []
    # TODO change the  range to np.array sth
    for mpla in range(224):
        for aman in range(224):
            a, b, c = rgb_to_yiq(image[mpla][aman][0], image[mpla][aman][1],
                           image[mpla][aman][2])
            ivydeli.append(a)
            ivydelii.append(b)
            ivydeliii.append(c)
            #ivy.append(list(a))
        #ivy.append(list(a))
    y = np.array(ivydeli).reshape(shape)
    i = np.array(ivydelii).reshape(shape)
    q = np.array(ivydeliii).reshape(shape)
    return (y, i, q);
'''End of function definition'''

'''Creating the graph with the histogram and respective image'''
def plot_img_and_hist(image, axes, bins=256):
    image = img_as_float(image)
    ax_img, ax_hist = axes
    ax_cdf = ax_hist.twinx()

    # Display image
    ax_img.imshow(image, cmap=plt.cm.gray)
    ax_img.set_axis_off()

    # Display histogram
    ax_hist.hist(image.ravel(), bins=bins, histtype='step', color='black')
    ax_hist.ticklabel_format(axis='y', style='scientific', scilimits=(0, 0))
    ax_hist.set_xlabel('Pixel intensity')
    ax_hist.set_xlim(0, 1)
    ax_hist.set_yticks([])

    # Display cumulative distribution
    img_cdf, bins = exposure.cumulative_distribution(image, bins)
    ax_cdf.plot(bins, img_cdf, 'r')
    ax_cdf.set_yticks([])

    return ax_img, ax_hist, ax_cdf
'''End of function definition'''

'''Histogram equalization'''
def hist_equal(image):
    image_equalized = exposure.equalize_hist(image)
    return image_equalized
'''End of function definition'''

def displayResults(image_equalized):
    fig = plt.figure(figsize=(2,5)) #figsize=(2, 5)
    axes = np.zeros((2, 1), dtype=np.object)
    #axes[0, 0] = fig.add_subplot(2, 1, 1)
    #axes[0, 0] = fig.add_subplot(1,1,1, sharex=axes[0, 0], sharey=axes[0, 0])
    axes[0, 0] = fig.add_subplot(2, 2, 1)
    axes[1, 0] = fig.add_subplot(2, 2, 2, sharex=axes[0, 0])
    ax_img, ax_hist, ax_cdf = plot_img_and_hist(image_equalized, axes[:, 0])
    ax_img.set_title('Histogram equalization')

    ax_cdf.set_ylabel('Fraction of total intensity')
    ax_cdf.set_yticks(np.linspace(0, 1, 5))
    fig.tight_layout()
    plt.show()
    plt.savefig(filepath+cancer[namecounter])


if __name__ == "__main__":

    
    images = parseImages() #index 0 contains the naevi cases and index 1 contains the melanoma cases
    global filepath
    filepath = os.getcwd()+"/melanomaGraphs/" ##Alazw to onoma tou fakelou edw kai to index apo 0 se 1 stis seires 130, 131 analogws
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    global namecounter
    for namecounter in range(len(images[0])):
        testImage = images[0][namecounter] #to 0 gia melanoma to 1 gia throumpes
        print(testImage)# Selects one image from the list
        yiqtestImage = imageConversionToYIQ(testImage)
        img = yiqtestImage[0] # The val of img is the 2D numpy array responding to the Y channel
        img = hist_equal(img) # Histogram equalization trasform
        print(type(img),img.shape)
        x = displayResults(img)
    #displayResults(img)
    #x.tight_layout()

    #y_eq=img_adapteq
    #plt.imshow(y_eq,cmap=plt.cm.gray)
