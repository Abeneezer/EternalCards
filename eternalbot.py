import praw
import re

bot = praw.Reddit(user_agent='EternalCards 0.1',
                  client_id='RtHZw0fr45qWUQ',
                  client_secret='2anumbtWPIOuuBUsQJOmHuqGgUc',
                  username='EternalCards',
                  password='EternalCards')

subreddit = bot.subreddit('EternalCardGame')

comments = subreddit.stream.comments()

def buildResponse(comment, result = ''):
    comm = comment.lower()
    start = comm.index('[[')
    end = comm.index(']]')
    length = len(comm)
    param = comm[start+2:end-length]
    param2 = '[' + param.title() + '](https://cards.eternalwarcry.com/cards/full/' + param.title().replace(' ', '_') + '.png)  '
    newResult = result + param2
    rString = comm[end-length+1:]
    if '[[' and ']]' in rString:
        newResult = buildResponse(rString, newResult);
    return newResult;

for comment in comments:
    text = comment.body
    if '[[' and ']]' in text and comment.author != 'EternalCards':
        finished = buildResponse(text)
        message = finished
        print(message)
        comment.reply(message)
