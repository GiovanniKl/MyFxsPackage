This project includes two packages, both include convenient functions but are separated for performance reasons due to the use of different dependencies. They are MyFxs and MyImages.

# MyFxs Package (`myfxs.py`)
Package of useful functions for Python 3.7, mostly used for experimental data analysis.
Requires following packages to be installed: `matplotlib`, `numpy`.

**Disclaimer:** I did not check the compatibility with newer versions. Everything was written using these module versions: `matplotlib 3.4.3`, `numpy 1.21.6`.

*Warning: Czech words included!*

## List of functions
### `getr2(y, yfit)`
Calculate the coefficient of determination (R squared).

- `y`    numpy-array, list of experimental data.
- `yfit` numpy-array, must be of the same length as `y`, list of fitted values at the same `x` value.

Returns:
- `r2`   float, coefficient of determination (not in percents).

### `zaoknem(x)`
Function for rounding mean and deviation pairs.

- `x` deviation to be rounded.

Returns:
- `x` rounded deviation to one significant digit (except for when the digit (denoted as `d`)  `1 < d < 2.95`, it is rounded to two significant digits).
- `ind` index used in `round(mean, ind)` or `np.round(mean, ind)` to round the mean (denoted `mean`) according to the deviation.

### `makemyfontnice()`
Set all fonts used in `matplotlib` plots to serif type.

### `linab(x, a, b)`
Linear function $y(x) = ax + b$. Used often for fitting and regression purposes.

### `lina(x, a)`
Linear function $y(x) = ax$. Used often for fitting and regression purposes.

### `vypoctinejistotu(xs, nejb=np.zeros(1), quantity="X", units="x", otype="g", out=True)`
Calculate mean and standard deviation from a list of measurements using 95% confidence interval of T distribution.
- `xs` array-like of experimental data (e.g. floats).
- `nejb` array-like (optional) of type B uncertainties (e.g. floats).
- `quantity` string (optional) containing quantity name.
- `units` string (optional) containing units name.
- `otype` string (optional), valid `format_spec` after ":", e.g. `"03.2f"`.
- `out` bool (optional), whether to print results in the terminal (if `False`, previous three arguments are not used).

Returns: 
- `xbar` float, mean value of `xs`.
- `nej` float, standard deviation.

### `prin(t, do=50, o=2, ws=True)`
Print desired text into the shell, centered and filled with asteriscs (*) to the length d, padded with space before and after the text.
-  `t` string, text to print, for best appearance shorter than `d-o-2`.
- `d` int (optional), length of the full row.
- `o` int (optional), minimal offset/padding at the beggining when `len(t) > d-o-2`.
- `ws` bool (optional), padding the text with one whitespace on each side.

### `wmean(nominal_values, weights, calculate_uncertainty=True)`
Function for calculating weighted mean. Can be useful together with `uncertainties` package or when calculating uncertainties, in general. Can calculate coresponding uncertainty `dx`, if weights are given as `w_i = 1/dx_i**2` for each `w_i` in `weights`.
- `nominal_values` array-like of nominal values.
- `weights` array-like of corresponding weights.  Can be a float, but then this function serves as a normal mean (e.g. `numpy.mean()`).
- `calculate_uncertainty` - bool (optional), whether to calculate also the combined uncertainty of nominal_values.

### `altline(x0, y0, r, phi, phiunit="deg")`
Function for calculating end points of a line from its origin given length and angle. (Angle+Length To LINE)
- `x0`, `y0` float, (given_length_unit) line-origin coorinates.
- `r` float, (given_length_unit) line length.
- `phi` float, (phiunit) angle of the line from x axis.
- `phiunit` one of `{"rad", "deg"}`, determines phi unit.


# MyImages Package (`myimages.py`)
Package for image manipulation for Python 3.7, mostly used for batch-processing of images.
Requires following packages to be installed: `os`, `PIL` (`Pillow`), `myfxs` (for dependencies see above).

**Disclaimer:** I did not check the compatibility with newer versions. Everything was written using these module versions: `Pillow 8.1.2`.

## List of functions
### `imresiz()`
Function for user-driven image resizing. All parameters will be asked on the run. This function resizes images and saves them with scale appended to the name.

Parameters (asked on the run) can modify:
- processing folder (possible to choose current folder)
- choosen images from a list (checks for some image formats, not all extensions may be included (you must add the extension to the package script manually or ask me for an update) and not every format may be supported by the `PIL` package, for more details see [PIL documentation](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html))
- scale (one for all specified images or individual)
- whether to save images to a specific new folder
- whether to run another procedure or exit the program

* This function might be improved in the future, e.g. to ask whether to append the scale to the image name or whether to change the processing folder for the next procedure. Please be patient or let me know you would desire such a thing which may make me do it sooner. ;) *

### `imjoin(impaths, spath, poses, padding=0, box=None, bg="#ffffff00", align="center center")`
Function for creating collages of images on a rectangular grid. 

Each image is inserted in its original scale and the size of a position is determined from the largest dimensions of all images or the `box` argument, larger dimensions apply.

- `impaths` list of paths (strings) to every image you want to include.
- `spath` path string to save the final image as.
- `poses` 2-d array (or list of lists) with positions of each image, use 0 where
no image will be located and index images from 1 (that is their index in `impaths` + 1).
- `padding` int, number of pixels of padding around each image.
- `box` 2-tuple of int values of size of each position, defaults are largest dimensions of all images.
- `bg` background color hex string in `"#rrggbbaa"` format.
- `align` location of image in its box, same as in `matplotlib.pyplot.legend`'s argument `loc`.

Example of usage:

You have 7 images named from `img0.png` to `img6.png` in two distinct folders and you want to create two collages, i.e. to compare results from both folders. I'd do something like this:
```Python
from myimages import imjoin


def main():
    '''Joins given images into a rectangular grid.'''
    impath = "somefolder/{}/img{}.png"  # image path common to all images
    folders = ("folder0", "folder1")  # this is optional, I just wanted to do all at once
    imind = range(7)  # list of indices for images in above specified folders
    spath = "somefolder/collage{}.png"  # path to the final images
    poses = [[1, 2, 3], 
             [4, 5, 6], 
             [7, 0, 0]]  # shape of the collages
    for i in folders:
        impaths = [impath.format(i,j) for j in imind]
        imjoin(impaths, spath.format(i[-1]), poses, padding=5)


if __name__ == "__main__":
    main()

```
After that you would have two collages each indexed like the folder from where are its sub-images.

### `pic2text(impath, spath=None, iscale=1, nchars=2, chars=None, maxwidth=None, style="default", reverse=False)`
Function that converts image to text. Works best with monospaced fonts.

- `impath` string, path to image.
- `spath` - string or `None`, string is a path to final .txt file (with extension), `None` signifies the text to be printed in the shell (useful for previews).
- `iscale` int or 2-tuple (optional), inverse scale of the final image, that is kind of like `(w_new, h_new) = (w, h)//iscale`.
- `nchars` int (optional), number of different characters to use, equals to number of colors to be recognized. Can be any integer from `2` to `10` (incl.).
- `chars` string or `None` (optional), str should contain custom characters to map the colors of the image. If given as string, `len(chars)` overwrites `nchars` (`len(chars)` can be larger than `10`).
- `maxwidth` int or `None` (optional), maximum width of the final image in pixels. If given, the `maxwidth` overwrites the `iscale` parameter (useful for including text-images e.g. in code).
- `style` string (optional), specifies the character-map theme. Available options are `"default"`, `"hi-contrast"` or `"numbers"`.
- `reverse` bool (optional). If `True`, reverses the mapping of the image. Default mapping starts with `" "` (blankspace) as white/light color and ends with `"W"` as black/dark color.

With this function you can transform images to text, so you can include them in your code, school notes, etc., for example:

```
                                 ooooooooo                                 
                               oo  ooooooooo                               
                               ooooooooooooo                               
                                      oooooo                               
                         ooooooooooooooooooo WWWWW                         
                         oooooooooooooooooio WWWWWW                        
                        oooooooooooooooooo  WWWWWWW                        
                        ooooooo WWWWWWWWWWWWWWWWWWW                        
                         ooooo WWWWWWWWWWWWWWWWWWW                         
                          oooo WWWWWWWWWWWWWWWWWW                          
                               WWWWWWWWWWWWW                               
                               WWWWWWWWW  WW                               
                                WWWWWWWWWWWW                               
                                                                           
                                     i                                     
                                  i  i                                     
                    i   i i    i  i  i   i ii  i  i   i                    
                    i   i i    i  i  i   i i    i i   i                    
                    i  ii  i  ii  i  i   i  i  i  i   i                    
                    i          i                                           
                    i       ii               
```
*Note: The width and height of the final text image is actually a bit different from what is stated in the description. It accounts for the width of the literals which is ca. twice smaller than the line-to-line distance.*



