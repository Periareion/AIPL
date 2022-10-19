
import os

def default(default_value, value):
    return default_value if value is None else value

def first_available_filename_number(filename, extension='.png'):
    k = 0
    while os.path.isfile(filename + extension):
        num_str = str(k)
        if k != 0 and filename.endswith(num_str):
            filename = filename[:-len(num_str)]
        k += 1
        filename += str(k)
    return filename + extension