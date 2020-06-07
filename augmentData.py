import numpy as np
np.set_printoptions(suppress=True)
import cv2
from pathlib import Path
import sys
import os


def pixelsWithWeight(imgDims, center, pixelCount):

    # 50 pixels radius around pixel in focus
    cov = [[50, 0], [0, 50]]
    # Create normally distributed pixels to mimic GradCAM visualisation to some extent
    x, y = np.random.multivariate_normal(center, cov, pixelCount).T
    # Convert coordinates to integers
    coords = np.rint(np.c_[x, y])
    # Make sure pixels generated are unique
    coords = np.unique(coords, axis=0)
    # Make sure pixels are within image dimension bounds
    coords = coords[((coords[:, 0] >= 0) & (coords[:, 0] < imgDims[0])) & ((coords[:, 1] >= 0) & (coords[:, 1] < imgDims[1]))]
    # Assign random weights to generated pixels
    pixelWeight = np.round(np.random.rand(coords.shape[0]), 4)

    # Convert 2D coordinates to 1D coordinate and Append pixel weights the resultant array
    coords = np.c_[coords[:, 0]*imgDims[1]+coords[:, 1], pixelWeight]

    # Save coordinates into file
    for rowIter in range(2):
        np.savetxt(imgDataFile, coords[:, rowIter].reshape(1, -1), fmt=("%.4f" if rowIter == 1 else "%d"))

    # return coords

try:
    imgPathInput = sys.argv[1]
    # images = ["2007_000129", "2007_000033", "2007_000762"]
    imageName = os.path.split(imgPathInput)[1].rsplit(".", 1)[0]
    outputCSVPathText = os.path.split(imgPathInput)[0]+"/"

    # Create directory if it doesnt exist
    outputCSVPath = Path(outputCSVPathText).mkdir(parents=True, exist_ok=True)

    img = cv2.imread(imgPathInput)
    imgDims = np.array([img.shape[0], img.shape[1]])

    points = "250"
    total_iterations = img.shape[0]*img.shape[1]
    with open(outputCSVPathText+imageName+".csv", "w") as imgDataFile:
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                pixelsWithWeight(imgDims, [i, j], int(points))
                sys.stdout.write("\r["+str(int((i*img.shape[1]+j)/total_iterations*100)+1)+"% completed]")
                sys.stdout.flush()

    sys.stdout.write("\nGradCAM data for ["+imageName+"] generated in ["+outputCSVPathText+imageName+".csv]\n")
except:
    e = sys.exc_info()[0]
    print("\nInvalid arguments\nUsage: python augmentData.py \"path/to/image.jpg\"")