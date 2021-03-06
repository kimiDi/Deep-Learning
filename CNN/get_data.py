import urllib
import cv2
import os
import numpy as np
import itertools
import Image

pic_num = 1

def load_image(path, link, counter):
    global pic_num
    if pic_num < counter:
        pic_num = counter + 1
    try:
        urllib.urlretrieve(link, path+"/"+str(counter)+".jpg")
        img = cv2.imread(path+"/"+str(counter)+".jpg")
        if img is not None:
            cv2.imwrite(path+"/"+str(counter)+".jpg",img)
            print(counter)
    except Exception as e:
        print(str(e))

def store_raw_images(paths, links):
    global pic_num
    for link, path in zip(links, paths):
        if not os.path.exists(path):
            os.makedirs(path)
        image_urls = str(urllib.urlopen(link).read())
        args = zip(itertools.repeat(path), image_urls.split('\r\n'), itertools.count(pic_num))
        for arg in args:
            load_image(arg[0], arg[1], arg[2])

def is_img_ok(fn):
    try:
        Image.open(fn)
        return True
    except:
        return False
def remove_broken(dir_paths):
    for dir_path in dir_paths:
        for img in os.listdir(dir_path):
            current_image_path = str(dir_path)+'/'+str(img)
            if not is_img_ok(current_image_path):
                os.remove(current_image_path)

def remove_invalid(dir_paths):
    for dir_path in dir_paths:
        for img in os.listdir(dir_path):
            for invalid in os.listdir('invalid'):
                try:
                    current_image_path = str(dir_path)+'/'+str(img)
                    invalid = cv2.imread('invalid/'+str(invalid))
                    question = cv2.imread(current_image_path)
                    if invalid.shape == question.shape and not (np.bitwise_xor(invalid,question).any()):
                        os.remove(current_image_path)
                        break
                except Exception as e:
                    print(str(e))

def main():
    links = [
            'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n01318894', \
            'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n03405725', \
            'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07942152', \
            'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n00021265', \
            'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07690019', \
            'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07865105', \
            'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07697537']

    paths = ['pets', 'furniture', 'people', 'food', 'frankfurter', 'chili-dog', 'hotdog']
    store_raw_images(paths, links)
    remove_broken(paths)
    remove_invalid(paths)

if __name__ == "__main__":
    main()
