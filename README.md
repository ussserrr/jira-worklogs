## Installation
It is recommended to establish a new virtual environment (venv). Next, use `requirement.txt` to set up all dependencies.


## Usage
Run the main script `app.py` supplying the env variables as config parameters:

```shell
$ JIRA_HOST=jira.company.domain JIRA_USERNAME=user JIRA_PASSWORD=password python app.py
```

By default, the app assumes the https protocol for Jira access and last month as a period of statistic aggregation (so if you're running it in january, the december issues will be collected). See upper-case constants in [app](/app.py) and [jira](/jira/__init__.py) modules for more information.

The `.html` report will be generated at `pwd`.