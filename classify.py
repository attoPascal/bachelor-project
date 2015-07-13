from __future__ import print_function
import sys
import os
import numpy
import images
import musicxml
from pybrain.tools.customxml.networkreader import NetworkReader

class_labels = {
    "symbol":        ["note", "rest"],
    "note_duration": ["whole", "half", "quarter", "eighth", "sixteenth", "other"],
    "pitch":          ["a", "h", "c1", "d1", "e1", "f1", "g1", "a1", "h1", "c2", "d2", "e2", "f2", "g2", "a2", "h2", "c3", "other"]
}

def calculate_probabilities(network_name, input):
    network = NetworkReader.readFrom("networks/" + network_name + ".xml")
    probabilities = network.activate(input).tolist()
    return probabilities

def print_probabilities(probabilities):
    for i, a in enumerate(probabilities):
        print("probability for class {0:2d}: {1:6.4f}".format(i, a))

def predict_class(probabilities, class_dict):
    class_number = probabilities.index(max(probabilities))
    class_name = class_dict[class_number]
    return (class_number, class_name)

def print_class(class_number, class_name):
    print("=> {} (class {})".format(class_name, class_number))

def classify(image, classification_name):
    print("classifying {}:".format(classification_name))
    probabilities = calculate_probabilities(classification_name, image)
    print_probabilities(probabilities)
    class_number, class_name = predict_class(probabilities, class_labels[classification_name])
    print_class(class_number, class_name)
    print()
    return class_name


def main():
    if len(sys.argv) < 2:
        sys.exit("no file passed")

    imgpath = sys.argv[1]
    image = images.get_grayscale_picture(imgpath)
    if image == None:
        sys.exit("could not read image")

    resized = images.resize_with_padding(image, 30, 50)
    flattened = numpy.ravel(resized)

    symbol = classify(flattened, "symbol")

    if symbol == "note":
        note_duration = classify(flattened, "note_duration")
        pitch = classify(flattened, "pitch")
        print(symbol, note_duration, pitch)

        xmlpath = "demo/" + os.path.splitext(os.path.basename(imgpath))[0] + ".xml"
        musicxml.create_xml_for_note(pitch, note_duration, xmlpath)

    elif symbol == "rest":
        rest_duration = classify(flattened, "rest_duration")
        print(symbol, rest_duration)

if __name__ == '__main__':
    main()