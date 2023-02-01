import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import matplotlib.font_manager
import time

# My functions:
def binning(column,bins,threshold = None,decimals=None):
    """
    This function bins the column data according to the parameters.

    It replaces each value of the column by the name of the bin where it falls in.
    The number of bins is given by "bins", and threshold is a optional paramater to stop
    the binning there and make a last bin for values bigger than threshold.

    Parameters:
    column (pd.Series): column that we want to bin
    bins (int): number of bins we want to create
    threshold (float, optional): where we want the last bin to start (e.g. >250)
    decimals (int, optional): number of decimals the bin labels will show.
    ...

    Returns:
    pd.Series, list: column transformed with bins, list of the name of the bins
    """

    # Initialazing output
    new_column = column.copy()
    order = []

    # Computing the range of the column, and the column bins:
    if threshold == None:
        cmax,cmin = max(column),min(column)
        cbins = list(np.arange(cmin,cmax+1,(cmax-cmin)/bins))

    else:
        cmax,cmin = threshold,min(column)
        cbins = list(np.arange(cmin,cmax+1,(cmax-cmin)/(bins-1)))

    # Rounding with decimals
    if decimals == None:
        cbins = list(np.rint(cbins).astype(int))
    elif decimals != None:
        cbins = list(np.round(cbins,decimals))

    # Iterating for each row and replacing its value by its bin
    if threshold == None:
        for record in range(len(column)):
            for bin in cbins[1:]:
                if column[record] <= bin:
                    new_column[record] = str(cbins[cbins.index(bin)-1])+'-'+str(bin)
                    break

    else:
        for record in range(len(column)):
            for bin in cbins[1:]:
                if column[record] <= bin:
                    new_column[record] = str(cbins[cbins.index(bin)-1])+'-'+str(bin)
                    break
                new_column[record] = ">"+str(cbins[-1])

    # Creating list with the order of the bins
    for bin in cbins[1:]:
        order.append(str(cbins[cbins.index(bin)-1])+'-'+str(bin))
    if threshold!= None:
        order.append(">"+str(round(cbins[-1],decimals)))

    return new_column, order


def beautiful_graph(ax,title,xtitle,ytitle,format_='None',title_size=18,x_size=15,y_size=15,angle=0, name = None, label='right'):
    sns.despine(bottom = True, left = True)
    if format_!= None:
        ax.bar_label(ax.containers[0], fmt=format_, padding=4)
    if label == 'right':
        plt.tick_params(labelleft=False, left=False)
        ax.xaxis.set_ticks_position('none')
    else:
        plt.xticks([])
        ax.yaxis.set_ticks_position('none')
    plt.title(title,fontsize = title_size, pad = 15)
    plt.xlabel(xtitle,fontsize = x_size, labelpad = 10)
    plt.ylabel(ytitle,fontsize = y_size, labelpad = 10)

    plt.xticks(rotation = angle)
    if name != None:
        plt.savefig('../figures/'+name+'.png', transparent=False, bbox_inches='tight', pad_inches=0.2)
    
    return

def beautiful_lineplot(ax, title, xtitle, ytitle, format_ = None, title_size = 17, x_size = 15, y_size = 15, name = None):
    sns.despine()
    ax.legend()
    plt.legend(frameon=False)
    plt.tick_params(labelleft=True, left=True)
    plt.tick_params(labelbottom=True, bottom=True)
    plt.title(title,fontsize = title_size, pad = 15)
    plt.xlabel(xtitle,fontsize = x_size, labelpad = 10)
    plt.ylabel(ytitle,fontsize = y_size, labelpad = 10)
    if format_ != None:
        ax.yaxis.set_major_formatter(format_)
    if name != None:
        plt.savefig('../figures/'+name+'.png', transparent=False ,bbox_inches='tight', pad_inches=0.2)

    return
