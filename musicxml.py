from __future__ import print_function

TEMPLATE_PATH = "musicxml-template.xml"
OUTPUT_PATH = "xml/"

def get_template(path = TEMPLATE_PATH):
    with open (path, "r") as f:
        return f.read()

def format_template(template, step, octave, duration, divisions = 4, fifths = 0, beats = 4, beat_type = 4, clef_sign = "G", clef_line = 2):
    durations = {
        "sixteenth": 1,
        "eighth":    2,
        "quarter":   4,
        "half":      8,
        "whole":    16
    }
    duration_number = durations[duration] * divisions

    return template.format(_step = step, _octave = octave, _duration = duration_number, _type = duration, _divisions = divisions,
        _fifths = fifths, _beats = beats, _beat_type = beat_type, _sign = clef_sign, _line = clef_line)

def save_file(path, data):
    with open(path, "w") as f:
        f.write(data)

def get_scientific_designation(pitch):
    if len(pitch) == 1:
        return (pitch.upper(), 3)
    elif len(pitch) == 2:
        step = pitch[0].upper()
        octave = int(pitch[1]) + 3
        return (step, octave)

def create_xml_for_note(pitch, duration, path):
    step, octave = get_scientific_designation(pitch)
    xml = format_template(get_template(), step, octave, duration)
    save_file(path, xml)


def main():
    print(format_template(get_template(), "C", 4, "whole"))

if __name__ == '__main__':
    main()
