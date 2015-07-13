from __future__ import print_function, division
import os
import numpy as np
from pybrain.datasets import ClassificationDataSet

import images, classes

PIXELS = images.RESIZE_WIDTH * images.RESIZE_HEIGHT

def get_data(dirname, files, classifier_func, m = PIXELS):
    n = len(files)

    X = np.zeros(shape = (n, m))
    y = np.zeros(shape = (n, 1))

    for (i, filename) in enumerate(files):
        image = images.get_grayscale_picture(dirname + filename)
        klass = classifier_func(filename)
            
        X[i] = np.ravel(image / 255)
        y[i] = klass

    return (X, y)

def old_get_data(inputdir, m = PIXELS):
    files = [f for f in os.listdir(inputdir) if f.endswith(".png")]
    n = len(files)

    X = np.zeros(shape = (n, m))
    y = np.zeros(shape = (n, 1))

    for (i, filename) in enumerate(files):
        image = images.get_grayscale_picture(inputdir + filename)
        klass = get_symbol_class(filename)
            
        X[i] = np.ravel(image / 255)
        y[i] = klass

    return (X, y)

def get_notes(inputdir, m = PIXELS):
    files = [f for f in os.listdir(inputdir) if f.startswith("note")]
    n = len(files)

    X = np.zeros(shape = (n, m))
    y = np.zeros(shape = (n, 1))

    for (i, filename) in enumerate(files):
        image = images.get_grayscale_picture(inputdir + filename)
        klass = classes.get_pitch_class(filename)
            
        X[i] = np.ravel(image / 255)
        y[i] = klass

    return (X, y)

def get_quarters_and_eights(inputdir, m = PIXELS):
    files = [f for f in os.listdir(inputdir) if (f.startswith("note") and ("quarter" in f or "eighth" in f))]
    n = len(files)

    X = np.zeros(shape = (n, m))
    y = np.zeros(shape = (n, 1))

    for (i, filename) in enumerate(files):
        image = images.get_grayscale_picture(inputdir + filename)
        klass = 0 if ("quarter" in filename) else 1
            
        X[i] = np.ravel(image / 255)
        y[i] = klass

    return (X, y)

def get_datasets(inputdir, dstype = "all", proportion = 0.3):
    untransformed_files = [f for f in os.listdir(inputdir) if "trans" not in f]

    if dstype == "symbol":
        files = [f for f in untransformed_files if f.endswith(".png")]
        classifier_func = classes.get_symbol_class
        num_classes = 2
    elif dstype == "pitch":
        files = [f for f in untransformed_files if "note" in f]
        classifier_func = classes.get_pitch_class
        num_classes = 18
    elif dstype == "note_duration":
        files = [f for f in untransformed_files if "note" in f and "other" not in f]
        classifier_func = classes.get_duration_class
        num_classes = 5
    elif dstype == "rest_duration":
        files = [f for f in untransformed_files if "rest" in f]
        classifier_func = classes.get_duration_class
        num_classes = 5
    elif dstype == "quarters_and_eighths":
        files = [f for f in untransformed_files if "note-quarter" in f or "note-eighth" in f]
        classifier_func = classes.quarter_or_eighth
        num_classes = 2
    else:
        files = []
        classifier_func = classes.get_symbol_class
        num_classes = 18

    random_indices = np.random.permutation(len(files))
    sep = int(len(files) * proportion)

    train_indices = random_indices[sep:]
    test_indices  = random_indices[:sep]

    train_files = [f for i, f in enumerate(files) if i in train_indices]
    test_files  = [f for i, f in enumerate(files) if i in test_indices]

    transformed = []
    for f in train_files:
        transformed += images.get_transformed_filenames(f)

    train_files += transformed

    Xtrain, ytrain = get_data(inputdir, train_files, classifier_func)
    Xtest,  ytest  = get_data(inputdir, test_files,  classifier_func)

    train_set = ClassificationDataSet(Xtrain.shape[1], nb_classes = num_classes)
    for i in range(len(Xtrain)):
        train_set.addSample(Xtrain[i], ytrain[i])

    test_set = ClassificationDataSet(Xtest.shape[1], nb_classes = num_classes)
    for i in range(len(Xtest)):
        test_set.addSample(Xtest[i], ytest[i])

    return train_set, test_set


def main():
    get_datasets("pics/sample/")

if __name__ == '__main__':
    main()
