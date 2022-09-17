import os
import myfxs as mfs
from PIL import Image


def imresiz():
    '''This script resizes pics to whatever (reasonable, e.g. not 0) scale you
    want in interactive, console-text-input way.'''
    mfs.prin("Welcome to Image Resizer!")
    exts = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".mpeg"]
    do = True
    while do:
        do0 = True
        while do0:
            try:
                pat = input("Gimme a path to image folder (empty for "+
                            "current folder): ")
                if pat == "":
                    pat = os.getcwd()
                lis = os.listdir(pat)
                print("Here is a list of possible images: ")
                count, ims = 0, []
                for i in lis:
                    for j in exts:
                        if i.find(j) != -1:
                            print("[{}]:".format(count), i)
                            count += 1
                            ims.append(i)
                if count == 0:
                    print("No images found, try different folder or add "+
                          "extension to list in the script.")
                    raise OSError
                do0 = False
            except OSError:
                print("Wrong path format, please try again.")
        do0 = True
        while do0:
            resize_inds = input("Enter index (or list of indices in []) of"+
                                " pictures you want to resize "+
                                "(empty for all): ")
            try:
                if resize_inds == "":
                    resiz_inds = [i for i in range(count)]
                    do0 = False
                elif type(eval(resize_inds)) == list:
                    resiz_inds = eval(resize_inds)
                    if all([isinstance(i, int) for i in resiz_inds]):
                        do0 = False
                elif type(eval("["+resize_inds+"]")) == list:
                    resiz_inds = eval("["+resize_inds+"]")
                    if all([isinstance(i, int) for i in resiz_inds]):
                        do0 = False
                else:
                    raise SyntaxError
                if any([i > count for i in resiz_inds]):
                    do0 = True
                    print("Some indices are larger than expected! Choose "+
                          "only from displayed values.")
                    raise SyntaxError
            except (SyntaxError, ValueError, NameError):
                print("Wrong format, please enter integers or list of "+
                      "integers.")
        do0, scalall = True, False
        while do0:
            scale = input("Enter new scaling parameter for all images or each"+
                          " image (as a list): ")
            try:
                if type(eval(scale)) == list:
                    scal = eval(scale)
                    if all([isinstance(i, (float, int)) for i in scal]):
                        do0 = False
                elif type(eval("["+scale+"]")) == list:
                    scal = eval("["+scale+"]")
                    if all([isinstance(i, (float,int)) for i in scal]):
                        do0 = False
                    if len(scal) == 1:
                        scalall = True
                if len(resiz_inds) != len(scal) and len(scal) != 1:
                    print("Wrong size of scaling parameter list (must be "+
                          "same size list as list of image indices or float).")
                    do0 = True
                    raise SyntaxError
            except (SyntaxError, ValueError, NameError):
                print("Wrong format, please enter integers or list of "+
                      "integers.")
        do0 = True
        while do0:
            sf = input("Save to a new folder? (y/n): ")
            if sf == "y" or sf == "Y":
                sfn = input("Enter folder name: ")
                os.mkdir(sfn)
                pats = os.path.join(pat, sfn)
                do0 = False
            elif sf == "n" or sf == "N":
                pats = pat
                do0 = False
            else:
                print("Wrong input format, please try again.")
        for i in resiz_inds:
            if scalall:
                j = 0
            else:
                j = i
            im = Image.open(os.path.join(pat,ims[i]))
            im = im.resize((round(im.width*scal[j]), round(im.height*scal[j])))
            im.save(os.path.join(pats, ims[i][:ims[i].rfind(".")]+
                                 "_sc{}".format(scal[j]).replace(".", "p")+
                                 ims[i][ims[i].rfind("."):]))
            im.close()
        mfs.prin("Finished.")
        # repeating procedure
        do0 = True
        while do0:
            dostop = input("Do you want to do one more procedure? (y/n): ")
            if dostop == "y" or dostop == "Y":
                do0 = False
                mfs.prin("Let's start again!")
            elif dostop == "n" or dostop == "N":
                mfs.prin("See you later!")
                do, do0 = False, False
            else:
                print("Wrong input format, please try again.")


def imjoin(impaths, spath, poses, padding=0, box=None, bg="#ffffff00",
           align="center center"):
    '''Joins given images into a predefined rectangular grid and saves the
    final image. Favourable format is PNG, compatibility with other images
    is not guaranteed. This may change in future releases.
    impaths - list of paths (strings) to every image
    spath - path string to save the final image
    poses - 2-d array (or list of lists) with positions of each image, 
    use 0 where no image will be located and index images from 1
    padding - int, number of pixels of padding around each image
    box - 2-tuple of int values of size of each position, default are largest
    dimensions of all images
    bg - background color hex string in "#rrggbbaa" format
    align - location of image in its box, same as in matplotlib legend loc'''
    ims, size = [Image.open(i) for i in impaths], [0, 0]
    for i in range(len(impaths)):
        if ims[i].size[0] > size[0]:
            size[0] = ims[i].size[0]
        if ims[i].size[1] > size[1]:
            size[1] = ims[i].size[1]
    if box != None:
        if box[0] > size[0]:
            size[0] = box[0]
        if box[1] > size[1]:
            size[1] = box[1]
    grid = (len(poses), len(poses[0]))
    fullsize = (grid[0]*(size[0]+padding*2), grid[1]*(size[1]+padding*2))
    full = Image.new("RGBA", fullsize, color=bg)
    for i in range(grid[0]):  # row
        for j in range(grid[1]):  # column
            if poses[i][j] == 0:
                continue
            else:
                bp = getboxpos(size, ims[poses[i][j]-1].size, align)
                full.paste(ims[poses[i][j]-1],
                           (j*(2*padding+size[0])+padding+bp[0],
                            i*(2*padding+size[1])+padding+bp[1]))
    full.save(spath)
    full.close()


def getboxpos(size, imsize, align):
    '''Calculates position relative to the inner frame of the image's
    position. Used in the imjoin() function.'''
    if size == imsize:
        return (0, 0)
    elif align == "upper left":
        return (0, 0)
    elif align == "center left":
        return (0, (size[1]-imsize[1])//2)
    elif align == "lower left":
        return (0, size[1]-imsize[1])
    elif align == "upper center":
        return ((size[0]-imsize[0])//2, 0)
    elif align == "center center":
        return ((size[0]-imsize[0])//2, (size[1]-imsize[1])//2)
    elif align == "lower center":
        return ((size[0]-imsize[0])//2, size[1]-imsize[1])
    elif align == "upper right":
        return (size[0]-imsize[0], 0)
    elif align == "center right":
        return (size[0]-imsize[0], (size[1]-imsize[1])//2)
    elif align == "lower right":
        return (size[0]-imsize[0], size[1]-imsize[1])
    else:
        raise Exception("The align argument getboxpos() has wrong format.")

