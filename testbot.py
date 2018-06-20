import praw
import re

bot = praw.Reddit(user_agent='EternalCards 0.1',
                  client_id='RtHZw0fr45qWUQ',
                  client_secret='2anumbtWPIOuuBUsQJOmHuqGgUc',
                  username='EternalCards',
                  password='EternalCards')

subreddit = bot.subreddit('Abeneezer')

comments = subreddit.stream.comments()

for comment in comments:
    text = comment.body
    if '[[' and ']]' in text:
        comm = text.lower()
        start = comm.index('[[')
        end = comm.index(']]')
        length = len(comm)
        param = comm[start+2:end-length]
        param2 = '[' + param.title() + '](https://cards.eternalwarcry.com/cards/full/' + param.title().replace(' ', '_') + '.png)'
        param3 = '\n To use this bot write [[Exact name of card]]'
        message = param2 + param3
        comment.reply(message)
