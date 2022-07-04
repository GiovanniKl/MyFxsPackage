from matplotlib import rcParams
import numpy as np


"""
This module serves as a source of my commonly used functions.
Sorry for Czech comments. Sometimes they seem apropriate.
There is no guarantee of compatibility with scripts using this module written
before last update.
Created by Jan Klíma on 2022-03-04.
Updated on 2022-03-27.
"""


def getr2(y, yfit):
    # returns sum of residual squares R^2
    # y - numpy array of experimental data
    # yfit - numpy array of fit data
    ss_res = np.sum((y - yfit)**2)
    ss_tot = np.sum((y - np.mean(y))**2)
    return 1 - ss_res/ss_tot


def zaoknem(x):
    # == ZAOKrouhliNEjistotu(M) (round uncertainty)
    # returns rounded uncertainty x and an index ind, where to round the main
    # value, e.g. using np.round(x0, ind)
    # Use only positive numbers!
    # In previous versions, there was in the first if number 1, which was later
    # changed to 3 and short after that replaced with variable koef = 2.95. Some
    # aditional changes had to be made (e.g. int()s inside str()s).
    koef = 2.95
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
    # sets all font types used in plots to look cool (i.e. serif roman/italic)
    rcParams["font.family"] = "serif"
    rcParams["mathtext.it"] = "serif:italic"
    rcParams["mathtext.cal"] = "serif:italic"
    rcParams["mathtext.rm"] = "serif:roman"
    rcParams["mathtext.default"] = "it"
    rcParams["mathtext.fontset"] = "custom"


def linab(x, a, b):
    # linear function y = a*b + b
    return a*x + b


def lina(x, a):
    # linear function intersecting at zero y = a*x
    return a*x


def vypoctinejistotu(xs, nejb=np.zeros(1), quantity="X", units="x", otype="g",
                     out=True):
    # Calculates standard deviation and mean using 95% confidence interval of
    # Student's distribution.
    # xs - array-like of experimental data
    # nejb - array-like (optional) of type B uncertainties
    # quantity - string (optional) containing quantity name
    # units - string (optional) containing units name
    # otype - string (optional), valid format_spec after ":", e.g. "03.2f"
    # out - bool (optional), whether to print results in the terminal
    # returns xbar (mean value of x) and nej (deviation) as floats
    def koef(n):
        # vraci koeficient 'k' dle t-rozdeleni pro p=95%
        koefsl = [12.71, 4.3, 3.18, 2.78, 2.57, 2.45, 2.36, 2.31, 2.26, 2.23,
                  2.2, 2.18, 2.16, 2.14, 2.13, 2.12, 2.11, 2.1, 2.09, 2.09]
        koefsh = {25: 2.06, 30: 2.04, 35: 2.03, 40: 2.02, 45: 2.01, 50: 2.01,
                  100: 1.984, 101: 1.96}
        if n < 21:
            k = koefsl[n-1]
        elif n < 26:
            k = koefsh[25]
        elif n < 31:
            k = koefsh[30]
        elif n < 36:
            k = koefsh[35]
        elif n < 41:
            k = koefsh[40]
        elif n < 46:
            k = koefsh[45]
        elif n < 51:
            k = koefsh[50]
        elif n < 101:
            k = koefsh[100]
        else:
            k = koefsh[101]
        return k
    nmer = len(xs)
    k = koef(nmer)
    xbar = sum(xs)/nmer
    neja = np.sqrt(1/nmer/(nmer-1)*sum([(el - xbar)**2 for el in xs]))*k
    nejb = np.sqrt(sum([i**2 for i in nejb]))
    nej = np.sqrt(neja**2 + nejb**2)
    if out:
        print("**** Vysledek vypoctu nejistot ****")
        print("Data: {}\nJednotek dat: {}\nPrumer: {}".format(xs, nmer, xbar))
        print("Nejistota A: {}\nk: {}\nNejistota B: {}\nKombinovana: {}"
              .format(neja, k, nejb, nej))
        print("*********** Po uprave: ************")
    nej, par = zaoknem(nej)
    xbar = round(xbar, par)
    if nej == int(nej):
       xbar, nej = int(xbar), int(nej)
    if out:
        outstr = "{}: ({:" + otype + "} +- {:" + otype + "}) {}"
        print(outstr.format(quantity, xbar, nej, units))
        print("*"*35)
    return xbar, nej


def prin(t, d = 50, o = 2):
    # Function to print desired text into the shell, centered and filled with
    #   asteriscs (*).
    # t - string, text to print for best appearance shorter than d
    # d - int (optional), length of the full row
    # o - int (optional), minimal offset/padding at the beggining when k > d-o
    # (if len(t)>d-o*2: len(row)=len(t)+o)
    k = len(t)
    if k < d-o*2-2:
        print("*"*((d-k)//2+(d-k) % 2-1)+" "+t+" "+"*"*((d-k)//2-1))
    elif k < d-o-2:
        print("*"*o+" "+t+" "+"*"*(d-k-o-2))
    else:
        print("*"*o+" "+t)

