import os

USERNAME = os.environ.get('JIRA_USERNAME')
HOST = os.environ.get('JIRA_HOST')
URL = f"https://{HOST}"
API_URL = URL + '/rest/api/2'
AUTH = (USERNAME, os.environ.get('JIRA_PASSWORD'))
PAGE_SIZE = 50
