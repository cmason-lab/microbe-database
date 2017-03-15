#!/usr/bin/env/python3
# coding=utf-8

import sqlite3
import re
from config import *
import os
import random

connection = sqlite3.connect('microbe.db')
cursor = connection.cursor()

# Parse humann
input = ['humann/A4.humann2_pathabundance.tsv', 'humann/F2.humann2_pathabundance.tsv', 'humann/H9.humann2_pathabundance.tsv']

# Make the output dir
output_path = 'output'
#if os.path.isdir(output_path):
#    os.chmod(output_path, 777)
#    os.remove(output_path)
#os.mkdir(output_path)
#os.chmod(output_path, 777)

from plotly.offline import plot
import plotly.graph_objs as go

def plot_range(data, y_label, data_name, save_name):
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
        x = x + .001
    
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
        title='Optimal pH for sample {}'.format(save_name.split('/')[1]),
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
    plot(fig, image='png', image_filename='{}_{}_data'.format(save_name, data_name), filename='{}_{}_data.html'.format(save_name, data_name))


for path in input:
    bn = os.path.basename(path)
    save_name = '{}/{}'.format(output_path, os.path.splitext(bn)[0])
    
    # Add all the species from the taxa classification scheme
    species_list = []

    f = open(path, 'r')
    for line in f:
        expr = re.compile('.*s__(.+)\t.*')
        if expr.match(line):
            species = re.sub(expr, '\\1', line)
            species = species.replace('_', ' ')
            species = species.replace('\n', '')
            species_list.append(species)
    f.close()
    
    # Make sure we have no duplicates
    species_set = set(species_list)

    i = 0
    
    species_query = ''
    for species in species_set:
        species_query += "species='{}'".format(species)
        
        if i is not len(species_set)-1:
            species_query += ' OR '
        i = i+1
    
    binary_results = {}
    pathogenicity_results = {}
    gram_stain_results = {}
    
    for key in type_from_key:
        type = type_from_key[key]
    
        if type == 'binary':
            query = "SELECT count({}) FROM Microbe WHERE {}=1 AND ({});".format(key, key, species_query)
            cursor.execute(query)
            result = cursor.fetchone()
            
            if result:
                count = result[0]
            else:
                count = 0
            binary_results[key] = count
        elif key == 'pathogenicity':
            for i in range(1,5):
                query = "SELECT count({}) FROM Microbe WHERE pathogenicity={} AND ({});".format(key, i, species_query)
                cursor.execute(query)
                result = cursor.fetchone()[0]
                pathogenicity_results[i] = result
        elif key == 'gram_stain':
            for i in range(0,3):
                query = "SELECT count({}) FROM Microbe WHERE gram_stain={} AND ({});".format(key, i, species_query)
                cursor.execute(query)
                result = cursor.fetchone()[0]
                gram_stain_results[i] = result
        elif key == 'optimal_pH':
             query = "SELECT species, optimal_pH FROM Microbe WHERE ({});".format(key, i, species_query)
             cursor.execute(query)
             optimal_pHs = cursor.fetchall()
             plot_range(optimal_pHs, 'Optimal pH', 'optimal_pH', save_name)
        elif key == 'optimal_temperature':
             query = "SELECT species, optimal_temperature FROM Microbe WHERE ({});".format(key, i, species_query)
             cursor.execute(query)
             optimal_temps = cursor.fetchall()
             plot_range(optimal_temps, 'Optimal Temperature (°C)', 'optimal_temperature', save_name)
    
    data = [go.Bar(
                x=list(binary_results.keys()),
                y=list(binary_results.values())
        )]
    
    layout = go.Layout(
        yaxis=dict(
            title='Count'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    plot(fig, image='png', image_filename='{}_boolean_data'.format(save_name), filename='{}_boolean_data.html'.format(save_name))
    
    # Plot the pathogenicity data
    data = [go.Bar(
                x=list(pathogenicity_results.keys()),
                y=list(pathogenicity_results.values())
        )]
    layout = go.Layout(
        xaxis=dict(
            title='COGEM Pathogenicity Rating',
            autotick=False
        ),
        yaxis=dict(
            title='Count'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    plot(fig, image='png', image_filename='{}_pathogenicity'.format(save_name), filename='{}_pathogenicity.html'.format(save_name))
    
    # Plot the gram stain data
    data = [go.Bar(
                x=['Gram-negative', 'Gram-positive', 'Gram-indeterminate'],
                y=list(gram_stain_results.values())
        )]
    layout = go.Layout(
        xaxis=dict(
            title='Gram Stain',
            autotick=False
        ),
        yaxis=dict(
            title='Count'
        )
    )
    fig = go.Figure(data=data, layout=layout)
    plot(fig, image='png', image_filename='{}_gram_stain'.format(save_name), filename='{}_gram_stain.html'.format(save_name))