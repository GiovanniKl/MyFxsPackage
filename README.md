# MyFxsPackage
Package of useful functions for Python 3.7, mostly used for experimental data analysis.

*Warning: Czech words included!*

## List of functions
### `getr2(y, yfit)`
Calculate the coefficient of determination (R squared).
- `y`    numpy-array, list of experimental data
- `yfit` numpy-array, must be of the same length as `y`, list of fitted values at the same `x` value

Returns:
- `r2`   float, coefficient of determination (not in percents)

### `zaoknem(x)`
Function for rounding mean and deviation pairs.
- `x` deviation to be rounded

Returns:
- `x` rounded deviation to one significant digit (except for when the digit (denoted as `d`)  `1 < d < 2.95`, it is rounded to two significant digits)
- `ind` index used in `round(mean, ind)` or `np.round(mean, ind)` to round the mean (denoted `mean`) according to the deviation

### `makemyfontnice()`
Set all fonts used in `matplotlib` plots to serif type.

### `linab(x, a, b)`
Linear function $y(x) = ax + b$. Used often for fitting and regression purposes.

### `lina(x, a)`
Linear function $y(x) = ax$. Used often for fitting and regression purposes.

### `vypoctinejistotu(xs, nejb=np.zeros(1), quantity="X", units="x", otype="g", out=True)`
Calculate mean and standard deviation from a list of measurements using 95% confidence interval of T distribution.
- `xs` array-like of experimental data (e.g. floats)
- `nejb` array-like (optional) of type B uncertainties (e.g. floats)
- `quantity` string (optional) containing quantity name
- `units` string (optional) containing units name
- `otype` string (optional), valid `format_spec` after ":", e.g. `"03.2f"`
- `out` bool (optional), whether to print results in the terminal (if `False`, previous three arguments are not used)

Returns: 
- `xbar` float, mean value of `xs`
- `nej` float, standard deviation

### `prin(t, do=50, o=2)`
Print desired text into the shell, centered and filled with asteriscs (*) to the length d, padded with space before and after the text.
-  `t` string, text to print, for best appearance shorter than `d-o-2`
- `d` int (optional), length of the full row
- `o` int (optional), minimal offset/padding at the beggining when `len(t) > d-o-2`
- `ws` bool (optional), padding the text with one whitespace on each side
