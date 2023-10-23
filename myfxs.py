from matplotlib import rcParams
import numpy as np


"""
This module serves as a source of my commonly used functions.
Sorry for Czech comments. Sometimes they seem apropriate.
There is no guarantee of compatibility with scripts using this module written
before last update.
Created by Jan Klíma on 2022-03-04.
Updated on 2023-10-23.
"""


def getr2(y, yfit):
    """Returns sum of residual squares R^2.
    y - numpy array of experimental data.
    yfit - numpy array of fit data.
    """
    ss_res = np.sum((y - yfit)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    return 1 - ss_res/ss_tot


def rounc(x):
    """== ROund UNCertainty
    Returns rounded uncertainty x and an index ind, where to round the main
    value, e.g. using np.round(x0, ind).
    Use only positive numbers!
    In previous versions, there was in the first if number 1, which was later
    changed to 3 and short after that replaced with variable koef = 2.95. Some
    additional changes had to be made (e.g. int()s inside str()s).
    """
    koef = 2.95
    assert x > 0, f"Uncertainty must be a (nonzero) positive number! x was {x}"
    if x > koef:
        do, i = True, koef*10**1
        while do:
            if x < i:
                do = False
            else:
                i = i*10
        x = round(x, -len(str(int(i)))+2)
        return x, -len(str(int(i)))+2
    elif x < koef:
        do, i = True, koef*10**(-1)
        while do:
            if x > i:
                do = False
            else:
                i = i/10
        # old technique
        # x = round(x,str(i).find("3")-1)
        # return x,str(i).find("3")-1
        # new technique
        x = round(x, -round(np.log10(i)))
        return x, -round(np.log10(i))
    else:
        return x, 1


def makemyfontnice():
    """Sets all font types used in plots to look cool 
    (i.e. serif roman/italic).
    """
    rcParams["font.family"] = "serif"
    rcParams["mathtext.it"] = "serif:italic"
    rcParams["mathtext.cal"] = "serif:italic"
    rcParams["mathtext.rm"] = "serif:roman"
    rcParams["mathtext.default"] = "it"
    rcParams["mathtext.fontset"] = "custom"


def linab(x, a, b):
    """Linear function y = a*b + b."""
    return a*x + b


def lina(x, a):
    """Linear function intersecting at zero y = a*x."""
    return a*x


def calcunc(xs, nejb=np.zeros(1), quantity="X", units="x", otype="g",
            out=True, stdtype="stddevofmean", lang="EN"):
    """Calculates mean and standard deviation (of mean) using 95% confidence
    interval of Student's distribution.
    xs - array-like of experimental data.
    nejb - array-like (optional) of type B uncertainties.
    quantity - string (optional) containing quantity name.
    units - string (optional) containing units name.
    otype - string (optional), valid format_spec after ":", e.g. "03.2f".
    out - bool (optional), whether to print results in the terminal.
    sdttype - string (optional), determines whether to calculate standard
        deviation ("stddev_ub" for unbiased, that is with N-1 in the
        denominator, or "stddev_b" for biased, with N) or standard deviation
        of mean ("stddevofmean"). In case of any questions, consult e.g.:
        https://en.wikipedia.org/wiki/Standard_deviation.
    lang - string (optional), language of output (has no effect when out=False).
        Supported languages: "EN", "CZ".

    Returns:
    xbar (mean value of x) and nej (deviation) as floats.
    """
    xs, nejb = np.array(xs), np.array(nejb)
    
    def koef(n):
        """Returns the 'k' coeficient of the t-distribution for p=95%.
        CZ: Vraci koeficient 'k' dle t-rozdeleni pro p=95%."""
        koefsl = [12.71, 4.3, 3.18, 2.78, 2.57, 2.45, 2.36, 2.31, 2.26, 2.23,
                  2.2, 2.18, 2.16, 2.14, 2.13, 2.12, 2.11, 2.1, 2.09, 2.09]
        koefsh = {25: 2.06, 30: 2.04, 35: 2.03, 40: 2.02, 45: 2.01, 50: 2.01,
                  100: 1.984, 101: 1.96}
        if n < 21:
            ko = koefsl[n - 1]
        elif n < 26:
            ko = koefsh[25]
        elif n < 31:
            ko = koefsh[30]
        elif n < 36:
            ko = koefsh[35]
        elif n < 41:
            ko = koefsh[40]
        elif n < 46:
            ko = koefsh[45]
        elif n < 51:
            ko = koefsh[50]
        elif n < 101:
            ko = koefsh[100]
        else:
            ko = koefsh[101]
        return ko
    
    nmer = len(xs)
    k = koef(nmer)
    xbar = np.sum(xs)/nmer
    if stdtype == "stddevofmean":  # standard deviation of mean
        neja = np.sqrt(1/nmer/(nmer-1)*np.sum((xs - xbar)**2))*k
    elif stdtype == "stddev_ub":  # unbiased standard deviation
        neja = np.sqrt(1/(nmer-1)*np.sum((xs - xbar)**2))*k
    elif stdtype == "stddev_b":  # biased standard deviation
        neja = np.sqrt(1/nmer*np.sum((xs - xbar)**2))*k
    else:
        raise Exception("Unsupported stdtype value!")
    nejb = np.sqrt(np.sum(nejb**2))
    nej = np.sqrt(neja**2 + nejb**2)
    if out and lang == "CZ":
        print("**** Vysledek vypoctu nejistot ****")
        print("Data: {}\nJednotek dat: {}\nPrumer: {}".format(xs, nmer, xbar))
        print("Nejistota A: {}\nk: {}\nNejistota B: {}\nKombinovana: {}"
              .format(neja, k, nejb, nej))
        print("*********** Po uprave: ************")
    elif out and lang == "EN":
        print("**** Result of the calculation ****")
        print("Data: {}\nDatapoints: {}\nMean: {}".format(xs, nmer, xbar))
        print("Uncertainty A: {}\nk: {}\nUncertainty B: {}\nCombined: {}"
              .format(neja, k, nejb, nej))
        print("******** After truncation: ********")
    elif out:
        raise Exception("Unsupported language option!")
    nej, par = zaoknem(nej)
    xbar = round(xbar, par)
    if nej == int(nej):
        xbar, nej = int(xbar), int(nej)
    if out:
        outstr = "{}: ({:" + otype + "} +- {:" + otype + "}) {}"
        print(outstr.format(quantity, xbar, nej, units))
        print("*"*35)
    return xbar, nej


def prin(t, d=50, o=2, ws=True):
    """Function to print desired text into the shell, centered and filled with
    asteriscs (*) to the length d, padded with space before and after the
    text if ws=True.
    t - string, text to print for best appearance shorter than d.
    d - int (optional), length of the full row.
    o - int (optional), minimal offset/padding at the beggining when k > d-o.
    ws - bool (optional), padding the text with one whitespace on each side
        (if len(t)>d-o*2: len(row)=len(t)+o).
    """
    k = len(t)
    if ws:
        if k < d-o*2-2:
            print("*"*((d-k)//2+(d-k) % 2-1)+" "+t+" "+"*"*((d-k)//2-1))
        elif k < d-o-2:
            print("*"*o+" "+t+" "+"*"*(d-k-o-2))
        else:
            print("*"*o+" "+t)
    else:
        if k < d-o*2:
            print("*"*((d-k)//2+(d-k) % 2)+t+" "+"*"*((d-k)//2))
        elif k < d-o:
            print("*"*o+t+"*"*(d-k-o))
        else:
            print("*"*o+t)

            
def wmean(nominal_values, weights, calculate_uncertainty=True):
    """Function for calculating weighted mean. Can be useful together with 
    uncertainties package or when calculating uncertainties, in general. 
    Can calculate coresponding uncertainty dx, if weights are given as 
    w_i = 1/dx_i**2 for each w_i in weights.
    nominal_values - array-like of nominal values.
    weights - array-like of corresponding weights.  Can be a float, but then 
        this function serves as a normal mean (e.g. numpy.mean()).
    calculate_uncertainty - bool (optional), whether to calculate also 
        the combined uncertainty of nominal_values.
    """
    yield np.sum(nominal_values*weights)/np.sum(weights)
    if calculate_uncertainty:
        yield np.sqrt(1/np.sum(weights))  # is this finished?


def altline(x0, y0, r, phi, phiunit="deg"):
    """Function for calculating end points of a line from its origin
    given length and angle. (Angle+Length To LINE)
    x0, y0 - float, (given_length_unit) line-origin coorinates.
    r - float, (given_length_unit) line length.
    phi - float, (phiunit) angle of the line from x axis.
    phiunit - one of {"rad", "deg"}, determines phi unit.
    """
    if phiunit == "rad":
        return x0+r*np.cos(phi), y0+r*np.sin(phi)
    elif phiunit == "deg":
        return x0+r*np.cos(phi/180*np.pi), y0+r*np.sin(phi/180*np.pi)
    else:
        raise Exception("Unsupported phi unit!")


# ### Aliases due to compatibility with older versions. ###
zaoknem = rounc
vypoctinejistotu = calcunc
