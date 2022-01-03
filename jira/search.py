from typing import List, Any

import app
import jira
import jira.util
import util


def get_issues() -> List[Any]:
    search_params = {
        'jql': f'assignee in ({jira.USERNAME}) AND worklogDate >= startOfMonth("{app.MONTHS_BACKWARD_OFFSET}") AND '
               'worklogDate < startOfMonth()'
               if app.IS_PREV_MONTH else f'assignee in ({jira.USERNAME}) AND worklogDate >= startOfMonth()',
        'fields': ['summary', 'status']
    }

    data = jira.util.get_all('/search', 'issues', search_params)

    issues = [{
        'key': i['key'],
        'summary': i['fields']['summary'],
        'resolution': util.get_field(i, 'fields', 'resolution', 'name'),
        'status': util.get_field(i, 'fields', 'status', 'name')
    } for i in data['issues']]

    return issues
