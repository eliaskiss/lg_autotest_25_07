from jira import JIRA  # pip install jira
import pymysql         # pip install pymysql
from datetime import datetime
from datetime import timedelta
# import time
import os
import sys
from jira.exceptions import JIRAError

# Python Jira Doc Site
# https://jira.readthedocs.io/examples.html
# pip install pyqt5-tools
# venv/lib/site-packages/qt5_applications/qt/bin/designer.exe

class logger:
    def startLog(self, fileName):
        now = datetime.now()
        currentDir = os.path.dirname(os.path.abspath(__file__))
        fileName = currentDir + "/logs/" + now.strftime(fileName + '_%Y_%m_%d') + '.txt' # ./logs/log_2023_04_11.txt
        self.logfile = open(fileName, 'w')

    def endLog(self):
        self.logfile.close()

    def log(self, message):
        now = datetime.now()
        msg = now.strftime('%H:%M:%S ') + message # 10:20:30 OpenFile
        # print msg
        self.logfile.write(msg + "\n")


class JiraIssueAutoAssigner:
    def get_issue(self, issue_id):
        options = {'server': 'http://hlm.lge.com/issue'}
        auth = ('', '')
        jira = JIRA(options, basic_auth=auth)
        return jira.issue(issue_id)

    def updateDuedate(self):
        options = {'server': 'http://hlm.lge.com/issue'}
        auth = ('', '')
        jira = JIRA(options, basic_auth=auth)
        sql = 'project in (IDWRTS) AND status = Open AND issuetype = Bug AND due is EMPTY ORDER BY created DESC'

        issues = jira.search_issues(sql, maxResults=200)

        for issue in issues:
            fields = issue.fields
            project = fields.project
            createdate = fields.created
            createdate = createdate.split('T')[0]
            createdate = datetime.strptime(createdate, '%Y-%m-%d')

            weekday = createdate.weekday()
            duedate = None

            if weekday == 2:  # 수요일 생성 > 월
                duedate = createdate + timedelta(days=5)
            elif weekday == 3:  # 목요일 생성 > 토 > 월(금,월)
                duedate = createdate + timedelta(days=5)
            elif weekday == 4:  # 금요일 생성 > 일 > 화(월, 화)
                duedate = createdate + timedelta(days=5)
            elif weekday == 5:  # 토요일 생성 > 월 > 화(월, 화)
                duedate = createdate + timedelta(days=4)
            else:
                duedate = createdate + timedelta(days=3)

            duedate = duedate.strftime('%Y-%m-%d')
            # print(duedate)
            issue.update(fields={'duedate': {'subkey': duedate}})

    def updateJiraIssueAssign(self):
        options = {'server': 'http://hlm.lge.com/qi'}
        # UserID, Passwoer (EP Account)
        auth = ('', '')
        jira = JIRA(options, basic_auth=auth)
        # sql = 'project in (WEBCOMM16, WEBCOMM17, WEBCOMM18, WEBCOMM19, WEBCOMM20, IDQSIXTHPP, IDQSIXTH, NCCOMM19, ' \
        #       'CDQLFOURT, CDQAPP, IDQOTW) ' \
        #       'AND status = Open ' \
        #       'AND cf[13457] in ("2.DQA SW 인정시험", "ID QE SW 인정시험", "SQE", "Software양산변경", "Software인정시험", "3.DQA SW 양산변경시험") ' \
        #       'AND assignee in (EMPTY)'
        sql = 'project in (WEBCOMM16, WEBCOMM17, WEBCOMM18, WEBCOMM19, WEBCOMM20, IDQSIXTHPP, IDQSIXTH, NCCOMM19, ' \
              'CDQLFOURT, CDQAPP, IDQOTW) ' \
              'AND cf[13457] in ("2.DQA SW 인정시험", "ID QE SW 인정시험", "SQE", "Software양산변경", "Software인정시험", "3.DQA SW 양산변경시험")'
        # field_list = ['cf[13457]']
        # issues = jira.search_issues(sql, maxResults=200, fields=field_list)
        issues = jira.search_issues(sql, maxResults=1, )

        for issue in issues:
            try:
                fields = issue.fields
                project = fields.project
                createdate = fields.created # 2022-04-13T14:10:20
                createdate = createdate.split('T')[0]
                createdate = datetime.strptime(createdate, '%Y-%m-%d')
                #today.strptime("%Y/%m/%d %H:%M:%S") # 2023/04/11 10:30:30

                duedate = fields.duedate
                duedate = datetime.strptime(duedate, '%Y-%m-%d')

                gap = duedate - createdate

                if gap.days == 0:
                    weekday = createdate.weekday()

                    if weekday == 2:  # 수요일 생성 > 월
                        duedate = duedate - timedelta(hours=3)
                    elif weekday == 3:  # 목요일 생성 > 토 > 월(금,월)
                        duedate = duedate + timedelta(days=5)
                    elif weekday == 4:  # 금요일 생성 > 일 > 화(월, 화)
                        duedate = duedate + timedelta(days=5)
                    elif weekday == 5:  # 토요일 생성 > 월 > 화(월, 화)
                        duedate = duedate + timedelta(days=4)
                    else:
                        duedate = duedate + timedelta(days=3)

                    duedate = duedate.strftime('%Y-%m-%d')

                    # Issue 필드값 변경
                    issue.update(fields={'duedate': duedate})
                    # self.logger.log('Duedate is updated')

                name = fields.customfield_14002
                if len(name) > 1:
                    name = ' '.join(name)
                else:
                    name = name[0]

                #             function = fields.customfield_14003
                #             if len(function) > 1:
                #                 function = ' '.join(function)
                #             else:
                #                 function = function[0]

                name = name.strip()
                function = fields.customfield_14003
                function = function[0].strip()
                # self.logger.log( 'Module: ' + name)
                # self.logger.log( 'Function: ' + function )
                assignee = self.getAssignee(name, function)

                # issue.update(assignee={'name': assignee})
                if assignee is not None:
                    if assignee != 'Not yet':
                        assignee = assignee.strip()
                        jira.assign_issue(issue, assignee)

                        if assignee == "" or assignee == "":
                            jira.add_watcher(issue, '')
                            # self.logger.log('Add Wacher: %s' % (issue.key))
                else:
                    db = pymysql.connect(host='idedqe.lge.com', user='', password='', db='trs', charset='utf8')
                    # db.set_character_set('utf8')
                    cursor = db.cursor()
                    cursor.execute('set names utf8;')

                    sql = 'INSERT INTO `jira_issue_auto_asign` (name, function, assignee, account) VALUES("%s", "%s", "%s", "%s");' % (
                        name, function, 'Not yet', 'Not yet')
                    cursor.execute(sql)
                    db.commit()
            except Exception as e:
                print(e)

    def getAssignee(self, name, function):
        db = pymysql.connect(host='idedqe.lge.com', user='', password='', db='trs', charset='utf8')
        cursor = db.cursor()
        cursor.execute('set names utf8;')

        sql = "SELECT * FROM `jira_issue_auto_asign` WHERE NAME='" + name + "' AND FUNCTION='" + function + "';"
        cursor.execute(sql)
        recs = cursor.fetchall()
        cursor.close()

        if len(recs) > 0:
            return recs[0][4]
        else:
            return None


if __name__ == '__main__':
    auto = JiraIssueAutoAssigner()
    auto.updateJiraIssueAssign()
    auto.updateDuedate()
    issue = auto.get_issue('IDEDWBS-13620')
    print(issue)