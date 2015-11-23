#!/usr/bin/env python

import json
from jira_csv import CsvGenerator

print "Loading export file from Trello, at export.json..."
with open("export.json") as f:
    data = json.load(f)

csv = CsvGenerator()


