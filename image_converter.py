import argparse
import os
import re
from threading import Thread

from wand.image import Image
from wand.version import formats

#
# Constants
#
CONVERTED_DIR_NAME = "converted_images"

#
# Globals
#
threads = []

def convert_img(src, input, output, directory):
    with Image(filename=f'{directory}/{src}') as original:
        converted_img = original.convert(output)
        
    src = src.replace(input, f'.{output}')

    converted_img.save(filename=f'{directory}/converted_images/{src}')
        
        

def convert_dir(directory, input, output):
    all = os.listdir(directory)
    folders = [f for f in all if os.path.isdir(directory+'/'+f) and CONVERTED_DIR_NAME not in f] 
    
    # recursively go into all directories
    for f in folders:
        print(f'Converting contents of {f}!')
        convert_dir(f'{directory}/{f}', input, output)

    files = [f for f in all if os.path.isfile(directory+'/'+f) and re.search(f"\w+\{input}", f)] 
    
    if not files:
        return
    
    if directory[-1] == "/":
        out_dir = directory + CONVERTED_DIR_NAME
    else:
        out_dir = directory + "/" + CONVERTED_DIR_NAME
        
    try:
        os.mkdir(out_dir)
    except OSError:
        pass
    

    for f in files:
        t = Thread(target=convert_img, args=(f, input, output, directory))
        t.start()
        threads.append(t)


if __name__ == "__main__":
    
    supported = formats('*')


    parser = argparse.ArgumentParser()
    
    parser.add_argument("-d", "--directory", type=str, required=True)
    parser.add_argument("-i", "--input", type=str, required=True)
    parser.add_argument("-o", "--output", type=str, required=True)
    
    args = parser.parse_args()
    
    input = args.input if '.' in args.input else '.' + args.input
    input = input.upper()
    
    if input.replace('.', '') not in supported:
        raise ValueError('Unsupported input file format!')
    
    output = (args.output).upper().replace('.', '')
    
    if output not in supported:
        raise ValueError('Unsupported output file format!')
    
    convert_dir(args.directory, input, args.output)
    
    for t in threads:
        t.join()
    
    
