import os
import glob
from PIL import Image

def flatten_list(_2d_list):
    flat_list = []
    # Iterate through the outer list
    for element in _2d_list:
        if type(element) is list:
            # If the element is of type list, iterate through the sublist
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

def convert(list):
      
    # Converting integer list to string list
    s = [str(i) for i in list]
      
    # Join list items using join()
    res = int("".join(s))
      
    return(res)

def sortstrings_numerically(strings,sort=True,drop_ints=True):
  #Return tuple, matching string to int
  ints = []
  for s in strings:
    ints.append([int(x) for x in s if x.isdigit()])
  int_new = []
  for l in ints:
    int_new.append(convert(l))
  tups = [[]]
  for i in range(len(strings)):
    tups.append([strings[i],int_new[i]])
  #tups.pop(0)
  tups = tups[1:]
  if sort:
    tups = sorted(tups,key=lambda x: x[1])
  else:
    tups = tups
  if drop_ints:
    for j in tups:
      del j[1]
    tups = flatten_list(tups)
  return tups

#Functions
def make_image_gif(folder,root_name,duration=100,delete_images=True):
  #os.chdir(folder)
  print(os.getcwd())
  fp_in = f'{root_name}*.jpg'
  fp_out = f'{root_name}.gif'
  #print(folder+fp_in)

  imgs = glob.glob(folder+fp_in)
  imgs = sortstrings_numerically(imgs)
  frames = [Image.open(image) for image in imgs]
  #print(folder+fp_in,frames)
  img = frames[0]
  img.save(fp=fp_out,format='GIF',append_images=frames,save_all=True,duration=duration,loop=0)
  os.system(f'mv {root_name}.gif {folder}')
  if delete_images:
    os.system(f'rm {folder}{root_name}*.jpg')