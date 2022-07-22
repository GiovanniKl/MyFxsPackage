import os
import myfxs as mfs
from PIL import Image


def imresiz():
    # This script resizes pics to whatever (reasonable, e.g. not 0) scale you
    # want.
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
                    print("No images found, try different folder or add extension "+
                          "to list in the script.")
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


if __name__ == "__main__":
    imresiz()
