from collections import Counter
import json
import matplotlib.pyplot as plt
from operator import itemgetter
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
        self.word_count = Counter()

    def flatten(self):
        """
        Flattens list of lists to list of strings
        :return: List of strings
        """
        self.skills = [item for sublist in self.skills for item in sublist]
        return self.skills

    def get_count(self):
        """
        Creates dictionary with skills as keys, number of occurrences as values
        :return: dictionary
        """
        for word in self.skills:
            self.word_count[word] += 1
        return self.word_count

    def plot_freq(self):
        """
        Creates a frequency histogram depicting number of times each skill is requested across all postings
        :return: 0
        """

        sns.barplot(list(self.word_count.keys()), list(self.word_count.values()))
        plt.show()

    '''TODO Make frequency histogram, visualize skills, and return list of top 5 desired skills along with percent of
            employers desiring those skills
        TODO Use networkx to build a network graph of skills. Try to detect any present communities in graph representing
            an ecosystem or stack of tools commonly desired together.'''

if __name__ == '__main__':
    data = DataPrepper('jobs.json')
    raw = data.from_json()
    print(f"Number of job postings scraped: {data.count_jobs(raw)}")
    clean = data.clean_strings(raw)
    visualize = Visualizer(clean)
    visualize.flatten()
    visualize.get_count()
    visualize.plot_freq()



