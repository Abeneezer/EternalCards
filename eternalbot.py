import praw
import re
import json
from pprint import pprint

botAlt = praw.Reddit(user_agent='EternalCards 0.1',
                  client_id='RtHZw0fr45qWUQ',
                  client_secret='2anumbtWPIOuuBUsQJOmHuqGgUc',
                  username='EternalCards',
                  password='EternalCards')

bot = praw.Reddit(user_agent='EternalCards 0.1',
                  client_id='XzEVaUokS7Rq9w',
                  client_secret='bIHZMZ3UR-a-VCR9IeQLLobSBfk',
                  username='Abeneezer',
                  password='pizzaplace')

subreddit = bot.subreddit('EternalCardGame')

comments = subreddit.stream.comments()

fullNames = []
names = []

with open('eternal-cards.json') as f:
    data = json.load(f);
    for x in range(0, len(data)):
        fullNames.append([data[x]["Name"], data[x]["DetailsUrl"]])
    names = [link[0] for link in fullNames]

def buildResponse(comment, result = ''):
    comm = comment.title()
    start = comm.index('[[')
    end = comm.index(']]')
    length = len(comm)
    param = comm[start+2:end-length]
    link = 'link not found'
    for x in range(0, len(fullNames)):
        if fullNames[x][0] == param:
            link = fullNames[x][1]
    param2 = '[' + param.title() + '](https://cards.eternalwarcry.com/cards/full/' + param.replace(' ', '_') + '.png)  '
    param3 = ' - [(EW)](' + link + ') \n'
    if param in names:
        newResult = result + param2 + param3
    else:
        newResult = result
    rString = comm[end-length+1:]
    if '[[' and ']]' in rString:
        newResult = buildResponse(rString, newResult);
    return newResult;

for comment in comments:
    text = comment.body
    if '[[' and ']]' in text and comment.author != 'EternalCards':
        finished = buildResponse(text)
        message = finished + "^^Problems ^^or ^^questions? ^^Contact ^^/u/Abeneezer"
        if finished != '':
            print (message)
            comment.reply(message)
