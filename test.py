# import cv2
# from matplotlib import pyplot as plt
# import os
#
# # Load the two images
# # input_gray = cv2.imread('/content/Ahri_278220660753197_round6_Ahri_06-02-2021.mp4_10_2.jpg', cv2.IMREAD_GRAYSCALE)
# def rightside_removing(image_path):
#     image = cv2.imread(image_path)
#     height, width, channels = image.shape
#     cropped_img = image[0:height , 0:(int(width/4)+1)]
#     return cropped_img
# img1 = rightside_removing('test_data/test_images/Akali_9Aa4KRvaLFA_round3_Fizz_05-19-2021.mp4_65_1.jpg')
# hero_names = []
# list_goodmatchs = []
# for img in os.listdir('./hero_icons'):
#     img2 = cv2.imread("./hero_icons/"+img)
#
#     input_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#     template_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
#
#     # Detect SIFT keypoints and descriptors in the images
#     sift = cv2.SIFT_create()
#     keypoints1, descriptors1 = sift.detectAndCompute(input_gray, None)
#     keypoints2, descriptors2 = sift.detectAndCompute(template_gray, None)
#
#     # Use the BFMatcher to find the best matches between the descriptors
#     # bf = cv2.BFMatcher()
#     # matches = bf.knnMatch(descriptors1, descriptors2, k=2)
#     FLANN_INDEX_KDTREE = 0
#     index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
#     search_params = dict(checks=50)
#     flann = cv2.FlannBasedMatcher(index_params, search_params)
#
#     # Use the FLANN-based Matcher to find the best matches between the descriptors
#     matches = flann.knnMatch(descriptors1, descriptors2, k=2)
#     # Filter the matches using the Lowe's ratio test
#     good_matches = []
#     for m, n in matches:
#         if m.distance < 0.8 * n.distance:
#             good_matches.append(m)
#     hero_name = img.split('.')[0]
#     hero_names.append(hero_name)
#     list_goodmatchs.append(len(good_matches))
#     # Define the threshold
#     threshold = 5
#     # Check the number of matches
#     if len(good_matches) >= threshold:
#         print("Good match found.")
#     else:
#         print("No good match found.")
#
#
#     # Draw the matches on the images
#     img_matches = cv2.drawMatches(input_gray, keypoints1, template_gray, keypoints2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
#
#     # Display the results
#     plt.figure(figsize = (20,10))
#     plt.imshow(img_matches)
#     cv2.imwrite('./test/'+img,img_matches)
#
# max_goodmatch = max(list_goodmatchs)
# max_index = list_goodmatchs.index(max_goodmatch)
#
# print(max_index)
# print(hero_names[max_index])
# from IPython.display import display
import pandas as pd
with open('output.txt', 'r') as f:
    predictions = [line.rstrip().split('\t') for line in f]
with open('test_data/test.txt', 'r') as f2:
    gt = [line.rstrip().split('\t') for line in f2]

predictions = pd.DataFrame(predictions,columns = ["file_name","prediction"])
gt = pd.DataFrame(gt, columns=["file_name","gt"])
df_all_rows = pd.merge(predictions, gt, how='inner',on = 'file_name')
print(len(df_all_rows.query('prediction ==  gt')))
