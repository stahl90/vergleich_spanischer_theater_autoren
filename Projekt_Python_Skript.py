# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 02:40:31 2017

@author: Jakob Stahl
"""

import glob
import os
import re
import pandas as pd
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt



def find_all(file):
    
    """I. Name der Datei"""
    file_name = os.path.basename(file)[:-4]
    print (file_name)
    
    """II. Textinhalt der Datei"""
    with open(file,"r", encoding = "utf-8") as sourcefile:
        full_text = sourcefile.read()
        
    """III. Rollenliste der Datei"""
    roles_ids=re.findall("xml:id=\"te(.*)\">", full_text)
    
    """IV. Speaker_Ids der Datei"""   
    all_ids_in_text = re.findall("who=\"#te(.*?)\">", full_text)
    
    """V. Eine zweite Id Liste anlegen, falls 90er Ids vorhanden sind"""
    ids_no_ninety = [item for item in all_ids_in_text if not re.search(r".*-9[0-9]", item)]
    
    """VI. Eine zweite Rolenliste anlegen, falls 90er Ids vorhanden sind""" 
    roles_ninety = roles_ids.copy()
    for item in all_ids_in_text:
        ninety = re.findall(".*-9[0-9]", item)
        if ninety not in roles_ids:
            roles_ninety.extend(ninety) 
    
    roles_ninety =(set(roles_ninety))
    
    
    """
    VII. Wer folgt auf welche Figur?
    - 2 Sprecher Fenster
    - ohne 90er Ids
    - ungewichtet und ungerichtet
    """
    list_of_teams = []
    for item in zip(ids_no_ninety[:-1],ids_no_ninety[1:]):
        list_of_teams.append(item)
    GroupofSpeaker=list(set(list_of_teams))
    
    
    """
    - Entfernt Kante vom Knoten zum gleichen Knoten 
    - Entfernt doppelte Kante zwischen zwei Knoten
    """
    for item in GroupofSpeaker:
        if (item[0] == item[1]):
            GroupofSpeaker.remove(item)
    simple_edges = set(tuple(sorted(t)) for t in GroupofSpeaker)
    
        
    """Anzahl der Knoten und der Verbindungen"""  
    all_nodes = (len(roles_ids)) 
    all_edges = (len(simple_edges))  
    
    columns = [file_name]
    dates_2speaker_noNinety_noDirected = pd.DataFrame(all_nodes, index=['2_uw_no90_nodes'], columns=columns)
    dates_edges = pd.DataFrame(all_edges, index=['2_uw_no90_edges'], columns=columns)
    dates_2speaker_noNinety_noDirected = dates_2speaker_noNinety_noDirected.append(dates_edges)
    
    
    """ Netzwerk """
    G1 = nx.Graph()
    G1.add_nodes_from(roles_ids)
    G1.add_edges_from(simple_edges)
   
   
    """Maximalen und Minimalen Grad"""
    degree_sequence=sorted(nx.degree(G1).values(),reverse=True) 
    maxdegree = degree_sequence[:1]
    mindegree = degree_sequence[-1:]
    dates_max = pd.DataFrame(maxdegree, index=['2_uw_no90_maxDegree'], columns=columns)
    dates_min = pd.DataFrame(mindegree, index=['2_uw_no90_minDegree'], columns=columns)
    dates_2speaker_noNinety_noDirected = dates_2speaker_noNinety_noDirected.append(dates_max)
    dates_2speaker_noNinety_noDirected = dates_2speaker_noNinety_noDirected.append(dates_min)
    
    
    """Durschnittsgrad"""
    avdegree = sum(G1.degree().values())/float(len(G1))
    dates_degree = pd.DataFrame(avdegree, index=['2_uw_no90_avdegree'], columns=columns)
    dates_2speaker_noNinety_noDirected = dates_2speaker_noNinety_noDirected.append(dates_degree)
    
    
    """Zentralitätsmaß (degree centrality)"""
    dc = sorted(nx.degree_centrality(G1).values(),reverse=True)
    maxdc = (dc[:1])
    dates_degree_centrality = pd.DataFrame(maxdc, index=['2_uw_no90_maxdc'], columns=columns)
    dates_2speaker_noNinety_noDirected = dates_2speaker_noNinety_noDirected.append(dates_degree_centrality)
    
    
    """Globaler Cluster-Koeffizient"""
    ck = nx.average_clustering(G1)
    dates_global_cluster = pd.DataFrame(ck, index=['2_uw_no90_ck'], columns=columns)
    dates_2speaker_noNinety_noDirected = dates_2speaker_noNinety_noDirected.append(dates_global_cluster)
    
    
    """Dichte"""
    den = nx.density(G1)
    dates_density = pd.DataFrame(den, index=['2_uw_no90_density'], columns=columns)
    dates_2speaker_noNinety_noDirected = dates_2speaker_noNinety_noDirected.append(dates_density)
    
    """Show the dataframe"""
    print (dates_2speaker_noNinety_noDirected)
    
    
    """nx Graph"""
    #nx.draw(G1, with_labels=True, font_weight='bold', alpha=0.5)
    #plt.savefig('./output/grafiken/'+file_name+'_simple_path1.pdf')
    #plt.show() # display
    
    
    """
    VIII. Wer folgt auf welche Figur?
    - 2 Sprecher Fenster
    - mit 90er Ids
    - ungewichtet und ungerichtet
    """
    list_of_teams = []
    for item in zip(all_ids_in_text[:-1],all_ids_in_text[1:]):
        list_of_teams.append(item)
    GroupofSpeaker=list(set(list_of_teams))
    
    
    """
    - Entfernt Kante vom Knoten zum gleichen Knoten 
    - Entfernt doppelte Kante zwischen zwei Knoten
    """
    for item in GroupofSpeaker:
        if (item[0] == item[1]):
            GroupofSpeaker.remove(item)
    
    simple_edges = set(tuple(sorted(t)) for t in GroupofSpeaker)
       
       
    """Anzahl der Knoten und der Verbindungen"""  
    all_edges = (len(simple_edges))  
    all_nodes_with90 = (len(roles_ninety))
    
    columns = [file_name]
    dates_2speaker_Ninety_noDirected = pd.DataFrame(all_nodes_with90, index=['2_uw_90_nodes'], columns=columns)
    dates90_edges = pd.DataFrame(all_edges, index=['2_uw_90_edges'], columns=columns)
    dates_2speaker_Ninety_noDirected = dates_2speaker_Ninety_noDirected.append(dates90_edges)
    
    
    """ Netzwerk """
    G2 = nx.Graph()
    G2.add_nodes_from(roles_ninety)
    G2.add_edges_from(simple_edges)
    
    
    """Maximalen und Minimalen Grad"""
    degree_sequence=sorted(nx.degree(G2).values(),reverse=True) 
    maxdegree = degree_sequence[:1]
    mindegree = degree_sequence[-1:]
    dates90_max = pd.DataFrame(maxdegree, index=['2_uw_90_maxDegree'], columns=columns)
    dates90_min = pd.DataFrame(mindegree, index=['2_uw_90_minDegree'], columns=columns)
    dates_2speaker_Ninety_noDirected = dates_2speaker_Ninety_noDirected.append(dates90_max)
    dates_2speaker_Ninety_noDirected = dates_2speaker_Ninety_noDirected.append(dates90_min)
    
    
    """Durschnittsgrad"""
    avdegree = sum(G2.degree().values())/float(len(G2))
    dates90_degree = pd.DataFrame(avdegree, index=['2_uw_90_avdegree'], columns=columns)
    dates_2speaker_Ninety_noDirected = dates_2speaker_Ninety_noDirected.append(dates90_degree)
    
    
    """Zentralitätsmaß (degree centrality)"""
    dc = sorted(nx.degree_centrality(G2).values(),reverse=True)
    maxdc = (dc[:1])
    dates90_degree_centrality = pd.DataFrame(maxdc, index=['2_uw_90_maxdc'], columns=columns)
    dates_2speaker_Ninety_noDirected = dates_2speaker_Ninety_noDirected.append(dates90_degree_centrality)
    
    
    """Globaler Cluster-Koeffizient"""
    ck = nx.average_clustering(G2)
    dates90_global_cluster = pd.DataFrame(ck, index=['2_uw_90_ck'], columns=columns)
    dates_2speaker_Ninety_noDirected = dates_2speaker_Ninety_noDirected.append(dates90_global_cluster)
    
    
    """Dichte"""
    den = nx.density(G2)
    dates90_density = pd.DataFrame(den, index=['2_uw_90_density'], columns=columns)
    dates_2speaker_Ninety_noDirected = dates_2speaker_Ninety_noDirected.append(dates90_density)
    
    """Show the dataframe"""
    print (dates_2speaker_Ninety_noDirected)
    
    """nx Graph"""
    #nx.draw(G2, with_labels=True, font_weight='bold', alpha=0.5)
    #plt.savefig('./output/grafiken/'+file_name+'_simple_path1.pdf')
    #plt.show() # display
    
    
    """
    XI. Wer folgt auf welche Figur?
    - 2 Sprecher Fenster
    - ohne 90er Ids
    - gewichtet und gerichtet
    """
    list_of_teams = []
    for z in zip(ids_no_ninety[:-1],ids_no_ninety[1:]):
        list_of_teams.append(z)
    
    
    """
    - Entfernt Kante vom Knoten zum gleichen Knoten 
    """
    for item in list_of_teams:
        if (item[0] == item[1]):
            list_of_teams.remove(item)
    counter=dict(Counter(list_of_teams))
    
    
    """Anzahl der Knoten und der Verbindungen"""  
    all_edges = (len(counter))  
    dates_2speaker_noNinety_Directed = pd.DataFrame(all_nodes, index=['2_gw_nodes'], columns=columns)
    dates_directed_eges = pd.DataFrame(all_edges, index=['2_gw_no90_edges'], columns=columns)
    dates_2speaker_noNinety_Directed = dates_2speaker_noNinety_Directed.append(dates_directed_eges)
    
    
    """ Netzwerk """
    G3 = nx.DiGraph((x, y, {'weight': v}) for (x, y), v in Counter(list_of_teams).items())
    G3.add_nodes_from(roles_ids)
   
    
    """Maximalen und Minimalen Grad"""
    degree_sequence=sorted(nx.degree(G3, weight='weight').values(),reverse=True) 
    
    maxdegree = degree_sequence[:1]
    mindegree = degree_sequence[-1:]
    dates_directed_max = pd.DataFrame(maxdegree, index=['2_gw_no90_maxDegree'], columns=columns)
    dates_directed_min = pd.DataFrame(mindegree, index=['2_gw_no90_minDegree'], columns=columns)
    dates_2speaker_noNinety_Directed = dates_2speaker_noNinety_Directed.append(dates_directed_max)
    dates_2speaker_noNinety_Directed = dates_2speaker_noNinety_Directed.append(dates_directed_min)
    
    """Durschnittsgrad"""
    avdegree = sum(G3.degree(weight='weight').values())/float(len(G3))
    dates_directed_degree = pd.DataFrame(avdegree, index=['2_gw_no90_avdegree'], columns=columns)
    dates_2speaker_noNinety_Directed = dates_2speaker_noNinety_Directed.append(dates_directed_degree)
    
    
    """Zentralitätsmaß (in degree centrality and out degree centrality)"""
    dc = sorted(nx.in_degree_centrality(G3).values(),reverse=True)
    dc2 = sorted(nx.out_degree_centrality(G3).values(), reverse=True)
    indc = (dc[:1])
    outdc = (dc2[:1])
    
    dates_directed_in_degree_centrality = pd.DataFrame(indc, index=['2_gw_no90_indc'], columns=columns)
    dates_directed_out_degree_centrality = pd.DataFrame(outdc, index=['2_gw_no90_outdc'], columns=columns)
    dates_2speaker_noNinety_Directed = dates_2speaker_noNinety_Directed.append(dates_directed_in_degree_centrality)
    dates_2speaker_noNinety_Directed = dates_2speaker_noNinety_Directed.append(dates_directed_out_degree_centrality)
    
    
    """Globaler Cluster-Koeffizient (entfällt)"""
    #ck = nx.average_clustering(G3)
    #ck = sum(nx.clustering(G3).values())/float(len(G3))
    
    
    """Dichte"""
    den = nx.density(G3)
    dates_directed_degree_density = pd.DataFrame(den, index=['2_gw_no90_density'], columns=columns)
    dates_2speaker_noNinety_Directed = dates_2speaker_noNinety_Directed.append(dates_directed_degree_density)
    
    """Show the dataframe"""
    print (dates_2speaker_noNinety_Directed)
    
    
    """nx Graph"""
    #nx.draw(G3, with_labels=True, font_weight='bold', alpha=0.5)
    #plt.savefig('./output/grafiken/'+file_name+'_simple_path1.pdf')
    #plt.show() # display
    
    
    """
    XI. Wer folgt auf welche Figur?
    - 2 Sprecher Fenster
    - mit 90er Ids
    - gewichtet und gerichtet
    """
    list_of_teams = []
    for z in zip(all_ids_in_text[:-1],all_ids_in_text[1:]):
        list_of_teams.append(z)
    
    
    """
    - Entfernt Kante vom Knoten zum gleichen Knoten 
    """
    for item in list_of_teams:
        if (item[0] == item[1]):
            list_of_teams.remove(item)
    
    counter=dict(Counter(list_of_teams))
    
    
    """Anzahl der Knoten und der Verbindungen"""  
    all_edges = (len(counter))  
    
    dates_2speaker_Ninety_Directed = pd.DataFrame(all_nodes_with90, index=['2_gw_nodes'], columns=columns)
    dates_directed_edges = pd.DataFrame(all_edges, index=['2_gw_90_edges'], columns=columns)
    dates_2speaker_Ninety_Directed = dates_2speaker_Ninety_Directed.append(dates_directed_edges)
    
    
    """ Netzwerk """
    G4 = nx.DiGraph((x, y, {'weight': v}) for (x, y), v in Counter(list_of_teams).items())
    G4.add_nodes_from(roles_ids)
    
    
    """Maximalen und Minimalen Grad"""
    degree_sequence=sorted(nx.degree(G4, weight='weight').values(),reverse=True) 
    
    maxdegree = degree_sequence[:1]
    mindegree = degree_sequence[-1:]
    dates_directed_max = pd.DataFrame(maxdegree, index=['2_gw_90_maxDegree'], columns=columns)
    dates_directed_min = pd.DataFrame(mindegree, index=['2_gw_90_minDegree'], columns=columns)
    dates_2speaker_Ninety_Directed = dates_2speaker_Ninety_Directed.append(dates_directed_max)
    dates_2speaker_Ninety_Directed = dates_2speaker_Ninety_Directed.append(dates_directed_min)
    
    
    """Durschnittsgrad"""
    avdegree = sum(G4.degree(weight='weight').values())/float(len(G4))
    dates_directed_degree = pd.DataFrame(avdegree, index=['2_gw_90_avdegree'], columns=columns)
    dates_2speaker_Ninety_Directed = dates_2speaker_Ninety_Directed.append(dates_directed_degree)
    
    
    """Zentralitätsmaß (degree centrality)"""
    dc = sorted(nx.in_degree_centrality(G4).values(),reverse=True)
    dc2 = sorted(nx.out_degree_centrality(G4).values(), reverse=True)
    indc = (dc[:1])
    outdc = (dc2[:1])
    
    dates_directed_in_degree_centrality = pd.DataFrame(indc, index=['2_gw_90_indc'], columns=columns)
    dates_directed_out_degree_centrality = pd.DataFrame(outdc, index=['2_gw_90_outdc'], columns=columns)
    dates_2speaker_Ninety_Directed = dates_2speaker_Ninety_Directed.append(dates_directed_in_degree_centrality)
    dates_2speaker_Ninety_Directed = dates_2speaker_Ninety_Directed.append(dates_directed_out_degree_centrality)
    
    
    """Dichte"""
    den = nx.density(G4)
    dates90_density = pd.DataFrame(den, index=['2_gw_90_density'], columns=columns)
    dates_2speaker_Ninety_Directed = dates_2speaker_Ninety_Directed.append(dates90_density)
    
    """Show the dataframe"""
    print (dates_2speaker_Ninety_Directed)
    
    """nx Graph"""
    #nx.draw(G4, with_labels=True, font_weight='bold', alpha=0.5)
    #plt.savefig('./output/grafiken/'+file_name+'_simple_path1.pdf')
    #plt.show() # display
    
    
    """Speichern/Save the Files"""
    with open('./output/'+file_name+"Daten"+".csv", "w") as resultsFile_II:
        dates_2speaker_noNinety_noDirected.to_csv(resultsFile_II)
        dates_2speaker_Ninety_noDirected.to_csv(resultsFile_II)
        dates_2speaker_noNinety_Directed.to_csv(resultsFile_II)
        dates_2speaker_Ninety_Directed.to_csv(resultsFile_II)
    
  

"""main"""
def main(inputpath, outputpath):
    for file in glob.glob(inputpath):
        find_all(file)
        
main('./input/*.xml','./output/')