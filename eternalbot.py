import praw
import re

bot = praw.Reddit(user_agent='EternalCards 0.1',
                  client_id='XzEVaUokS7Rq9w',
                  client_secret='bIHZMZ3UR-a-VCR9IeQLLobSBfk',
                  username='Abeneezer',
                  password='pizzaplace')

subreddit = bot.subreddit('Abeneezer')

comments = subreddit.stream.comments()

for comment in comments:
    text = comment.body
    if '[[' and ']]' in text and comment.author != 'EternalCards':
        comm = text.lower()
        start = comm.index('[[')
        end = comm.index(']]')
        length = len(comm)
        param = comm[start+2:end-length]
        param2 = '[' + param.title() + '](https://cards.eternalwarcry.com/cards/full/' + param.title().replace(' ', '_') + '.png)'
        message = param2
        comment.reply(message)
