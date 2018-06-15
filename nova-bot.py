from random import randint
from slackclient import SlackClient
import urllib.request
import json
import requests
import psycopg2
from urllib import parse


class NovaBot(object):
    client = SlackClient("xoxb-301260605360-IoDIvO8sSBx5tYgK91NiBmQc")
    webhook_url = 'https://hooks.slack.com/services/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'
    url = parse.urlparse(
        "postgres://pkqqrhksxqhexa:4be7a6fb4d46a30a04867aed7093ab678230db93ef9b7f885d6068c701316b7c@ec2-107-21-201-57.compute-1.amazonaws.com:5432/d6evup307rbj4q")
    currentuser = None
    previoususer = None
    responding = False
    message = ""
    response = ""
    def __init__(self):
        self.client.rtm_connect()
        my_user_name = self.client.server.username
        parse.uses_netloc.append("postgres")
        print("Connected to slack")
    def post(self,jsonData):
        jsonDumps = json.dumps(jsonData)
        r = requests.post(self.webhook_url,data=jsonDumps,headers={'Content-Type': 'application/json'})
        print("Status Code:" + str(r.status_code) + "\nMessage Sent")

    def getvid(self,msg):
        msg['text'] = str(msg['text']).replace("!video ", "")
        msg['text'] = str(msg['text']).replace(" ", "+")
        req = urllib.request.Request('https://www.youtube.com/results?search_query={}'.format(msg['text']),
                                     headers={'User-Agent': 'Mozilla/5.0'})
        vidurl = urllib.request.urlopen(req)
        html = vidurl.read()
        for i in str(html).split():
            if 'href=\"/watch' in i:
                i = i.replace("href=", "")
                i = i.replace("\"", "")
                jsonData = {"text": "https://www.youtube.com" + i}
                try:
                    self.post(jsonData)
                    return
                except:
                    print("Video could not be found")
                    return

    def process_message(self,msg):
        # self.post({"text": "Gerard love my master"})
        if str(msg['text']).lower() == 'hello':
            jsonData = {"text": "Hello everybody in #general","attachments": [{"fallback": "Come have a blast at https://www.clubpenguinisland.com/",
                                                                         "actions": [{"type": "button", "text": "@Novacane","url": "https://www.clubpenguinisland.com/"}]}]}
            self.post(jsonData)
        if '!video' in str(msg['text']).lower():
            self.getvid(msg)
        conn = psycopg2.connect(
            database=self.url.path[1:],
            user=self.url.username,
            password=self.url.password,
            host=self.url.hostname,
            port=self.url.port
        )

        cursor = conn.cursor()

        if self.previoususer is None:
            self.previoususer = msg['user']
        if msg['user'] != self.previoususer and not self.responding:
            print("Changing current user")
            self.previoususer = msg['user']
            self.message += msg['text'] + " ;"
            self.responding = True
        if msg['user'] != self.previoususer and self.responding:
            print("Changing current user")
            self.previoususer = msg['user']
            self.response += msg['text'] + " ;"
            self.responding = False
            print("Storing Data in DB")
            message = self.message.replace("\'", "\'\'")
            response = self.response.replace("\'", "\'\'")
            cursor.execute("INSERT INTO data(message, response) VALUES (\'{}\',\'{}\')".format(message.replace("  ", " "), response.replace("  ", " ")))
            conn.commit()
            self.message = ""
            self.response = ""
        if msg['user'] == self.previoususer and not self.responding:
            self.message += msg['text'] + " "
        if msg['user'] == self.previoususer and self.responding:
            self.response += msg['text'] + " "

        cursor.execute("SELECT * FROM data;")
        res = cursor.fetchall()
        strings = []
        for i in range(0,len(res)-1):
            count = 0
            for j in str(msg['text']).split():
                for k in str(res[i][0]).split():
                    if j == k:
                        count += 1
            if count > len(str(msg['text']).split())/2 and count > len(str(res[i][0]).split())/2:
                jsonData = {"text": str(res[i][1]).replace(" ;","")}
                strings.append(jsonData)
        if len(strings) > 0:
            self.post(strings[randint(0,len(strings)-1)])
    def getevent(self):
        msg = self.client.rtm_read()
        if msg:
            for action in msg:
                print(action)
                if ('type' in action) and (action['type'] == "message") and ("text" in action) and ("bot_id" not in action):
                    self.process_message(action)


novabot = NovaBot()
while True:
    novabot.getevent()
