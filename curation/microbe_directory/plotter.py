# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt

class Plotter():
    def plot_column(self, column, x_label):
        values = list(column.values())
        hist, bin_edges = np.histogram(values)
        ln_hist = [np.log(x) if x>0 else 0 for x in hist]
        
        bin_labels = []
        for current, next in zip(bin_edges, bin_edges[1:]):
            bin_labels.append('{}–{}'.format(round(current, 2), round(next, 2)))
        
        xs = range(len(bin_labels))
        
        fig, ax = plt.subplots()
        
        rects1 = ax.bar(xs, ln_hist)
        plt.xticks(xs, bin_labels, rotation=45, ha='right')
        plt.rcParams['xtick.labelsize'] = 'x-small'
        
        plt.title('The Microbe Directory')
        plt.xlabel(x_label)
        plt.ylabel('ln(count)')
        
        axes = plt.gca()
        axes.set_ylim([0, max(ln_hist) + 1])
        
        self.__autolabel_bars(rects1, ax, hist) # put the # on top
        
        plt.show()
    
    def __autolabel_bars(self, rects, ax, labels):
        # Get y-axis height to calculate label position from.
        (y_bottom, y_top) = ax.get_ylim()
        y_height = y_top - y_bottom
    
        for i, rect in enumerate(rects):
            height = rect.get_height()
    
            # Fraction of axis height taken up by this rectangle
            p_height = (height / y_height)
    
            # If we can fit the label above the column, do that;
            # otherwise, put it inside the column.
            if p_height > 0.95: # arbitrary; 95% looked good to me.
                label_position = height - (y_height * 0.05)
            else:
                label_position = height + (y_height * 0.01)
    
            ax.text(rect.get_x() + rect.get_width()/2., label_position,
                    labels[i],
                    ha='center', va='bottom')