import csv

def csv_line_dict(csv_file_path):
    reader = csv.DictReader(open(csv_file_path))
    dict_ = {}
    for line in reader:
        yield line['Year'] + line['Cause Name'] + line['State'] , line['Year'] +','+ line['113 Cause Name'] +','+ line['Cause Name'] +','+ line['State'] +','+ line['Deaths'] +','+ line['Age-adjusted Death Rate']
