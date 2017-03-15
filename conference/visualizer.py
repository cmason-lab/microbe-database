#!/usr/bin/env python3.5

import random

from plotly.offline import plot
import plotly.graph_objs as go

def plot_range(data, title_label, y_label, data_name, save_name):
    # This is where the scatter will start relative to the boxplot at x=0
    x = .35
    # This is the x distance b/w each scatter point
    xstep = .001
    
    # These will be plotted in the scatter later
    x_data = []
    y_data = []
    color_data = []
    hover_data = []
    
    for item in data:
        # Value is of the form 1:5,7; 5.8; 1:2; ...
        species = item[0]
        value = item[1]
        
        if value == None:
            continue
        
        # One color per species
        color = 'rgba({}, {}, {}, .9)'.format(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        
        # If there is more than one optimal pH (i.e. 7,10:12)
        multiple = value.split(',')
        
        for single in multiple:
            # single can be a point value or a range
            single_split = single.split(':')
        
            if len(single_split) > 1:
                # average the range and use this value
                single_value = (float(single_split[0]) + float(single_split[1]))/2
            else:
                # Just use the point value
                single_value = float(single_split[0])
        
            # Add our data    
            x_data.append(x)
            y_data.append(single_value)
            color_data.append(color)
            hover_data.append('{}: {}'.format(species, single.replace(':', '-')))
        
        # Increment the x value
        x = x + .01
    
    # Make the scatter (color-coded by species)
    trace_scatter = go.Scatter(
        x = x_data,
        y = y_data,
        mode = 'markers',
        text=hover_data,
        hoverinfo='text',
        marker = dict(
             size = 8,
             color = color_data,
             line = dict(
                 width = 1,
             )
         )
    )
    
    # Make the boxplot that goes with the scatter
    trace_box = go.Box(
        y=y_data,
        hoverinfo='y',
        boxpoints= False,
        line=dict(width=1),
        whiskerwidth=.5
    )
    
    data = [trace_scatter, trace_box]
    
    layout = go.Layout(
        title='{} for sample {}'.format(title_label, save_name.split('/')[1]),
        hovermode='closest',
        xaxis=dict(
            showticklabels=False
        ),
        yaxis=dict(
            title=y_label
        ),
        showlegend = False
    )
    
    fig = go.Figure(data=data, layout=layout)
    plot(fig, image='png', image_filename='{}_{}_data'.format(save_name, data_name), filename='{}_{}_data.html'.format(save_name, data_name), auto_open=False)

def plot_booleans(binary_results, save_name):
    bar_data_labels = {'antimicrobial_susceptibility': 'Antimicrobial-susceptible<br>microbes', 'spore_forming': 'Spore-formers',
                       'biofilm_forming': 'Biofilm-formers', 'extreme_environment': 'Extremophiles',
                       'microbiome_location': 'Found in microbiome', 'plant_pathogen': 'Potential plant<br>pathogens',
                       'animal_pathogen': 'Potential animal<br>pathogens'}
    
    order = ['spore_forming', 'biofilm_forming', 'antimicrobial_susceptibility', 'extreme_environment', 'microbiome_location',
        'plant_pathogen', 'animal_pathogen']
                         
    data_x = []
    data_y = []
    
    for key in order:
        data_y.append(binary_results[key])
        data_x.append(bar_data_labels[key])
    
    data = [go.Bar(
                x=list(data_x),
                y=list(data_y)
        )]
    
    layout = go.Layout(
        yaxis=dict(
            title='Number of Microbes'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    plot(fig, image='png', image_filename='{}_boolean_data'.format(save_name), filename='{}_boolean_data.html'.format(save_name), auto_open=False)
    
def plot_pathogenicity(pathogenicity_results, save_name):
    # COGEM risk class 2
    # Plot the pathogenicity data
    data = [go.Bar(
                x=['COGEM risk class 1', 'COGEM risk class 2', 'COGEM risk class 3'],
                y=list(pathogenicity_results.values())
        )]
    layout = go.Layout(
        xaxis=dict(
            autotick=False
        ),
        yaxis=dict(
            title='Number of Microbes'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    plot(fig, image='png', image_filename='{}_pathogenicity'.format(save_name), filename='{}_pathogenicity.html'.format(save_name), auto_open=False)
    
def plot_gram_stain(gram_stain_results, save_name):
     # Plot the gram stain data
    data = [go.Bar(
                x=['Gram-negative', 'Gram-positive', 'Gram-indeterminate'],
                y=list(gram_stain_results.values())
        )]
    layout = go.Layout(
        xaxis=dict(
            autotick=False
        ),
        yaxis=dict(
            title='Number of Microbes'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    plot(fig, image='png', image_filename='{}_gram_stain'.format(save_name), filename='{}_gram_stain.html'.format(save_name), auto_open=False)
    