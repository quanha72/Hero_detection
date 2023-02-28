# Hero_detection
## Install
To use this repo you have to install the following packages :
- selenium
- opencv
- Numpy
- Pandas
- Matplotlib
- requests
- PIL
## Run the code
### hero icon crawling
for using the code, you have to adjust some following line in heros_crawler.py to run on your environment
- selenium path : line 14 you have to replace the driver path where is on your computer, if does not have, you can download chrome driver from this link and paste to the code https://chromedriver.chromium.org/
After running this code, the folder ./hero_icons will appear for containing all of hero icons which was crawled previously.

### hero detection
After collected hero icon using for template images, you can run file hero_detection to detect all of input images from provided test_images folder to print the result in output.txt file.
