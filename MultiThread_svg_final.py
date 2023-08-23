import os
import csv
import cairosvg
from PIL import Image
from tqdm import tqdm
from glob import glob
from enum import Enum
import aspose.words as aw
import threading
import argparse

doc = aw.Document()
builder = aw.DocumentBuilder(doc)
saveOptions = aw.saving.ImageSaveOptions(aw.SaveFormat.SVG)

# This class fixes file extention name
class Ext(Enum):
    svg = '.svg'
    png = '.png'

# This function resizes & pads img before svg2png
def resize(img, max_size):
    shape = img.size
    if max(shape) > max_size:
        ratio = max_size/max(shape)
        newshape = int(shape[0]*ratio), int(shape[1]*ratio)
        img = img.resize(newshape)
    return img

# This function changes imgs to png format through resize, pad and change svg format
def work(imgs, src_path, dst_path, size_for_resize, size_for_png, remove_svg):
    for img in tqdm(imgs):
        # setting up path
        svg_path = os.path.splitext(img.replace(src_path, dst_path))[0] + Ext.svg.value
        output_path = svg_path.replace(Ext.svg.value, Ext.png.value)

        if not (os.path.exists(output_path) and os.path.exists(svg_path)):
            # resize imgs before svg2png
            resized_path = output_path
            os.makedirs(os.path.dirname(svg_path), exist_ok=True)
            image = Image.open(img)
            resized_image = resize(image, size_for_resize)
            resized_image.save(resized_path)

            # Change resized imgs to png imgs  
            try:
                shape = builder.insert_image(resized_path)
                shape.get_shape_renderer().save(svg_path, saveOptions) # save svg imgs
                cairosvg.svg2png(url=svg_path,write_to=output_path,output_width=size_for_png,output_height=size_for_png) # save png imgs
                if remove_svg:
                    os.remove(svg_path)

            # Save image paths with errors (that are broken)
            except:
                with open(f'{output_path}.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([img])

def main(args):
    output_path = args.dst_path
    src_imgs = [i for i in glob(os.path.join(args.src_path, '**/*'), recursive=True) if os.path.isfile(i)]
    
    print('number of imgs in src_dir: ', len(src_imgs))
    
    split_num = args.multi_thread_num
    
    for i in range(split_num):      
        # Split imgs indexes before input into multi_thread
        tmp = src_imgs[(len(src_imgs)//split_num)*i:(len(src_imgs)//split_num)*(i+1)]
        if i == split_num-1:
            tmp = src_imgs[(len(src_imgs)//split_num)*i:]
            
        # Work multi_thread
        th = threading.Thread(target=work, name=f'thread_{i}', args=(tmp, args.src_path, args.dst_path, args.size_for_resize, args.size_for_png, args.remove_svg))
        th.start()
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src-path', default='/home/ubuntu/workspace/dataset/test_dataset_svg/spec69_src', type=str, help='type input imgs path')
    parser.add_argument('--dst-path', default='/home/ubuntu/workspace/dataset/test_dataset_svg/seunghoon_test', type=str, help='type output imgs path')  
    parser.add_argument('--size-for-resize', default=1280, type=int, help="size for resizing input imgs before svg2png")  
    parser.add_argument('--size-for-png', default=224, type=int, help="size for resizing png imgs" )
    parser.add_argument('--remove-svg', default=False, type=bool, help='type true, if you want to remove svg files')  
    parser.add_argument('--multi-thread-num', default=32, type=int)  
    args = parser.parse_args()
    
    main(args)
