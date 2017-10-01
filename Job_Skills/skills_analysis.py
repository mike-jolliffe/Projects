from collections import Counter
import json
import matplotlib.pyplot as plt


class DataPrepper:
    def __init__(self, file):
        self.file = file
        self.skills_list = None

    def from_json(self):
        """Opens JSON file and deserializes JSON object"""
        with open(self.file) as json_infile:
            jobs_list = json.load(json_infile)
        return jobs_list

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

    '''TODO Make frequency histogram, visualize skills, and return list of top 5 desired skills along with percent of
            employers desiring those skills
        TODO Use networkx to build a network graph of skills. Try to detect any present communities in graph representing
            an ecosystem or stack of tools commonly desired together.'''
    pass

if __name__ == '__main__':
    data = DataPrepper('jobs.json')
    clean = data.clean_strings(data.from_json())
    visualize = Visualizer(clean)
    visualize.flatten()
    print(visualize.get_count())



