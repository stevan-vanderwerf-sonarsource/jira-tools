from jira import JIRA
from collections import Counter
import os
from dotenv import load_dotenv
import datetime
from collections import defaultdict
import calendar as cal

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
        perUserInfo[x].append(jql_exec.count(x))
        numbs += numb
    return numbs

def longestNumRow(input):
    m = [value for key,value in input.items()]
    o = [max(list(x)) for x in list(zip(*m))]
    return o

jql = 'assignee is not EMPTY AND resolution = Unresolved ORDER BY assignee DESC'
open_tickets = jql_exec(jql)
distinct_user_list = users(open_tickets)
totalOpenTickets = output_format(distinct_user_list, open_tickets)
print(f"\n__{totalOpenTickets}__ total open tickets\n")


for day in daysInt:
    dayJQL = daysJQL[day]
    jql = f"assignee is not EMPTY and assignee changed after startOfDay(-{dayJQL}d) and assignee changed before endOfDay(-{dayJQL}d)"
    print(f"\n__{output_format(distinct_user_list, jql_exec(jql))}__ tickets taken on {days[day]}\n")

jql = f"assignee is not EMPTY and assignee changed after startOfWeek() and assignee changed before endOfWeek()"
print(f"\n__{output_format(distinct_user_list, jql_exec(jql))}__ tickets taken since Monday\n")

size = longestNumRow(perUserInfo)

print('-' * 150)
for k,v in perUserInfo.items():
    asterix = [('*' * x) + ((size[i] - x) * ' ') for i,x in enumerate(v)]
    print(f"{k:20s}: {' | '.join(map(str, asterix))} |")
    print('-' * 150)
