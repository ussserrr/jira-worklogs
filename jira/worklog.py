from typing import List, Any

import arrow

import app
import jira.util


def attach_worklogs(issues: List[Any]):
    for issue in issues:
        data = jira.util.get_all(f"/issue/{issue['key']}/worklog", 'worklogs')
        worklogs = data['worklogs']

        issue['timeSpentSeconds'] = 0
        for record in worklogs:
            if arrow.get(record['started']) > app.MONTH_START:
                issue['timeSpentSeconds'] += record['timeSpentSeconds']
