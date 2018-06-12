import pickle
import re

def read_in_txt(filepath):
    """Reads data from .txt file in given filepath
    :type filepath: str
    :rtype: str
    """
    data = None
    metadata_dict = {}
    with open(filepath, 'r') as infile:
        data = infile.read().replace('\n', '')
    return data

def to_dict(data):
    """Parses text in form "001 Abc defg 002 Hij 003" into dict with numbers as
    keys and text as values
    :type data: str
    :rtype: dict
    """
    # Only split on whitespace followed by a digit (to get k:v group)
    split_data = re.split('\s(?=[0-9])', data)
    for elmnt in split_data:
        # Only split on whitespace preceded by a digit (to separate k and v)
        elmnt = re.split('(?<=[0-9])\s', elmnt)
        metadata_dict[elmnt[0]] = elmnt[1]
        
# output = open('all_source_paths_pickle', 'wb')
# print 'Pickling all source paths'
# pickle.dump(self.all_source_paths, output)
# output.close()


if __name__ == '__main__':
    data = read_in_txt('/Users/jolliffe/Desktop/EVT_105_metadata.txt')
