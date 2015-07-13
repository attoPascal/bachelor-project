from __future__ import print_function
import os, sys

def get_symbol_class(filename):
    return 1 if "rest" in filename else 0

def get_pitch_class(filename):
    keywords = filename.split("-")
    if "note" in filename:
        pitch = keywords[2]
        try:
            return {
                "a": 0,
                "h": 1,
                "c1": 2,
                "d1": 3,
                "e1": 4,
                "f1": 5,
                "g1": 6,
                "a1": 7,
                "h1": 8,
                "c2": 9,
                "d2": 10,
                "e2": 11,
                "f2": 12,
                "g2": 13,
                "a2": 14,
                "h2": 15,
                "c3": 16,
                "other": 17
            }[pitch]
        except:
            print(pitch)
            sys.exit()
    else:
        return None

def get_duration_class(filename):
    keywords = filename.split("-")
    duration = keywords[1]
    try:
        return {
            "whole": 0,
            "half": 1,
            "quarter": 2,
            "eighth": 3,
            "sixteenth": 4,
            "other": 5
        }[duration]
    except:
        print(duration)
        sys.exit()

def quarter_or_eighth(filename):
    return 0 if ("quarter" in filename) else 1

def get_class_array(filenames, function):
    classes = []
    for filename in filenames:
        classes.append(function(filename))
    return classes

def main():
    pass

if __name__ == '__main__':
    main()