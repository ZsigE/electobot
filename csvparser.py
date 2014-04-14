#!/usr/bin/python
"""
Electobot
by Philip Brien (http://github.com/ZsigE)

Analysis and prediction tool based on the 2010 UK General Election results

CSV parser
"""

import csv

def csv_to_dicts(filename):
    """Function to convert a CSV file into a list of dictionaries, each holding
    one row of the CSV table.
    """
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        
        # The first row is the headers - save off their names.
        headers = csvfile.next()
        
        # All subsequent rows are the entries in this table - save them off
        # under their appropriate headers.
        rows = []
        for row in reader:
            row_dict = {}
            for ii in range(len(row)):
                row_dict[headers[ii]] = row[ii]
            rows.append(row_dict)
            
    return rows
    