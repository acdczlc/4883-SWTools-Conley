#Zac Conley
#A07 - match
#compares emojis and finds closest matches

from skimage.measure import compare_ssim as ssim
import matplotlib.pyplot as plt
import numpy as np
import cv2
import glob
import os
import sys
from PIL import Image
def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	s = ssim(imageA, imageB)
	return (m,s)

print("\nZac Conley")
print("A07 - match")
print("compares emojis and finds closest matches")

args = {} #command line arguments
for arg in sys.argv[1:]:
    k,v = arg.split('=')
    args[k] = v
folder=str("/"+args["folder"]+"/") #saves folder name
path = os.path.dirname(os.path.abspath(__file__)) + folder #sets path to emoji folder
originalpath=path+args["image"] #saves image path
original = cv2.imread(originalpath) # convert pic

diff=9223372036854775807 #max int for mse
diffs=0 #0 for ssim
# convert the image to grayscale
original = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY) 

image_list = [] # fetches all emojis in folder
for filename in glob.glob(path+"*.png"): 
	image_list.append(filename)

ans=original #have to have these to avoid error
anss=original
for x in image_list: # for every emoji
	xpath=x #save path
	if (open(originalpath,"rb").read() != open(xpath,"rb").read()): # make sure new emoji is not the same as the original
		x=cv2.imread(x) # convert emoji
		if(original.shape[0]==x.shape[0] and original.shape[1]==x.shape[1]): #makes sure emojis are same size
			x = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY) #makes greyscale
			m,s=compare_images(original, x, "Original vs. Original") # compares images
			if (m<diff): #finds smallest mse
				diff=m
				ans=x
				anspath=xpath
			if (s>diffs): #finds largest ssim
				diffs=s
				anss=x
				ansspath=xpath

# initialize the figure
fig = plt.figure("Most Similar Images")
original=Image.open(originalpath)
ans=Image.open(anspath) # displays the closest images
anss=Image.open(ansspath)
images = ("Original", original),  ("Closest (MSE)", ans),("Closest (SSIM)",anss)

# loop over the images
for (i, (name, image)) in enumerate(images):
	# show the image
	ax = fig.add_subplot(1, 3, i + 1)
	ax.set_title(name)
	plt.imshow(image, cmap = plt.cm.gray)
	plt.axis("off")
plt.show()
