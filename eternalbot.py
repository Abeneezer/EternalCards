import praw
import re
import json
from pprint import pprint

bot = praw.Reddit(user_agent='EternalCards 0.1',
                  client_id='RtHZw0fr45qWUQ',
                  client_secret='2anumbtWPIOuuBUsQJOmHuqGgUc',
                  username='EternalCards',
                  password='EternalCards')

botAlt = praw.Reddit(user_agent='EternalCards 0.1',
                  client_id='XzEVaUokS7Rq9w',
                  client_secret='bIHZMZ3UR-a-VCR9IeQLLobSBfk',
                  username='Abeneezer',
                  password='pizzaplace')

subreddit = bot.subreddit('EternalCardGame')

writerName = 'EternalCards'

comments = subreddit.stream.comments()

fullNames = []
names = []

with open('eternal-cards.json') as f:
    data = json.load(f);
    for x in range(0, len(data)):
        fullNames.append([data[x]["Name"], data[x]["DetailsUrl"], data[x]["ImageUrl"]])
    names = [link[0].lower() for link in fullNames]

def buildResponse(comment, result = ''):
    print(comment)
    comm = comment
    start = comm.index('[[')
    end = comm.index(']]')
    length = len(comm)
    param = comm[start+2:end-length]
    url = '[' + param + '](https://cards.eternalwarcry.com/cards/full/' + param.replace(' ', '_') + '.png)  '
    link = 'link not found'
    for x in range(0, len(fullNames)):
        if fullNames[x][0].lower() == param.lower():
            link = fullNames[x][1]
            url = fullNames[x][2]
    param2 = '[' + param + '](' + url + ')  '
    param3 = ' - ([EWC](' + link + ')) \n \n'
    if param.lower() in names:
        newResult = result + param2 + param3
    else:
        newResult = result
    rString = comm[end-length+1:]
    if '[[' in rString and ']]' in rString:
        newResult = buildResponse(rString, newResult);
    return newResult;

for comment in comments:
    comment.refresh()
    alreadyDone = False
    for y in comment.replies:
        if y.author == writerName:
            alreadyDone = True
    text = comment.body
    if '[[' in text and ']]' in text and comment.author != writerName and not alreadyDone:
        finished = buildResponse(text)
        message = finished + " ^^Problems ^^or ^^questions? ^^Contact ^^[\/u\/Abeneezer](https://www.reddit.com/user/Abeneezer)"
        if finished != '':
            print (message)
            comment.reply(message)
