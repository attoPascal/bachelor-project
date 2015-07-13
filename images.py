from __future__ import print_function, division
import os
import cv2
import numpy as np

RESIZE_WIDTH = 30
RESIZE_HEIGHT = 50
WHITE = [255, 255, 255]

def get_grayscale_picture(path):
    return cv2.imread(path, 0)

def resize_with_padding(image, width, height):
    ratio = width / height

    pic_height = image.shape[0]
    pic_width = image.shape[1]
    pic_ratio = pic_width / pic_height

    if pic_ratio < ratio:
        new_height = height
        new_width = int(round(height * pic_ratio))
        padding_top = 0
        padding_bottom = 0
        padding_left = int((width - new_width) / 2)
        padding_right = int(round((width - new_width) / 2))
    else:
        new_width = width
        new_height = int(round(width / pic_ratio))
        padding_top = int((height - new_height) / 2)
        padding_bottom = int(round((height - new_height) / 2))
        padding_left = 0
        padding_right = 0

    resized = cv2.resize(image, (new_width, new_height), interpolation = cv2.INTER_AREA)
    padded = cv2.copyMakeBorder(resized, padding_top, padding_bottom,
        padding_left, padding_right, cv2.BORDER_CONSTANT, value = [255, 255, 255])
    return padded

def resize_images(inputdir, outputdir, width = RESIZE_WIDTH, height = RESIZE_HEIGHT):
    for filename in os.listdir(inputdir):
        inputpath = inputdir + filename
        outputpath = outputdir + filename
        
        image = get_grayscale_picture(inputpath)
        if image != None:
            resized_image = resize_with_padding(image, width, height)
            cv2.imwrite(outputpath, resized_image)

def rotate_image(image, angle):
    rows, cols = image.shape
    matrix = cv2.getRotationMatrix2D((cols/2,rows/2), angle, 1)
    result = cv2.warpAffine(image, matrix, (cols, rows), borderMode = cv2.BORDER_CONSTANT, borderValue = WHITE)
    return result

def shear_image(image, ratio):
    rows, cols = image.shape
    offset = int(cols*ratio)

    pts1 = np.float32([[0, 0], [cols, 0], [0, rows]]) # top left, bottom left, top right
    pts2 = np.float32([[offset, 0], [cols+offset, 0], [-offset, rows]]) # slanted right

    matrix = cv2.getAffineTransform(pts1,pts2)
    result = cv2.warpAffine(image, matrix, (cols,rows), borderMode = cv2.BORDER_CONSTANT, borderValue = WHITE)
    return result

def add_noise(image, amount = 0.01, salt_ratio = 0.5):
    rows, cols = image.shape
    result = image.copy()

    # pepper mode
    num_pepper = np.ceil(amount* image.size * (1. - salt_ratio))
    coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
    result[coords] = 0

    # salt mode
    num_salt = np.ceil(amount * image.size * salt_ratio)
    coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
    result[coords] = 255

    return result

def get_transformed_filenames(filename):
    transformed_filenames = []
    name, ext = os.path.splitext(filename)
    transformed_filenames.append(name + "-trans-rot1" + ext)
    transformed_filenames.append(name + "-trans-rot2" + ext)
    transformed_filenames.append(name + "-trans-rot3" + ext)
    transformed_filenames.append(name + "-trans-rot4" + ext)
    transformed_filenames.append(name + "-trans-shear1" + ext)
    transformed_filenames.append(name + "-trans-shear2" + ext)
    transformed_filenames.append(name + "-trans-shear3" + ext)
    transformed_filenames.append(name + "-trans-shear4" + ext)
    transformed_filenames.append(name + "-trans-noise1" + ext)
    transformed_filenames.append(name + "-trans-noise2" + ext)
    transformed_filenames.append(name + "-trans-noise3" + ext)
    transformed_filenames.append(name + "-trans-noise4" + ext)
    return transformed_filenames

def main():
    inputdir = "./pics/originals/"
    outputdir = "./pics/resized/"
    transformdir = "./pics/transformed/"
    resize_images(inputdir, outputdir)
    print("originals resized")

    for filename in os.listdir(inputdir):
        inputpath = inputdir + filename
        
        image = get_grayscale_picture(inputpath)
        if image != None:
            rot1 = rotate_image(image, -2)
            rot2 = rotate_image(image, -1)
            rot3 = rotate_image(image, 1)
            rot4 = rotate_image(image, 2)
            shear1 = shear_image(image, 0.1)
            shear2 = shear_image(image, 0.2)
            shear3 = shear_image(image, -0.1)
            shear4 = shear_image(image, -0.2)
            noise1 = add_noise(image, 0.05)
            noise2 = add_noise(image, 0.1)
            noise3 = add_noise(image, 0.2, salt_ratio = 0.9)
            noise4 = add_noise(image, 0.5, salt_ratio = 1.0)

            name, ext = os.path.splitext(filename)
            cv2.imwrite(transformdir + name + "-trans-rot1" + ext, rot1)
            cv2.imwrite(transformdir + name + "-trans-rot2" + ext, rot2)
            cv2.imwrite(transformdir + name + "-trans-rot3" + ext, rot3)
            cv2.imwrite(transformdir + name + "-trans-rot4" + ext, rot4)
            cv2.imwrite(transformdir + name + "-trans-shear1" + ext, shear1)
            cv2.imwrite(transformdir + name + "-trans-shear2" + ext, shear2)
            cv2.imwrite(transformdir + name + "-trans-shear3" + ext, shear3)
            cv2.imwrite(transformdir + name + "-trans-shear4" + ext, shear4)
            cv2.imwrite(transformdir + name + "-trans-noise1" + ext, noise1)
            cv2.imwrite(transformdir + name + "-trans-noise2" + ext, noise2)
            cv2.imwrite(transformdir + name + "-trans-noise3" + ext, noise3)
            cv2.imwrite(transformdir + name + "-trans-noise4" + ext, noise4)

    print("originals transformed")
    resize_images(transformdir, outputdir)
    print("transformed images resized")

if __name__ == '__main__':
    main()




