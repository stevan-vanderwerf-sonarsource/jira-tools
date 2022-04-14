from jira import JIRA
from collections import Counter
import os
from dotenv import load_dotenv
import datetime
from collections import defaultdict
import calendar as cal
import pandas as pd
from tabulate import tabulate

load_dotenv()

jiraOptions = {'server': "https://services.sonarsource.com/"}
jira = JIRA(options=jiraOptions, basic_auth=(
    os.environ.get('JIRA_USERNAME'), os.environ.get('JIRA_PASSWORD')))
dayOfWeekInteger = datetime.datetime.today()

daysInt = [day for day in range(dayOfWeekInteger.weekday() + 1)]
# output: [0, 1, 2]
daysJQL = list(reversed(daysInt))
# output: [2, 1, 0]

days = [d for d in cal.day_name]
# output: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
perUserInfo = {}
perUserInfo = defaultdict(list)
# output: defaultdict(<class 'list'>, {'user.1': [19, 1, 4, 1, 6, 3, 0, 15], 'user.2': [12, 6, 3, 2, 0, 0, 0, 11]})
# output: defaultdict(<class 'list'>, {'user.1': ['13 *************', '2  **', '0  ', '3  ***', '5  *****'], 'user.2': ['13 *************', '0  ', '2  **', '3  ***', '5  *****']})

def users(y):
    #output: dict_keys(['user.1', 'user.2'])
    return Counter(y).keys()

def jql_exec(jql):
    y = [issue.fields.assignee.name for issue in jira.search_issues(jql, maxResults=500)]
    #output: ['user.1', 'user.1', 'user.1', 'user.2', 'user.1']
    return y    

def output_format(distinct_user_list, jql_exec):
    '''returns total number of tickets open, but also populates perUserInfo list'''
    numbs = 0
    for x in distinct_user_list:
        numb = jql_exec.count(x)
        numb_padded = str(numb).ljust(2)
        perUserInfo[x].append(numb_padded + ' ' + (numb * '*'))
        numbs += numb
    return numbs

jql = 'assignee is not EMPTY AND resolution = Unresolved ORDER BY assignee DESC'
open_tickets = jql_exec(jql)
distinct_user_list = users(open_tickets)
totalOpenTickets = output_format(distinct_user_list, open_tickets)

for day in daysInt:
    dayJQL = daysJQL[day]
    jql = f"assignee is not EMPTY and assignee changed after startOfDay(-{dayJQL}d) and assignee changed before endOfDay(-{dayJQL}d)"
    output_format(distinct_user_list, jql_exec(jql))

jql = f"assignee is not EMPTY and assignee changed after startOfWeek() and assignee changed before endOfWeek()"
output_format(distinct_user_list, jql_exec(jql))

df = pd.DataFrame(perUserInfo.values(),columns=['TotalTicketsHeld','Mon','Tue','Wed','TotalTicketsTakenSinceMon'],index=perUserInfo.keys()) #.sort_index()
print(tabulate(df, headers=df.columns, tablefmt='fancy_grid'))