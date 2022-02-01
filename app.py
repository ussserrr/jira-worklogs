import datetime
import os
from pathlib import Path

import arrow
import html
# HACK: https://github.com/jazzband/prettytable/issues/40#issuecomment-846439234
html.escape = lambda *args, **kwargs: args[0]
from prettytable import PrettyTable

import jira
import jira.search
import jira.worklog


IS_PREV_MONTH = os.environ.get('IS_PREV_MONTH', default='1')
IS_PREV_MONTH = True if IS_PREV_MONTH.lower() in ['1', 'y', 'yes', 'true'] else False

MONTHS_BACKWARD_OFFSET = -1
MONTH_START = arrow.now().shift(months=MONTHS_BACKWARD_OFFSET).floor('month')\
    if IS_PREV_MONTH else arrow.now().floor('month')


def main():
    print(f"Running for {jira.HOST}, {MONTH_START.format('MMMM YYYY')}...")

    issues = jira.search.get_issues()
    jira.worklog.attach_worklogs(issues)

    table = PrettyTable(['Задача', 'Название', 'Статус', 'Затраченное время, ч'])

    for issue in issues:
        if issue['timeSpentSeconds']:
            table.add_row([
                f"<a href=\"{jira.URL + '/browse/' + issue['key']}\">{issue['key']}</a>",
                issue['summary'],
                issue['status'],
                datetime.timedelta(seconds=issue['timeSpentSeconds'])
            ])

    total_time_spent_seconds = 0
    for issue in issues:
        total_time_spent_seconds += issue['timeSpentSeconds']
    total_working_days = total_time_spent_seconds / 60 / 60 / 8

    print('========================================')
    print(f"Total in {MONTH_START.format('MMMM')}: {total_working_days} working days")

    html_content = f"""<!DOCTYPE html>
    <html lang="ru">
        <head>
          <meta charset="UTF-8">
          <title>Отчёт {jira.USERNAME}</title>
        </head>
        <body>
            <p>Выполненные работы пользователя <b>{jira.USERNAME}</b> за <b>
                {MONTH_START.format('MMMM YYYY', locale='ru')}</b>
                (согласно данным <a href="{jira.URL}">{jira.HOST}</a>)</p>
            {table.get_html_string(format=True)}
            <p><b>Всего:</b> {total_working_days} рабочих дней
                ({datetime.timedelta(seconds=total_time_spent_seconds)} часов чистого времени).</p>
            <p><b>Отчёт сформирован:</b> {arrow.now().format(locale='ru')}</p>
        </body>
    </html>"""

    report = Path(f"report_{jira.HOST}_{MONTH_START.format('YYYYMM')}.html")
    report.write_text(html_content)


if __name__ == '__main__':
    main()
