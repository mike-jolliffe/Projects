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

        # sns.barplot(list(self.word_count.keys()), list(self.word_count.values()))
        # plt.show()

    def get_all_edges(self):
        """
        Build list of edge tuples for network graph  ['A', 'B', 'C'] --> [('A', 'B'), ('A', 'C'), ('B', 'C')]
        :return: List
        """
        edge_list = []
        # For every job in the list
        for job in self.skills:
            # Return all unique node pairs
            edge_list.extend(tuple(itertools.combinations(job, 2)))
        self.edgeList = edge_list
        return self.edgeList

    '''TODO Use networkx to build a network graph of skills. Try to detect any present communities in graph representing
            an ecosystem or stack of tools commonly desired together.'''

    def plot_graph(self):
        """
        Builds and plots a network graph
        :return: None
        """
        # Instantiate a Graph object
        g = nx.Graph()

        # Add all edges from edge list to the object
        g.add_edges_from(self.edgeList)

        # Plot the graph, sizing nodes by number of occurrences
        nx.draw(g, nodelist=self.word_count.keys(), with_labels=True, node_size=[v * 10 for v in self.word_count.values()])
        plt.show()

if __name__ == '__main__':
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



