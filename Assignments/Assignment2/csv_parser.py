import csv


def parsetodict(csv_file_path):
    reader = csv.DictReader(open(csv_file_path))
    dict_ = {}
    for line in reader:
        dict_[line['Year'] + line['Cause Name'] + line['State']] = line['Year'] +','+ line['113 Cause Name'] +','+ line['Cause Name'] +','+ line['State'] +','+ line['Deaths'] +','+ line['Age-adjusted Death Rate']
    return dict_