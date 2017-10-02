from collections import Counter
import itertools
import json
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import seaborn as sns


class DataPrepper:
    def __init__(self, file):
        self.file = file
        self.skills_list = None
        self.num_jobs = None

    def from_json(self):
        """Opens JSON file and deserializes JSON object"""
        with open(self.file) as json_infile:
            jobs_list = json.load(json_infile)
        return jobs_list

    def count_jobs(self, jobs_list):
        """
        Calculates the total number of job postings
        :param: List of lists
        :return: Integer
        """
        self.num_jobs = len(jobs_list)
        return self.num_jobs

    def clean_strings(self, lists):
        """Breaks up list of single-element lists into list of multi-element lists"""
        cleaned = []
        for lst in lists:
            new_lst = list(lst[0].split(', '))
            cleaned.append(new_lst)

        self.skills_list = cleaned
        return self.skills_list

class Visualizer:
    def __init__(self, skills):
        self.skills = skills
        self.flatskills = None
        self.word_count = Counter()
        self.edgeList = None
        self.graph = None

    def flatten(self):
        """
        Flattens list of lists to list of strings
        :return: List of strings
        """
        self.flatskills = [item for sublist in self.skills for item in sublist]
        return self.flatskills

    def get_count(self):
        """
        Creates dictionary with skills as keys, number of occurrences as values
        :return: dictionary
        """
        for word in self.flatskills:
            self.word_count[word] += 1
        # Get rid of Python, b/c appears in every result by default
        del self.word_count['Python']
        # Get rid of any occurrence that is less than 5
        drop_keys = [word for word in self.word_count if self.word_count[word] < 10]
        for key in drop_keys:
            del self.word_count[key]

        return self.word_count

    def plot_freq(self):
        """
        Creates a frequency histogram depicting number of times each skill is requested across all postings
        :return: None
        """
        # Create DataFrame object from word count dictionary
        skills_df = pd.DataFrame(list(self.word_count.items()))
        skills_df.columns = ["Skill", "Count"]


        # Sort DataFrame by Count column
        skills_df = skills_df.sort_values(['Count'], ascending=False).reset_index(drop=True)
        print(skills_df)

        # Create a figure
        plt.figure(figsize=(16, 8))
        # Plot barchart with DataFrame index as x values
        ax = sns.barplot(skills_df.index, skills_df.Count)
        ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: '{:,}'.format(int(x))))
        ax.set(xlabel='Skill', ylabel='Count')
        # add proper Skill values as x labels
        ax.set_xticklabels(skills_df.Skill, size=8)
        for item in ax.get_xticklabels(): item.set_rotation(90)
        for i, v in enumerate(skills_df['Count'].iteritems()):
            ax.text(i, v[1], '{:,}'.format(v[1]), color='m', va='bottom', rotation=45, size=8)
        plt.tight_layout()
        plt.show()

        #sns.barplot(list(self.word_count.keys()), list(self.word_count.values()))
        #plt.show()

    def get_all_edges(self):
        """
        Build list of edge tuples for network graph  ['A', 'B', 'C'] --> [('A', 'B'), ('A', 'C'), ('B', 'C')]
        :return: List
        """
        edge_list = []
        no_py_nodes = []
        # For every job in the list
        for job in self.skills:
            # Return all unique node pairs
            edge_list.extend(tuple(itertools.combinations(job, 2)))
        for node_pair in edge_list:
            # Drop node pairs where one of the nodes is 'Python'
            if node_pair[0] == 'Python' or node_pair[1] == 'Python':
                pass
            # Drop node pairs where one of the elements is low-frequency
            elif not node_pair[0] in self.word_count or not node_pair[1] in self.word_count:
                pass
            else:
                no_py_nodes.append(node_pair)
        self.edgeList = no_py_nodes
        return self.edgeList

    '''TODO Use networkx to build a network graph of skills. Try to detect any present communities in graph representing
            an ecosystem or stack of tools commonly desired together.'''

    def plot_graph(self):
        """
        Builds and plots a network graph
        :return: None
        """
        # Instantiate a Graph object
        self.graph = nx.Graph()

        # Add all edges from edge list to the object
        self.graph.add_edges_from(self.edgeList)

        # Plot the graph, sizing nodes by number of occurrences
        nx.draw(self.graph, nodelist=self.word_count.keys(),
                            edge_color='gray',
                            font_color='black', with_labels=True,
                            font_weight='bold', node_size=[v ** 1.6 for v in self.word_count.values()])

        plt.show()

    def detect_communities(self):
        """
        Finds up to k different communities by using Girvan-Newman algorithm for edge removal. Also finds the largest
        clique for each node in the network
        :return: Dictionary
        """
        # return len(list(nx.algorithms.clique.find_cliques(self.graph)))

        # G = nx.algorithms.clique.make_max_clique_graph(self.graph)
        # exit()
        # nx.draw(G, with_labels=True)
        # plt.show()

        k = 40
        comp = nx.algorithms.community.centrality.girvan_newman(self.graph)
        limited = itertools.takewhile(lambda c: len(c) <= k, comp)
        for communities in limited:
            if len(communities) == 50:
                print(tuple(sorted(c) for c in communities))



def run():
    data = DataPrepper('jobs.json')
    raw = data.from_json()
    print(f"Number of job postings scraped: {data.count_jobs(raw)}")
    clean = data.clean_strings(raw)
    visualize = Visualizer(clean)
    visualize.flatten()
    visualize.get_count()

    #visualize.plot_freq()
    visualize.get_all_edges()
    visualize.plot_graph()
    print(visualize.detect_communities())

if __name__ == '__main__':
    run()



