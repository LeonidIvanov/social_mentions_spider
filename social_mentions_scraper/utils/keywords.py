import csv


def get_keywords_list(path_to_file):
    keywords = []
    with open(path_to_file, 'r') as file:
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            keywords.append(row[0].replace(" ", "+").replace("&", "%26"))
    return keywords
