import os
import myfxs as mfs
from PIL import Image


def imresiz():
    """This script resizes pics to whatever (reasonable, e.g. not 0)
    scale you want in interactive, console-text-input way.
    """
    mfs.prin("Welcome to Image Resizer!")
    exts = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".mpeg"]
    do = True
    while do:
        do0 = True
        while do0:
            try:
                pat = input("Gimme a path to image folder (empty for " +
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
                    print("No images found, try different folder or add " +
                          "extension to list in the script.")
                    raise OSError
                do0 = False
            except OSError:
                print("Wrong path format, please try again.")
        do0 = True
        while do0:
            resize_inds = input("Enter index (or list of indices in []) of" +
                                " pictures you want to resize " +
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
                    print("Some indices are larger than expected! Choose " +
                          "only from displayed values.")
                    raise SyntaxError
            except (SyntaxError, ValueError, NameError):
                print("Wrong format, please enter integers or list of " +
                      "integers.")
        do0, scalall = True, False
        while do0:
            scale = input("Enter new scaling parameter for all images or each" +
                          " image (as a list): ")
            try:
                if type(eval(scale)) == list:
                    scal = eval(scale)
                    if all([isinstance(i, (float, int)) for i in scal]):
                        do0 = False
                elif type(eval("["+scale+"]")) == list:
                    scal = eval("["+scale+"]")
                    if all([isinstance(i, (float, int)) for i in scal]):
                        do0 = False
                    if len(scal) == 1:
                        scalall = True
                if len(resiz_inds) != len(scal) and len(scal) != 1:
                    print("Wrong size of scaling parameter list (must be " +
                          "same size list as list of image indices or float).")
                    do0 = True
                    raise SyntaxError
            except (SyntaxError, ValueError, NameError):
                print("Wrong format, please enter integers or list of " +
                      "integers.")
        do0 = True
        while do0:
            sf = input("Save to a new folder? (y/n): ")
            if sf == "y" or sf == "Y":
                sfn = input("Enter folder name: ")
                pats = os.path.join(pat, sfn)
                try:
                    os.mkdir(pats)
                    do0 = False
                except FileExistsError:
                    print("Folder with this name already exists.")
                    do1 = True
                    while do1:
                        uex = input("Do you still want to continue? You risk "
                                    +"overwriting of existing images. (y/n): ")
                        if uex == "y" or uex == "Y":
                            do1, do0 = False, False
                            pass
                        elif uex == "n" or uex == "N":
                            print("You will be asked again.")
                            do1, do0 = False, True
                        else:
                            print("Wrong input format, please try again.")
            elif sf == "n" or sf == "N":
                pats = pat
                do0 = False
            else:
                print("Wrong input format, please try again.")
        for ii, i in enumerate(resiz_inds):
            if scalall:
                j = 0
            else:
                j = i
            im = Image.open(os.path.join(pat, ims[i]))
            im = im.resize((round(im.width*scal[j]), round(im.height*scal[j])))
            im.save(os.path.join(pats, ims[i][:ims[i].rfind(".")] +
                                 "_sc{}".format(scal[j]).replace(".", "p") +
                                 ims[i][ims[i].rfind("."):]))
            im.close()
            print(f"Saved {ii+1}/{len(resiz_inds)}")
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
           align="center center", scale="fitL",
           scaling_filter=Image.Resampling.BOX):
    """Joins given images into a predefined rectangular grid and saves
    the final image.  Favourable format is PNG, compatibility with other
    images is not guaranteed. This may change in future releases.
    impaths - list of paths (strings) to every image.
    spath - path string to save the final image.
    poses - 2-d array (or list of lists) with positions of each image,
        use 0 where no image will be located and index images from 1.
    padding - int, number of pixels of padding around each image.
    box - 2-tuple of int values of size of each position, default are
        largest dimensions of all images.
    bg - background color hex string in "#rrggbbaa" format.
    align - location of image in its box, same as in matplotlib legend
        loc.
    scale - method to scale images, one of {"fit", "fitL", "stretch"}.
        "fit" - image will be scaled with preserved aspect ratio to fit
            the box (smaller images upscaled, larger downscaled).
        "fitL" - same as "fit" but images smaller than box will not be
            scaled.
        "stretch" - images will be stretched to the size of box.
    scaling_filter - resampling filter used for scaling, valid
        resampling filters are: NEAREST, BOX, BILINEAR, HAMMING,
        BICUBIC, LANCZOS (ordered in increasing quality, decr.
        performance).
    """
    ims, size = [Image.open(i) for i in impaths], [0, 0]
    if box is None:
        for i in range(len(impaths)):
            if ims[i].size[0] > size[0]:
                size[0] = ims[i].size[0]
            if ims[i].size[1] > size[1]:
                size[1] = ims[i].size[1]
    else:
        size = list(box)
    if scale == "fit":
        for i in range(len(impaths)):
            if ims[i].size[0] == size[0] and ims[i].size[1] == size[1]:
                continue
            elif ims[i].size[0]/ims[i].size[1] > size[0]/size[1]:
                ims[i] = ims[i].resize((size[0], int(size[0]*ims[i].size[1]
                                                     // ims[i].size[0])),
                                       resample=scaling_filter)
            else:
                ims[i] = ims[i].resize((int(size[1]*ims[i].size[0]
                                            // ims[i].size[1]), size[1]),
                                       resample=scaling_filter)
    elif scale == "fitL":
        for i in range(len(impaths)):
            if ims[i].size[0] == size[0] and ims[i].size[1] == size[1]:
                continue
            elif (ims[i].size[0]/ims[i].size[1] >= size[0]/size[1] and
                ims[i].size[1] > size[1]):
                ims[i] = ims[i].resize((size[0], int(size[0]*ims[i].size[1]
                                                     // ims[i].size[0])),
                                       resample=scaling_filter)
            elif (ims[i].size[0]/ims[i].size[1] <= size[0]/size[1] and
                ims[i].size[0] > size[0]):
                ims[i] = ims[i].resize((int(size[1]*ims[i].size[0]
                                            // ims[i].size[1]), size[1]),
                                       resample=scaling_filter)
    elif scale == "reshape":
        for i in range(len(impaths)):
            if ims[i].size[0] != size[0] or ims[i].size[1] != size[1]:
                ims[i] = ims[i].resize(size, resample=scaling_filter)
    else:
        raise Exception(f"Wrong scale value: {scale}")
    grid = (len(poses), len(poses[0]))
    fullsize = (grid[1]*(size[0]+padding*2), grid[0]*(size[1]+padding*2))
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
    for i in ims:  # close all used images
        i.close()


def getboxpos(size, imsize, align):
    """Calculates position relative to the inner frame of the image's
    position.  Used in the imjoin() function.
    """
    if size == imsize:
        return 0, 0
    elif align == "upper left":
        return 0, 0
    elif align == "center left":
        return 0, (size[1] - imsize[1]) // 2
    elif align == "lower left":
        return 0, size[1] - imsize[1]
    elif align == "upper center":
        return (size[0] - imsize[0]) // 2, 0
    elif align == "center center":
        return (size[0] - imsize[0]) // 2, (size[1] - imsize[1]) // 2
    elif align == "lower center":
        return (size[0] - imsize[0]) // 2, size[1] - imsize[1]
    elif align == "upper right":
        return size[0] - imsize[0], 0
    elif align == "center right":
        return size[0] - imsize[0], (size[1] - imsize[1]) // 2
    elif align == "lower right":
        return size[0] - imsize[0], size[1] - imsize[1]
    else:
        raise Exception("The align argument in getboxpos() has wrong format.")


def pic2text(impath, spath=None, iscale=1, nchars=2, chars=None, maxwidth=None,
             style="default", reverse=False):
    """Function that converts image to text. Works best with monospaced fonts.
    impath - string, path to image.
    spath - string or None, string is a path to final .txt file (with
        extension), None signifies the image to be printed in the shell.
    iscale - int or 2-tuple, inverse scale of the final image,
        (wf,hf) = (wi,hi)//iscale.
    nchars - int, number of different characters to use, equals to number of
        colors to be recognized. Can be any integer from 2 to 10 (incl.),
        except for styles having a number at the end of its name, e.g.
        "extended68" has a maximum of 68 characters.
    chars - str or None, str should contain custom characters to map the colors
        of the image. If given, len(chars) overwrites nchars (len(chars) can be
        larger than 10).
    maxwidth - int or None, maximum width of the final image in pixels.
        If given, the maxwidth overwrites the iscale parameter (useful for
        including text-images e.g. in code).
    style - string, specifies the char-map theme. Available options are:
        "default", "hi-contrast", "numbers", "balanced", or "extended68".
    reverse - bool. If true, reverses the mapping of the image. Default mapping
        starts with " " (blankspace) as white/light color and ends with "W" as
        black/dark color.
    """
    default = ("", " ", " o", " io", " ioW", " ioeW", " .ioeW", " .:ioeW",
               " .:ioeHW", " .:ioebHW", " .:ioebHBW")
    hicont = ("", " ", " W", "  W", "  WW", "  oWW", "  :oWW", "  .:oWW",
              "  .:oWWW", "   .:oWWW", "   .:ioWWW")
    nums = ("", "0", "01", "012", "0123", "01234", "012345", "0123456",
            "01234567", "012345678", "0123456789")
    balanced = ("", " ", " &", " /&", " ,/&", " ,*/&", " ,*/#&", " ,*/(#&",
                " .,*/(#&", " .,*/(#%&", " .,*/(#%&@")

    def gen_map_from_chars(_chars):
        """Create a character map for all possible lengths from an array
        of characters.
        """
        arr = [_chars]
        for i in range(len(_chars)):
            ind = i % len(arr[i]) + 1  # continuously remove every second char
            arr.append(arr[i][:ind] + arr[i][ind+1:])
            if len(arr[-1]) == len(arr[-2]):
                arr[-1] = arr[-1][:-1]  # small fix
        return tuple(arr[::-1])  # tuple to protect integrity of the char. map

    extended68 = gen_map_from_chars(' .`^",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczX'
                                    + 'YUJCLQ0OZmwqpdbkhao*#MW&8%B@$')
    
    styles = {"default": default, "hi-contrast": hicont, "numbers": nums,
              "balanced": balanced, "extended68": extended68}
    if chars is None:
        maps = styles[style]
    else:
        maps, nchars = [chars]*10, len(chars)
    im = Image.open(impath)
    size = im.size
    if type(maxwidth) == int:
        w, h = maxwidth, int(size[1]//(size[0]/maxwidth*2))
    elif type(iscale) == int:
        w, h = size[0]//iscale, size[1]//(iscale*2)
    elif type(iscale) == tuple:
        w, h = size[0]//iscale[0], size[1]//iscale[1]
    else:
        raise Exception("The iscale parameter has unsupported format!")
    im = im.resize((w, h)).quantize(nchars).convert("L")
    # print(im.getcolors())
    mappin, colors = dict(), im.getcolors()
    if len(colors) < nchars:
        nchars = len(colors)
    if reverse:
        for i in range(nchars):
            mappin[colors[i][1]] = nchars-1-i
    else:
        for i in range(nchars):
            mappin[colors[i][1]] = i
    # im.show()
    if spath is None:
        for j in range(h):
            st = ""
            for i in range(w):
                st += maps[nchars][mappin[im.getpixel((i, j))]]
            print(st)
    else:
        with open(spath, "w+") as file:
            for j in range(h):
                for i in range(w):
                    file.write(maps[nchars][mappin[im.getpixel((i, j))]])
                file.write("\n")
    im.close()
