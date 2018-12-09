import praw
from prawcore.exceptions import PrawcoreException
import re
import json
import difflib
import time
import sys
from string import capwords
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

subredditAlt = bot.subreddit('Abeneezer')

writerName = 'EternalCards'

comments = subreddit.stream.comments()

fullNames = []
names = []

with open('eternal-cards.json') as f:
    data = json.load(f);
    for x in range(0, len(data)):
        fullNames.append([data[x]["Name"], data[x]["DetailsUrl"], data[x]["ImageUrl"]])
    names = [name[0].lower() for name in fullNames]

def buildResponse(comment, result = ''):
    comm = comment
    start = comm.index('[[')
    end = comm.index(']]')
    length = len(comm)
    param = comm[start+2:end-length]
    url = '[' + param + '](https://cards.eternalwarcry.com/cards/full/' + param.replace(' ', '_') + '.png)  '
    link = 'link not found'

    cardFound = False
    correctlyNamed = False
    matches = []

    for x in range(0, len(fullNames)):
        itername = fullNames[x][0].lower()
        if itername == param.lower():
            link = fullNames[x][1]
            url = fullNames[x][2]
            cardFound = True
            correctlyNamed = True
        elif param.lower() in itername:
            matches.append(itername)

    cardName = ''
    if not cardFound and not matches:
        bestGuess = difflib.get_close_matches(param.lower(), names)
        if not not bestGuess:
            cardName = bestGuess[0]
            cardFound = True
    elif not cardFound:
        possibleNames = []
        for x in matches:
            if ',' in x:
                possibleNames.append(x)
        if not possibleNames:
            bestGuess = difflib.get_close_matches(param.lower(), matches, 1, 0)
            cardName = bestGuess[0]
            cardFound = True
        else:
            bestGuess = difflib.get_close_matches(param.lower(), possibleNames, 1, 0)
            cardName = bestGuess[0]
            cardFound = True

    for x in range(0, len(fullNames)):
        itername = fullNames[x][0].lower()
        if itername == cardName.lower():
            link = fullNames[x][1]
            url = fullNames[x][2]

    param2 = '[' + param + '](' + url + ')  ' if correctlyNamed else '[' + capwords(cardName) + '](' + url + ')  '
    param3 = ' - ([EWC](' + link + ')) \n \n'
    if cardFound:
        newResult = result + param2 + param3
    else:
        newResult = result
    rString = comm[end-length+1:]
    if '[[' in rString and ']]' in rString:
        newResult = buildResponse(rString, newResult);
    return newResult;

#print(buildResponse('[[cirsos c]]'))
def main():
    try:
        for comment in comments:
            comment.refresh()
            alreadyDone = False
            for y in comment.replies:
                if y.author == writerName:
                    alreadyDone = True
            text = comment.body
            if ('[[' in text and ']]' in text and comment.author != writerName
            and comment.author != "MTGCardFetcher" and not alreadyDone
            and not '/u/MTGCardFetcher'.lower() in text.lower()):
                finished = buildResponse(text)
                message = finished + " ^^Problems ^^or ^^questions? ^^Contact ^^[\/u\/Abeneezer](https://www.reddit.com/user/Abeneezer)"
                if finished != '':
                    print (message)
                    comment.reply(message)
    except PrawcoreException:
        print("Prawcore Exceptions thrown at " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        time.sleep(60*5)
        main()
    print('exiting')

main()
