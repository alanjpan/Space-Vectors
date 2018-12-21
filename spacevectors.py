# -*- coding: utf-8 -*-
"""
Created on Fri Decc 21 09:28:35 2018

@author: Alan Jerry Pan, CPA, CSc student
@affiliation: Shanghai Jiaotong University

Program used to describe and simulate competition in n-dimensional vector space. Activatable self-propagating space object included.

Suggested citation as computer software for reference:
Pan, Alan J. (2018). Space Vectors [Computer software]. Github repository <https://github.com/alanjpan/Space--Vectors>

Note this software's license is GNU GPLv3.

Works Cited:
Pan, Alan J. (2018). Overflow [Computer software]. Github repository <https://github.com/alanjpan/Overflow>
"""

import random
secure_random = random.SystemRandom()

board = []
boardmid = []
def initializeboard(n, length):
    global board
    global boardmid
    for i in range(n):
        if length <= 0:
            space = 1
        elif length <= 6:
            space = length + random.randrange(-2, 2, 2)
        else:
            space = length + random.randrange(-4, 4, 2)
        vector = []
        for j in range(space):
            if j == 0:
                vector.append(1)
            elif j == space-1:
                vector.append(1)
            else:
                vector.append(0)
        boardmid.append(len(vector)/2)
        board.append(vector)

initializeboard(10, 10)
boardvectors = len(board)

def autophase():
    #player autophase
    for i in range(len(board)):
        done = False
        x = 0
        while done == False:
            playermove = board[i][x]
            if playermove > 10:
                overflow = playermove - 10
                if x >= boardmid[i]-1:
                    board[i][x+1] -= overflow
                    board[i][x] -= overflow
                    print('flood adversary underflow (' + str(overflow) + ')')
                elif x < boardmid[i]-1:
                    board[i][x+1] += overflow
                    board[i][x] -= overflow
                    print('advance one overflow (' + str(overflow) + ')')
            elif playermove < -10:
                overflow = playermove - -10
                if x >= boardmid[i]:
                    board[i][x+1] += overflow
                    board[i][x] -= overflow
                    print('adversary territory underflow (' + str(overflow) + ')')
            x += 1
            if x >= (2*boardmid[i]-1):
                done = True
    #comp autophase
    for i in range(len(board)):
        done = False
        x = len(board[i])-1
        while done == False:
            cpumove = board[i][x]
            if cpumove > 10:
                overflow = cpumove - 10
                if x <= boardmid[i]:
                    board[i][x-1] -= overflow
                    board[i][x] -= overflow
                    print('cpu overflows your territory (' + str(overflow) + ')')
                elif x > boardmid[i]:
                    board[i][x-1] += overflow
                    board[i][x] -= overflow
            elif cpumove < -10:
                overflow = cpumove - -10
                if x <= boardmid[i]:
                    board[i][x-1] += overflow
                    board[i][x] -= overflow
                    print('cpu continues to flood your territory (' + str(overflow) + ')')
            x -= 1
            if x <= 0:
                done = True

def playermoveboard(select, position):
    board[position][0] += select
def cpumoveboard(select, position):
    board[position][len(board[position])-1] += select

def cputurn(cpuhand):
    select = secure_random.choice(cpuhand)    
    position = random.randrange(0, boardvectors, 1)
    cpumoveboard(select, position)
    draw = drawhand()
    cpuhand.append(draw)

def playersturn(hand):
    output = ''
    print('(vector)')
    for i in range(len(board)):
        output += '(' + str(i) + '): '
        for j in range(len(board[i])):
            if j == boardmid[i]:
                output += '// '
            output += '[' + str(board[i][j]) + '] '
        output += '\n'
    print(output)
    print('S P A C E V E C T O R S')
    print('turn: ' + str(turns))
    output = ''
    for i in range(len(hand)):
        output += '(' + str(i) + '):' + str(hand[i]) + ' '
    print(output)
    try:
        print('play a card')
        select = int(input())
        print('which vector of space')
        position = int(input())
        playermoveboard(hand[select], position)
        hand.pop(select)
        print(hand)
        draw = drawhand()
        hand.append(draw)
    except:
        print('turn wasted')

def drawhand():
    card = random.randrange(3, 10, 1)
    return card

def stationaryspace():
    #player
    for i in range(len(board)):
        for j in range(int(boardmid[i])):
            if board[i][j] == 10:
                board[i][0] += 1
                print('full space overflow in vector ' + str(i))
    #cpu
    for i in range(len(board)):
        for j in range(int(boardmid[i])*2-1, int(boardmid[i]), -1):
            if board[i][j] == 10:
                board[i][len(board[i])-1] += 1
                print('adversary space overflow in vector ' + str(i))

playerhand = []
cpuhand = []
for i in range(5):
    card = drawhand()
    playerhand.append(card)
for i in range(5):
    card = drawhand()
    cpuhand.append(card)

turns = 0
while turns <= 20:
    cputurn(cpuhand)
    print()
    autophase()
    playersturn(playerhand)
    print()
    autophase()
    print()
    stationaryspace()
    turns += 1

print('\nGAME RESULTS')
playerscore = 0
cpuscore = 0

for i in range(len(board)):
    for j in range(int(boardmid[i])):
        playerscore += board[i][j]
    cpustart= int(boardmid[i])
    cpuend = len(board[i])
    for j in range(cpustart, cpuend):
        cpuscore += board[i][j]
print('PLAYER SCORE: ' + str(playerscore))
print('CPU SCORE: ' + str(cpuscore))
if playerscore > cpuscore:
    print('HUMAN LEADERSHIP: ' + str(playerscore - cpuscore))
elif playerscore < cpuscore:
    print('AI LEADERSHIP: ' + str(cpuscore - playerscore))
elif playerscore == cpuscore:
    print("TIE GAME")