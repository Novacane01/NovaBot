import urllib.request
import random

from slackclient import SlackClient
from urllib import parse
import psycopg2

parse.uses_netloc.append("postgres")
url = parse.urlparse(
    "postgres://pkqqrhksxqhexa:4be7a6fb4d46a30a04867aed7093ab678230db93ef9b7f885d6068c701316b7c@ec2-107-21-201-57.compute-1.amazonaws.com:5432/d6evup307rbj4q")

# cursor.execute("DROP TABLE data;")

# sql_command = """CREATE TABLE data(id INTEGER PRIMARY KEY, message VARCHAR(10000) NOT NULL, response VARCHAR(10000) NOT NULL);"""
# cursor.execute(sql_command)


x = 0
message = ""
response = ""
current_user = 0
responding = False


def post(channel, msg):
    chan = client.server.channels.find(channel)
    if not chan:
        raise Exception("Channel %s not found." % channel)
    return chan.send_message(msg)


def react(msg):
    client.api_call("reactions.add", None, channel=msg['item']['channel'],name = "brainlag", timestamp = msg['item']['ts'])


def process_message(msg):
    global x
    global current_user
    global responding
    global message
    global response

    for c in msg['text']:
        if c in "<>{}@":
            return
    random.seed(x)
    """if(msg['text'].lower() == "hello"):
        post(msg['channel'],"hello")"""
    # if(msg['user'] == 'USLACKBOT'):
    # post(msg['channel'],"why does slackbot do that lmao")
    if msg['text'].lower():
        if "!image" in msg['text']:
            l = []
            msg['text'] = str(msg['text']).replace("!image ", "")
            req = urllib.request.Request('https://imgur.com/search/score?q={}'.format(msg['text']),
                                         headers={'User-Agent': 'Mozilla/5.0'})
            imgurl = urllib.request.urlopen(req)
            html = imgurl.read()
            for i in str(html).split():
                if '.jpg\"' in i and 'i.imgur.com' in i:
                    i = i.replace("src=", "https:")
                    i = i.replace("\"", "")
                    l.append(i)
            try:
                post(msg['channel'], l[random.randint(0, len(l) - 1)])
                x += 1
                return
            except:
                return
        elif "!video" in msg['text']:
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
                    break
            try:
                post(msg['channel'], 'https://www.youtube.com' + i)
                x += 1
                return
            except:
                return
        else:
            string = []
            conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM data;")
            res = cursor.fetchall()
            for i in range(0, len(res)):
                count = 0
                for j in str(res[i][0]).split():
                    for k in str(msg['text']).split():
                        if j == k:
                            count += 1
                if count > len(str(res[i][0]).split()) * .75 and count > len(str(msg['text']).split()) * .75:
                    print("storing string")
                    string.append(str(res[i][1]).replace(";", ""))
            if len(string) >= 1:
                post(msg['channel'], string[random.randint(0, len(string) - 1)])
                string.clear()
            if x == 0:
                current_user = msg["user"]
                print("Changing current user")
            if current_user != msg["user"] and responding:
                print("STORING DATA IN LOCAL DB")
                response += " ;"
                responding = False
                current_user = msg["user"]
                message = message.replace("\'", "\'\'")
                response = response.replace("\'", "\'\'")
                message = message.replace("<https://", "")
                message = message.replace(".com>", ".com")
                response = response.replace(".com>", ".com")
                response = response.replace("<https://", "")
                sql_command = """INSERT INTO data(message, response, id) VALUES(\'{}\',\'{}\',{});""".format(
                    message.replace("  ", " "), response.replace("  ", " "), res[len(res) - 1][2] + 1)
                cursor.execute(sql_command)
                conn.commit()
                message = ""
                response = ""
            elif current_user != msg["user"] and not responding:
                print("End of first user message")
                responding = True
                current_user = msg["user"]
            if not responding:
                message += msg['text'].lower() + " "
            else:
                response += " " + msg['text'].lower()
        x += 1


client = SlackClient("xoxb-289218111841-tuzMZgYL598QAUFy3TSX6TfI")
client.rtm_connect()
my_user_name = client.server.username
print("Connected to slack")
while True:
    msg = client.rtm_read()
    if msg:
        for action in msg:
            print(action)
            if ('type' in action) and (action['type'] == "message") and ("text" in action):
                process_message(action)
            elif('type' in action) and (action['type'] == "reaction_added"):
                react(action)
            elif ('type' in action and (action['type'] == 'member_joined_channel')):
                post(action['channel'], "who invited the skrub?")
            elif ('type' in action and (action['type'] == 'member_left_channel')):
                post(action['channel'], "good riddance")
