#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 16:12:53 2019

A FAIRE : 
    Créer une fonction qui si les 2 tableaux ont la même longueur, le même index, compare pour chaque colonne commune (même nom
    et même type) la répartition sous forme de json ==> ou alors sommer les index genre données temporelles
        ==> fait appel à un bout de code JS 1                
                                                                                                                       
    
    Créer une fonction qui pour les colonnes non communes affichent la répartition selon l'index et la colonne
        ==> fait appel à un bout de code JS 2
        
        RESTE PLUS QU'A FAIRE LE JS + BOUCLE JINJA + INTEGRER LE CSS DANS UN FICHIER A PART
        https://www.sitepoint.com/creating-simple-line-bar-charts-using-d3-js/
        https://codepen.io/jay3dec/pen/glLxK/
        
        AJUSTER LE MAX ET MIN DE L'AXE X / Y POUR ÊTRE UN PEU ADAPTATIF
        METTRE UNE MARGE GAUCHE POUR AFFICHER LE LIBELLE DE L AXE Y DANS COMPARATIVE CHARTS
        AJOUTER DES CERCLES ET DES AXES Y NEGATIFS
        
@author: hichem
"""

from flask import Flask, request, render_template
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    stats_df1 = None
    stats_df2 = None
    comparison_summary = None
    chart_data = None
    chart_names = None
    test = None
    
    if request.method == 'POST':
        file1 = request.files.get('file1', None)
        file2 = request.files.get('file2', None)
        
        if file1:
            df1 = pd.read_csv(file1)
            stats_df1 = get_global_stats(df1)
        if file2:
            df2 = pd.read_csv(file2)
            stats_df2 = get_global_stats(df2)
        if file1 and file2:
            comparison_summary = df_html_display(get_descriptive_comparison(df1, df2))
        
        chart_data, chart_names = generate_charts(df1,df2)
            
            
    return render_template('main.html', stats_df1 = stats_df1, stats_df2= stats_df2,
                           comparison_summary = comparison_summary, chart_data=chart_data,
                           chart_names = chart_names)

def get_global_stats(df):
    stats = []
    stats.append(["Number of rows", df.shape[0] ])
    stats.append(["Number of columns", df.shape[1] ])
    stats.append(["Number of duplicates", len(df) - len(df.drop_duplicates())])
    stats.append(["Number of rows with NaN values", df.isnull().values.ravel().sum() ])
    stats.append(["Header", [col for col in df.columns] ])
    stats.append(["Data Types", [dtyp.name for dtyp in df.dtypes.values] ])
    return stats
        
def get_descriptive_comparison(df1, df2):
    summary1 = df1.describe()
    summary2 = df2.describe()
    
    #If the two input tables have no common columns, then return a concatenation of both tables
    if len(list( set(summary1.columns).intersection(set(summary2.columns)) )) == 0:
        return pd.concat([summary1, summary2], axis=1)
    
    #If the two input tables are the same, return it directly
    if summary1.equals(summary2): return summary1
    
    #Merge all summary results with the suffix whether A or B
    cols_to_compare = list(summary1.columns)
    suffixes = ("_A","_B")
    merged_summary = pd.merge(summary1, summary2, left_index=True, right_index=True, suffixes=suffixes, how='outer')
    
    #Compute differences between table A and B
    header = merged_summary.columns
    for col in cols_to_compare:
        if col + suffixes[0] in header and col + suffixes[1] in header:
            merged_summary[col + "_diff_%"] = 100 * (merged_summary[col + suffixes[0]] - merged_summary[col + suffixes[1]]) / merged_summary[col + suffixes[0]] 
        else : continue
        
    comparison_summary = merged_summary.reindex(sorted(merged_summary.columns), axis=1)
    
    
    return comparison_summary

def generate_charts(df1, df2):
    mono_charts_json = []
    mono_charts_names = []
    comparative_charts_json = []
    comparative_charts_names = []
    suffixes = ("_A","_B")
    
    #Merge the two input tables
    cols1 = set(df1.select_dtypes([np.number]).columns)
    cols2 = set(df2.select_dtypes([np.number]).columns)
    merged_df = pd.merge(df1, df2, left_on = df1.index, right_on = df2.index, suffixes = suffixes, how="outer").select_dtypes([np.number])
    uncommon_cols = (cols1.difference(cols2)).union(cols2.difference(cols1))
    common_cols = cols1.intersection(cols2)
    
    #Add the index as a column
    merged_df["_Index"] = merged_df.index
    
    #Generate the JSON for each "unique" columns
    for col in uncommon_cols:
        if col != "_Index":
            col_df = merged_df[["_Index",col]]
            col_df = col_df.rename({ col_df.columns[0]: '_x', col_df.columns[1]: '_y'}, axis=1)
            mono_charts_names.append(col)
            mono_charts_json.append(col_df.dropna().to_json(orient='records'))
        
    #Generate the JSON for common columns between both DF
    for col in common_cols:
        if col != "_Index":
            comparative_charts_names.append(col)
            col_df = merged_df[["_Index",col+"_A",col+"_B"]]
            col_df = col_df.rename({ col_df.columns[0]: '_x', col_df.columns[1]: '_y1', col_df.columns[2]: '_y2'}, axis=1)
            comparative_charts_json.append(col_df.to_json(orient='records'))
            
    return {"mono_charts":mono_charts_json, 
            "comparative_charts":comparative_charts_json}, {"mono_charts":mono_charts_names, 
            "comparative_charts":comparative_charts_names} 

def df_html_display(df):
    config_df = df.style
    return config_df.render()

if __name__ == '__main__':
    app.run(debug=True)
