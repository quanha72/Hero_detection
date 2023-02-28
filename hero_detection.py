
import cv2
import os
import numpy as np
# import imutils
from matplotlib import pyplot as plt



def get_hero_dict(image_dir = './hero_icons/'):
    histograms = []
    hero_names = []
    for img_path in os.listdir('./hero_icons'):
        img = cv2.imread('./hero_icons/'+img_path)
        hero_name = img_path.split('.')[0]
        # hero_names.append(hero_name)
        #
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        #
        # cv2.normalize(hist, hist)
        #
        # #store to dict of histograms
        # histograms.append(hist)
        hero_names.append(hero_name)
        histograms.append(img)
    return histograms,hero_names

#this function use for keeping just left side of image which contains the needed hero
def rightside_removing(image_path):
    image = cv2.imread(image_path)
    height, width, channels = image.shape
    cropped_img = image[0:height , 0:(int(width/4)+1)]
    return cropped_img

def caculate_similarities(cropped_image):
    cropped_image = cv2.resize(cropped_image, None, fx=0.7, fy=0.7)
    templates, hero_names = get_hero_dict()

    #caculate histogram of cropped image
    input_gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    #caculate similarities
    list_goodmatchs = []
    for i,template in enumerate(templates):
        template = cv2.resize(template, None, fx=1.3, fy=1.3)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # Detect SIFT keypoints and descriptors in the images
        sift = cv2.SIFT_create(nfeatures=1000, contrastThreshold=0.01, edgeThreshold=10)
        keypoints1, descriptors1 = sift.detectAndCompute(input_gray, None)
        keypoints2, descriptors2 = sift.detectAndCompute(template_gray, None)

        # Use the BFMatcher to find the best matches between the descriptors
        # bf = cv2.BFMatcher()
        # matches = bf.knnMatch(descriptors1, descriptors2, k=2)
        FLANN_INDEX_KDTREE = 0
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv2.FlannBasedMatcher(index_params, search_params)

        # Use the FLANN-based Matcher to find the best matches between the descriptors
        matches = flann.knnMatch(descriptors1, descriptors2, k=2)
        # Filter the matches using the Lowe's ratio test
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)
        list_goodmatchs.append(len(good_matches))

        img_matches = cv2.drawMatches(input_gray, keypoints1, template_gray, keypoints2, good_matches, None,
                                      flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

        # Display the results
        # plt.figure(figsize=(20, 10))
        # plt.imshow(img_matches)
        cv2.imwrite('./test/' + hero_names[i] + '.jpg', img_matches)
    result = dict(zip(hero_names,list_goodmatchs))
    max_goodmatchs = max(list_goodmatchs)
    max_index = list_goodmatchs.index(max_goodmatchs)
    return hero_names[max_index]

for input_path in os.listdir('test_data/test_images'):
    cropped = rightside_removing('test_data/test_images/'+input_path)
    # cv2.imwrite('cropped.png',cropped)
    hero_predict = caculate_similarities(cropped)
    with open('output.txt','a') as f:
        f.write(input_path + '\t' + hero_predict + '\n')

with open('output.txt','r') as f:
    lines = [line.rstrip().split('\t') for line in f]


