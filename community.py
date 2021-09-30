import json
import os
import networkx as nx
import pickle
import matplotlib.pyplot as plt
import mplcursors
import numpy as np
import random


class Community:
    def __init__(self, config):
        self.config = config

    def communities(self):
        try:
            fileNames = os.listdir(os.path.join(
                self.config['associatedFolderPath'], self.config['subreddit']))
        except OSError as e:
            print(e)
            raise

        try:
            if not os.path.exists(os.path.join(self.config['communitiesFolderPath'], self.config['subreddit'])):
                os.makedirs(os.path.join(
                    self.config['communitiesFolderPath'], self.config['subreddit']))
        except OSError as e:
            print(e)
            raise

        for fileName in fileNames:
            f1 = open(os.path.join(
                self.config['associatedFolderPath'], self.config['subreddit'], fileName), 'r')
            try:
                edge_list = json.load(f1)
            except json.JSONDecodeError as e:
                print(e)

            G = nx.Graph()
            DG = nx.DiGraph()
            # ax_n=0
            fig, ax = plt.subplots()

            for i in edge_list.keys():
                temp = i.split("'")
                # print(temp[1],temp[3])
                DG.add_edge(temp[1], temp[3])
                G.add_edge(temp[1], temp[3])

            pos = nx.spring_layout(G)
            comp = nx.algorithms.community.label_propagation.label_propagation_communities(
                G)
            # print(list(G.nodes(data=True)))

            f2 = open(os.path.join(self.config['communitiesFolderPath'],
                                   self.config['subreddit'], 'comm_'+fileName+'.pickle'), 'wb')
            temp = [c for c in comp]
            pickle.dump(temp, f2)
            f2.close()

            ax.set_title(fileName)
            # ax=ax[ax_n//2][ax_n%2]
            nx.draw_networkx_edges(
                G, pos, width=1.0, alpha=0.5, edge_color='k')
            for community in temp:
                nx.draw_networkx_nodes(G, pos,
                                       # ax=ax[ax_n//2][ax_n%2],
                                       nodelist=[
                                           i for i in community],
                                       node_color=[
                                           [random.random(), random.random(), random.random()]],
                                       node_size=50,
                                       alpha=0.8)
            # ax=ax[ax_n//2][ax_n%2]
            nx.draw_networkx_labels(
                G, pos, labels={n: n for n in pos.keys()}, font_size=5)
            #ax_n += 1
            f1.close()
            """
			mplcursors.cursor().connect(
					"add", lambda sel: sel.annotation.set_text(sel.artist.get_label()))"""
            f2 = open(os.path.join(self.config['communitiesFolderPath'],
                                   self.config['subreddit'], 'fig_'+fileName+'.pickle'), 'wb')
            pickle.dump(fig, f2)
            f2.close()
            plt.show()
