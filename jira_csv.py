# Support for generating a csv file understood by jira

# IssueType (bug, story, epic), Status (lane), Summary, Description, Issue ID, Parent ID, Reporter


class CsvEntry:
    def __init__(self, issue_type, status, summary, description, issue_id=None, parent_id=None):
        self.issue_type = issue_type
        self.status = status
        self.summary = summary
        self.description = description
        self.issue_id = str(issue_id) if issue_id else None
        self.parent_id = str(parent_id) if parent_id else None

    def __repr__(self):
        def output_as(x):
            return unicode(x) if x else u""
        entries = map(output_as, [self.summary, self.description, self.issue_id, self.parent_id])
        return u",".join(entries)


class CsvGenerator:
    def __init__(self):
        self.csv = []

    def add_task(self, summary, description):
        self.csv.append(CsvEntry(summary, description, len(self.csv) + 1, None))

    def add_subtask(self, issue_type, summary, description):
        self.csv.append(CsvEntry(summary, description, None, len(self.csv) + 1))

    def report(self):
        yield u"Summary,Description,Issue ID,Parent ID"
        for entry in self.csv:
            yield entry
