from jira import JIRA
from collections import Counter
import os
from dotenv import load_dotenv

load_dotenv()

jiraOptions = {'server': "https://services.sonarsource.com/"}
jira = JIRA(options=jiraOptions, basic_auth=(
    os.environ.get('JIRA_USERNAME'), os.environ.get('JIRA_PASSWORD')))

def users(y):
    return Counter(y).keys()

def jql_exec(jql):
    print('\nrunning query')
    y = [issue.fields.assignee.name for issue in jira.search_issues(jql, maxResults=500)]
    return y

def output_format(distinct_user_list, jql_exec):
    numbs = 0
    print('\n')
    for x in distinct_user_list:
        numb = jql_exec.count(x)
        print(f"{x:20s} {jql_exec.count(x)*'*'}")
        numbs += numb 
    return numbs

jql = 'assignee is not EMPTY AND resolution = Unresolved ORDER BY assignee DESC'
open_tickets = jql_exec(jql)
distinct_user_list = users(open_tickets)

jql = "assignee is not EMPTY and assignee changed after startOfDay(-0d)"
print(f"\n__{output_format(distinct_user_list, jql_exec(jql))}__ tickets taken today\n")