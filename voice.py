import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests
import cv2
import re
from time import sleep
import random
import tkinter
from tkinter import *
from functools import partial
from tkinter import messagebox
from copy import deepcopy
import winshell
from turtle import *
from random import randrange
from freegames import square, vector
from random import choice
from turtle import *
from freegames import floor, vector
import pyaudio
from PyDictionary import PyDictionary
from playsound import playsound
import ctypes
import smtplib
import datefinder
import winsound
import vlc




def speak(text):
   engine = pyttsx3.init('sapi5')
   voices = engine.getProperty('voices')
   engine.setProperty('voice', voices[1].id)
   #engine.setProperty("rate",1)
   engine.say(text)
   engine.runAndWait()

def takeCommand():
   r=sr.Recognizer()
   with sr.Microphone() as source:
       r.energy_threshold=10000
       r.adjust_for_ambient_noise(source,1.4)
       print("Listening...")
       audio=r.listen(source)
       r.pause_threshold = 1

       try:
           statement=r.recognize_google(audio,language='en-in')
           statement=statement.lower()
           print(f"user said:{statement}\n")
           return statement

       except Exception as e:
           print("Pardon me, please say that again")
           speak("Pardon me, please say that again")
           return takeCommand()



def snake():
   food = vector(0, 0)
   snake = [vector(10, 0)]
   aim = vector(0, -10)

   def change(x, y):
       aim.x = x
       aim.y = y

   def inside(head):
       "Return True if head inside boundaries."
       return -200 < head.x < 190 and -200 < head.y < 190

   def move():
       "Move snake forward one segment."
       head = snake[-1].copy()
       head.move(aim)

       if not inside(head) or head in snake:
           square(head.x, head.y, 9, 'red')
           update()
           return

       snake.append(head)

       if head == food:
           print('Snake:', len(snake))
           food.x = randrange(-15, 15) * 10
           food.y = randrange(-15, 15) * 10
       else:
           snake.pop(0)

       clear()

       for body in snake:
           square(body.x, body.y, 9, 'black')

       square(food.x, food.y, 9, 'green')
       update()
       ontimer(move, 100)

   setup(420, 420, 370, 0)
   hideturtle()
   tracer(False)
   listen()
   onkey(lambda: change(10, 0), 'Right')
   onkey(lambda: change(-10, 0), 'Left')
   onkey(lambda: change(0, 10), 'Up')
   onkey(lambda: change(0, -10), 'Down')
   move()
   done()



#pacman
def pcman():
    state = {'score': 0}
    path = Turtle(visible=False)
    writer = Turtle(visible=False)
    aim = vector(5, 0)
    pacman = vector(-40, -80)
    ghosts = [
        [vector(-180, 160), vector(5, 0)],
        [vector(-180, -160), vector(0, 5)],
        [vector(100, 160), vector(0, -5)],
        [vector(100, -160), vector(-5, 0)],
    ]
    tiles = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
        0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
        0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
        0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
        0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
        0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
        0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
        0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
        0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
        0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]

    def square(x, y):
        path.up()
        path.goto(x, y)
        path.down()
        path.begin_fill()

        for count in range(4):
            path.forward(20)
            path.left(90)

        path.end_fill()

    def offset(point):
        x = (floor(point.x, 20) + 200) / 20
        y = (180 - floor(point.y, 20)) / 20
        index = int(x + y * 20)
        return index

    def valid(point):
        index = offset(point)

        if tiles[index] == 0:
            return False

        index = offset(point + 19)

        if tiles[index] == 0:
            return False

        return point.x % 20 == 0 or point.y % 20 == 0

    def world():
        bgcolor('black')
        path.color('blue')

        for index in range(len(tiles)):
            tile = tiles[index]

            if tile > 0:
                x = (index % 20) * 20 - 200
                y = 180 - (index // 20) * 20
                square(x, y)

                if tile == 1:
                    path.up()
                    path.goto(x + 10, y + 10)
                    path.dot(2, 'white')

    def move():
        writer.undo()
        writer.write(state['score'])

        clear()

        if valid(pacman + aim):
            pacman.move(aim)

        index = offset(pacman)

        if tiles[index] == 1:
            tiles[index] = 2
            state['score'] += 1
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

        up()
        goto(pacman.x + 10, pacman.y + 10)
        dot(20, 'yellow')

        for point, course in ghosts:
            if valid(point + course):
                point.move(course)
            else:
                options = [
                    vector(5, 0),
                    vector(-5, 0),
                    vector(0, 5),
                    vector(0, -5),
                ]
                plan = choice(options)
                course.x = plan.x
                course.y = plan.y

            up()
            goto(point.x + 10, point.y + 10)
            dot(20, 'red')

        update()

        for point, course in ghosts:
            if abs(pacman - point) < 20:
                return

        ontimer(move, 100)

    def change(x, y):
        if valid(pacman + vector(x, y)):
            aim.x = x
            aim.y = y

    setup(420, 420, 370, 0)
    hideturtle()
    tracer(False)
    writer.goto(160, 160)
    writer.color('white')
    writer.write(state['score'])
    listen()
    onkey(lambda: change(5, 0), 'Right')
    onkey(lambda: change(-5, 0), 'Left')
    onkey(lambda: change(0, 5), 'Up')
    onkey(lambda: change(0, -5), 'Down')
    world()
    move()
    done()


#tictactoe
sign=0
def tictactoe():


   global board
   board = [[" " for x in range(3)] for y in range(3)]


   def winner(b, l):
       return ((b[0][0] == l and b[0][1] == l and b[0][2] == l) or
               (b[1][0] == l and b[1][1] == l and b[1][2] == l) or
               (b[2][0] == l and b[2][1] == l and b[2][2] == l) or
               (b[0][0] == l and b[1][0] == l and b[2][0] == l) or
               (b[0][1] == l and b[1][1] == l and b[2][1] == l) or
               (b[0][2] == l and b[1][2] == l and b[2][2] == l) or
               (b[0][0] == l and b[1][1] == l and b[2][2] == l) or
               (b[0][2] == l and b[1][1] == l and b[2][0] == l))


   def get_text(i, j, gb, l1, l2):
       global sign
       if board[i][j] == ' ':
           if sign % 2 == 0:
               l1.config(state=DISABLED)
               l2.config(state=ACTIVE)
               board[i][j] = "X"
           else:
               l2.config(state=DISABLED)
               l1.config(state=ACTIVE)
               board[i][j] = "O"
           sign += 1
           button[i][j].config(text=board[i][j])
       if winner(board, "X"):
           gb.destroy()
           box = messagebox.showinfo("Winner", "Player 1 won the match")
       elif winner(board, "O"):
           gb.destroy()
           box = messagebox.showinfo("Winner", "Player 2 won the match")
       elif (isfull()):
           gb.destroy()
           box = messagebox.showinfo("Tie Game", "Tie Game")



   def isfree(i, j):
       return board[i][j] == " "

   # Check the board is full or not
   def isfull():
       flag = True
       for i in board:
           if (i.count(' ') > 0):
               flag = False
       return flag


   def gameboard_pl(game_board, l1, l2):
       global button
       button = []
       for i in range(3):
           m = 3 + i
           button.append(i)
           button[i] = []
           for j in range(3):
               n = j
               button[i].append(j)
               get_t = partial(get_text, i, j, game_board, l1, l2)
               button[i][j] = Button(
                   game_board, bd=5, command=get_t, height=4, width=8)
               button[i][j].grid(row=m, column=n)
       game_board.mainloop()

   def pc():
       possiblemove = []
       for i in range(len(board)):
           for j in range(len(board[i])):
               if board[i][j] == ' ':
                   possiblemove.append([i, j])
       move = []
       if possiblemove == []:
           return
       else:
           for let in ['O', 'X']:
               for i in possiblemove:
                   boardcopy = deepcopy(board)
                   boardcopy[i[0]][i[1]] = let
                   if winner(boardcopy, let):
                       return i
           corner = []
           for i in possiblemove:
               if i in [[0, 0], [0, 2], [2, 0], [2, 2]]:
                   corner.append(i)
           if len(corner) > 0:
               move = random.randint(0, len(corner) - 1)
               return corner[move]
           edge = []
           for i in possiblemove:
               if i in [[0, 1], [1, 0], [1, 2], [2, 1]]:
                   edge.append(i)
           if len(edge) > 0:
               move = random.randint(0, len(edge) - 1)
               return edge[move]



   def get_text_pc(i, j, gb, l1, l2):
       global sign
       if board[i][j] == ' ':
           if sign % 2 == 0:
               l1.config(state=DISABLED)
               l2.config(state=ACTIVE)
               board[i][j] = "X"
           else:
               button[i][j].config(state=ACTIVE)
               l2.config(state=DISABLED)
               l1.config(state=ACTIVE)
               board[i][j] = "O"
           sign += 1
           button[i][j].config(text=board[i][j])
       x = True
       if winner(board, "X"):
           gb.destroy()
           x = False
           box = messagebox.showinfo("Winner", "Player won the match")
       elif winner(board, "O"):
           gb.destroy()
           x = False
           box = messagebox.showinfo("Winner", "Computer won the match")
       elif (isfull()):
           gb.destroy()
           x = False
           box = messagebox.showinfo("Tie Game", "Tie Game")
       if (x):
           if sign % 2 != 0:
               move = pc()
               button[move[0]][move[1]].config(state=DISABLED)
               get_text_pc(move[0], move[1], gb, l1, l2)



   def gameboard_pc(game_board, l1, l2):
       global button
       button = []
       for i in range(3):
           m = 3 + i
           button.append(i)
           button[i] = []
           for j in range(3):
               n = j
               button[i].append(j)
               get_t = partial(get_text_pc, i, j, game_board, l1, l2)
               button[i][j] = Button(
                   game_board, bd=5, command=get_t, height=4, width=8)
               button[i][j].grid(row=m, column=n)
       game_board.mainloop()


   def withpc(game_board):
       game_board.destroy()
       game_board = Tk()
       game_board.title("Tic Tac Toe")
       l1 = Button(game_board, text="Player : X", width=10)
       l1.grid(row=1, column=1)
       l2 = Button(game_board, text="Computer : O",
                   width=10, state=DISABLED)

       l2.grid(row=2, column=1)
       gameboard_pc(game_board, l1, l2)


   def withplayer(game_board):
       game_board.destroy()
       game_board = Tk()
       game_board.title("Tic Tac Toe")
       l1 = Button(game_board, text="Player 1 : X", width=10)

       l1.grid(row=1, column=1)
       l2 = Button(game_board, text="Player 2 : O",
                   width=10, state=DISABLED)

       l2.grid(row=2, column=1)
       gameboard_pl(game_board, l1, l2)


   def play():
       menu = Tk()
       menu.geometry("250x250")
       menu.title("Tic Tac Toe")
       wpc = partial(withpc, menu)
       wpl = partial(withplayer, menu)

       head = Button(menu, text="---Welcome to tic-tac-toe---",
                     activeforeground='red',
                     activebackground="yellow", bg="red",
                     fg="yellow", width=500, font='summer', bd=5)

       B1 = Button(menu, text="Single Player", command=wpc,
                   activeforeground='red',
                   activebackground="yellow", bg="red",
                   fg="yellow", width=500, font='summer', bd=5)

       B2 = Button(menu, text="Multi Player", command=wpl, activeforeground='red',
                   activebackground="yellow", bg="red", fg="yellow",
                   width=500, font='summer', bd=5)

       B3 = Button(menu, text="Exit", command=menu.quit, activeforeground='red',
                   activebackground="yellow", bg="red", fg="yellow",
                   width=500, font='summer', bd=5)
       head.pack(side='top')
       B1.pack(side='top')
       B2.pack(side='top')
       B3.pack(side='top')
       menu.mainloop()


   if __name__ == '__main__':
       play()



def joke():
   res = requests.get(
       'https://icanhazdadjoke.com/',
       headers={"Accept": "application/json"})
   if res.status_code == requests.codes.ok:
       print(str(res.json()['joke']))
       speak(str(res.json()['joke']))

       print("how did you enjoy the joke..?")
       speak("how did you enjoy the joke..?")
       opinion = takeCommand()
       # excellent joke
       if "excellent" in str(opinion) or "very good" in str(opinion) or  "good"in str(opinion):
           print("thank you do you want to hear one more...!")
           speak("thank you do you want to hear one more...!")
           feedback = takeCommand()
           if "yes" in str(feedback) or "okay" in str(feedback) or "sure" in str(feedback):
               joke()

           elif "No" in str(feedback) or "No thanks" in str(feedback):
               print("Happy,hear from you")
               speak("Happy,hear from you")
               return

       elif 'bad' in str(opinion):
           print("sorry you did not like it. Want me to tell you another one?")
           speak("sorry you did not like it. Want me to tell you another one?")
           feedback = takeCommand()
           if "yes" in str(feedback) or "okay" in str(feedback):
               joke()

           elif "No" in str(feedback) or "No thanks" in str(feedback):
               return
       return


def story1():
    choices = ["A", "B"]
    choice2a = random.choice(choices)
    print(choice2a)
    print("what is your name")
    speak("what is your name")
    name = takeCommand()

    print("Hi " + name + "Welcome to my story")
    speak("Hi " + name + "Welcome to my story")
    sleep(3)

    print("You are watching TV when an asteroid with a door falls through your roof")
    speak("You are watching TV when an asteroid with a door falls through your roof")
    sleep(2)

    print("You can:")
    speak("You can:")

    print("Choice A: Call 911")
    speak("Choice A: Call 911")

    print("Choice B: Hide behind the TV")
    speak("Choice B: Hide behind the TV")

    print("what do you do")
    speak("what do you do")

    choice1 = takeCommand().lower()

    if re.search("ChoiceA | a | A | choice A | Call 911 |call 911", choice1):
        print("You call and hear fuzz: The phone has been blocked")
        speak("You call and hear fuzz: The phone has been blocked")

        print("You can:")
        speak("You can:")

        print("Choice A: Try your cell phone")
        speak("Choice A: Try your cell phone")

        print("Choice B: Throw the phone into the ground")
        speak("Choice B: Throw the phone into the ground")

        print("What do you do?")
        speak("What do you do?")

        choice2a = takeCommand().lower()
        if re.search("choice a | Choice A | a | A |try your cell phone", choice2a):
            print("Your cell phone will not turn on; the battery has been removed")
            speak("Your cell phone will not turn on; the battery has been removed")
            sleep(2)

            print("You stomp on the ground and it breaks the floor and you fall in a hole and die")  # die
            speak("You stomp on the ground and it breaks the floor and you fall in a hole and die")  # die

        elif re.search(" choice b | Choice B | B | b |throw the phone into the ground", choice2a):
            print("You get shocked and die")  # die
            speak("You get shocked and die")  # die

    elif re.search("choice b | Choice B | B | b ", choice1):
        print("Your TV falls over and you get stuck under it")
        speak("Your TV falls over and you get stuck under it")

        print("You can:")
        speak("You can:")

        print("Choice A: Pick the TV back up and hide behind it")
        speak("Choice A: Pick the TV back up and hide behind it")

        print("Choice B: Hide behind your couch instead")
        speak("Choice B: Hide behind your couch instead")

        print("What do you do?")
        speak("What do you do?")

        choice2b = takeCommand().lower()

        if re.search("choice a | Choice A | a | A ", choice2b):
            print("The door opens and you hear something stepping out")
            speak("The door opens and you hear something stepping out")

            print("You get hit in the head by a flying spear and die")  # die
            speak("You get hit in the head by a flying spear and die")  # die

        elif choice2b == "B" or choice2b == "b":
            print("The TV falls over and makes a loud noise")
            speak("The TV falls over and makes a loud noise")

            print("You can:")
            speak("You can:")

            print("Choice A: Sceam because the loud noise startled you")
            speak("Choice A: Sceam because the loud noise startled you")

            print("Choice B: tiptoe over to see of it broke")
            speak("Choice B: tiptoe over to see of it broke")

            print("What do you do?")
            speak("What do you do?")

            choice2bb = takeCommand().lower()
            if re.search("choice a | A | a | Choice A", choice2bb):
                print("You quickly cover your mouth hoping noone or nothing heard you")
                speak("You quickly cover your mouth hoping noone or nothing heard you")

                print('''To bad something did and a 20 foot speargun pops out of the asteroid and shoots you
                       and you die ''')  # die
                speak('''To bad something did and a 20 foot speargun pops out of the asteroid and shoots you
                                           and you die ''')  # die

            elif re.search("choice b | B | b | Choice B", choice2bb):
                print("The door slowly creaks open")
                speak("The door slowly creaks open")

                print("You can")
                speak("you can")

                print("Choice A: Run like a crazy person and charge strait at the door yelling YAAAAA!")
                speak("Choice A: Run like a crazy person and charge strait at the door yelling YAAAAA!")

                print("Choice B: Go pick up a kitchen knife and crouch behint the counter")
                speak("Choice B: Go pick up a kitchen knife and crouch behint the counter")

                print("What do you do?")
                speak("what do you do?")

                choice2bbb = takeCommand().lower()
                choice2bbb = choice2bbb.lower()

                if re.search("choice a|A|a|Choice A", choice2bbb):
                    print("You see a face and you look into the eyes and vaporate")  # die
                    speak("You see a face and you look into the eyes and vaporate")  # die

                elif re.search("choice b|B|b|Choice B", choice2bbb):
                    print("The door finishes opening and you here footsteps. You peek out and see a creature")
                    speak("The door finishes opening and you here footsteps. You peek out and see a creature")

                    print("You can")
                    speak("You can")

                    print("Choice A:  Hold the knife and take a closer look")
                    speak("Choice A:  Hold the knife and take a closer look")

                    print("Choice B: Throw the knife at the creature")
                    speak("Choice B: Throw the knife at the creature")

                    print("What do you do?")
                    speak("what do you do?")

                    choicebbbb = takeCommand().lower()  # choice
                    choicebbbb = choicebbbb.lower()

                    if re.search("choice a|A|a|Choice A", choicebbbb):
                        print("You get shot by a speargun and die. THE END YOU FAILED")  # die
                        speak("You get shot by a speargun and die. THE END YOU FAILED")  # die

                    elif re.search("choice b|B|b|Choice B", choicebbbb):
                        print("You hear a groan. you see the creature lying on the floor with the knife in it's chest")
                        speak("You here a groan, you see the creature lying on the floor with the knife in it's chest")

                        print("There are 2 knives")
                        speak("There are 2 knives")

                        print("You can")
                        speak("You can")

                        print("Choice A: Grab one knife")
                        speak("Choice A: Grab one knife")

                        print("Choice B: Grab both")
                        speak("Choice B: Grab both")

                        choicebbbbb = takeCommand().lower()  # choice
                        choicebbbbb = choicebbbbb.lower()

                        if re.search("choice a|A|a|Choice A", choicebbbbb):
                            print(
                                "two creatures pop out and you throw the knife and kill one but the other one wacks you over the head with the tip of the spear and you die")  # die
                            speak(
                                "two creatures pop out and you throw the knife and kill one but the other one wacks you over the head with the tip of the spear and you die")  # die

                        else:
                            print("Two more creatures with large spearguns pop out of the door")
                            speak("Two more creatures with large spearguns pop out of the door")

                            print("You can...")
                            speak("You can...")

                            print("Choice A: Throw one knife at one and charge the other.")
                            speak("Choice A: Throw one knife at one and charge the other.")

                            print("Choice B: Throw both knives at the creatures")
                            speak("Choice B: Throw both knives at the creatures")

                            choicebbbbb = takeCommand().lower()  # choice
                            choicebbbbb = choicebbbbb.lower()

                            if re.search("choice a|A|a|Choice A", choicebbbbb):
                                print("You miss the throw and get shot and die")
                                speak("You miss the throw and get shot and die")

                                # die
                            else:
                                print(
                                    "You hit both of them and they both die, but one of them fires the shot of and just misses you")
                                speak(
                                    "You hit both of them and they both die, but one of them fires the shot of and just misses you")

                                print("You can...")
                                speak("You can...")

                                print("Choice A: Turn and run")
                                speak("Choice A: Turn and run")

                                print("choice B: Charge the door")
                                speak("choice B: Charge the door")

                                choicebbbbbb = takeCommand()  # choice
                                choicebbbbbb = choicebbbbbb.lower()

                                if re.search("choice a|A|a|Choice A", choicebbbbbb):
                                    print(
                                        "You hit the spear in the ground which was a double sided spear and die")
                                    speak(
                                        "You hit the spear in the ground which was a double sided spear and die")

                                else:
                                    print(
                                        "You go in and find 20,000 pounds of pure diamond inside. YOU WON")
                                    speak(
                                        "You go in and find 20,000 pounds of pure diamond inside. YOU WON")
                                    # winning

    else:
        print("You must answer A or B: The world explodes and you die")
        speak("You must answer A or B: The world explodes and you die")
        # die


def story2():
    answer_A = ["A", "a"]
    answer_B = ["B", "b"]
    answer_C = ["C", "c"]
    yes = ["Y", "y", "yes"]
    no = ["N", "n", "no"]

    # Grabbing objects
    sword = 0
    flower = 0

    required = ("\nUse only A, B, or C\n")  # Cutting down on duplication

    # The story is broken into sections, starting with "intro"
    def intro():
        print("After a drunken night out with friends, you awaken the "
              "next morning in a thick, dank forest. Head spinning and "
              "fighting the urge to vomit, you stand and marvel at your new, "
              "unfamiliar setting. The peace quickly fades when you hear a "
              "grotesque sound emitting behind you. A slobbering orc is "
              "running towards you. You will:")
        speak("After a drunken night out with friends, you awaken the "
              "next morning in a thick, dank forest. Head spinning and "
              "fighting the urge to vomit, you stand and marvel at your new, "
              "unfamiliar setting. The peace quickly fades when you hear a "
              "grotesque sound emitting behind you. A slobbering orc is "
              "running towards you. You will:")
        time.sleep(1)
        print("""  A. Grab a nearby rock and throw it at the orc
      B. Lie down and wait to be mauled
      C. Run""")
        speak("""  A. Grab a nearby rock and throw it at the orc
         B. Lie down and wait to be mauled
         C. Run""")
        choice = takeCommand()  # Here is your first choice.
        if choice in answer_A:
            option_rock()
        elif choice in answer_B:
            print("\nWelp, that was quick. "
                  "\n\nYou died!")
            speak("Welp, that was quick. "
                  "You died!")
        elif choice in answer_C:
            option_run()
        else:
            print(required)
            intro()

    def option_rock():
        print("\nThe orc is stunned, but regains control. He begins "
              "running towards you again. Will you:")
        speak("The orc is stunned, but regains control. He begins "
              "running towards you again. Will you:")
        time.sleep(1)
        print("""  A. Run
      B. Throw another rock
      C. Run towards a nearby cave""")
        speak("""  A. Run
         B. Throw another rock
         C. Run towards a nearby cave""")
        choice = takeCommand()
        if choice in answer_A:
            option_run()
        elif choice in answer_B:
            print("\nYou decided to throw another rock, as if the first "
                  "rock thrown did much damage. The rock flew well over the "
                  "orcs head. You missed. \n\nYou died!")
            speak("You decided to throw another rock, as if the first "
                  "rock thrown did much damage. The rock flew well over the "
                  "orcs head. You missed. You died!")
        elif choice in answer_C:
            option_cave()
        else:
            print(required)
            option_rock()

    def option_cave():
        print("\nYou were hesitant, since the cave was dark and "
              "ominous. Before you fully enter, you notice a shiny sword on "
              "the ground. Do you pick up a sword. Y/N?")
        speak("You were hesitant, since the cave was dark and "
              "ominous. Before you fully enter, you notice a shiny sword on "
              "the ground. Do you pick up a sword. Y/N?")
        choice = ()
        if choice in yes:
            sword = 1  # adds a sword
        else:
            sword = 0
        print("\nWhat do you do next?")
        speak("What do you do next?")
        time.sleep(1)
        print("""  A. Hide in silence
      B. Fight
      C. Run""")
        speak("""  A. Hide in silence
        B. Fight
        C. Run""")
        choice = takeCommand()
        if choice in answer_A:
            print("\nReally? You're going to hide in the dark? I think "
                  "orcs can see very well in the dark, right? Not sure, but "
                  "I'm going with YES, so...\n\nYou died!")
            speak("Really? You're going to hide in the dark? I think "
                  "orcs can see very well in the dark, right? Not sure, but "
                  "I'm going with YES, so...You died!")
        elif choice in answer_B:
            if sword > 0:
                print("\nYou laid in wait. The shimmering sword attracted "
                      "the orc, which thought you were no match. As he walked "
                      "closer and closer, your heart beat rapidly. As the orc "
                      "reached out to grab the sword, you pierced the blade into "
                      "its chest. \n\nYou survived!")
                speak("You laid in wait. The shimmering sword attracted "
                      "the orc, which thought you were no match. As he walked "
                      "closer and closer, your heart beat rapidly. As the orc "
                      "reached out to grab the sword, you pierced the blade into "
                      "its chest. You survived!")
            else:  # If the user didn't grab the sword
                print("\nYou should have picked up that sword. You're "
                      "defenseless. \n\nYou died!")
                speak("You should have picked up that sword. You're "
                      "defenseless. You died!")
        elif choice in answer_C:
            print("As the orc enters the dark cave, you sliently "
                  "sneak out. You're several feet away, but the orc turns "
                  "around and sees you running.")
            speak("As the orc enters the dark cave, you sliently "
                  "sneak out. You're several feet away, but the orc turns "
                  "around and sees you running.")
            option_run()
        else:
            print(required)
            option_cave()

    def option_run():
        print("\nYou run as quickly as possible, but the orc's "
              "speed is too great. You will:")
        speak("You run as quickly as possible, but the orc's "
              "speed is too great. You will:")
        time.sleep(1)
        print("""  A. Hide behind boulder
      B. Trapped, so you fight
      C. Run towards an abandoned town""")
        speak("""  A. Hide behind boulder
         B. Trapped, so you fight
         C. Run towards an abandoned town""")
        choice = takeCommand()
        if choice in answer_A:
            print("You're easily spotted. "
                  "\n\nYou died!")
            speak("You're easily spotted. "
                  "You died!")
        elif choice in answer_B:
            print("\nYou're no match for an orc. "
                  "\n\nYou died!")
            speak("You're no match for an orc. "
                  "You died!")
        elif choice in answer_C:
            option_town()
        else:
            print(required)
            option_run()

    def option_town():
        print("\nWhile frantically running, you notice a rusted "
              "sword lying in the mud. You quickly reach down and grab it, "
              "but miss. You try to calm your heavy breathing as you hide "
              "behind a delapitated building, waiting for the orc to come "
              "charging around the corner. You notice a purple flower "
              "near your foot. Do you pick it up? Y/N")
        speak("While frantically running, you notice a rusted "
              "sword lying in the mud. You quickly reach down and grab it, "
              "but miss. You try to calm your heavy breathing as you hide "
              "behind a delapitated building, waiting for the orc to come "
              "charging around the corner. You notice a purple flower "
              "near your foot. Do you pick it up? Y/N")
        choice = takeCommand()
        if choice in yes:
            flower = 1  # adds a flower
        else:
            flower = 0
        print("You hear its heavy footsteps and ready yourself for "
              "the impending orc.")
        speak("You hear its heavy footsteps and ready yourself for "
              "the impending orc.")
        time.sleep(1)
        if flower > 0:
            print("\nYou quickly hold out the purple flower, somehow "
                  "hoping it will stop the orc. It does! The orc was looking "
                  "for love. "
                  "\n\nThis got weird, but you survived!")
            speak("You quickly hold out the purple flower, somehow "
                  "hoping it will stop the orc. It does! The orc was looking "
                  "for love. "
                  "This got weird, but you survived!")
        else:  # If the user didn't grab the sword
            print("\nMaybe you should have picked up the flower. "
                  "\n\nYou died!")
            speak("Maybe you should have picked up the flower. "
                  "You died!")

    intro()


def alarm(statement):
   datef=datefinder.find_dates(statement)
   for i in datef:
       print(i)
   a=str(i)
   timeA=a[11:]
   hourA=int(timeA[:-6])
   minA=int(timeA[3:-3])
   while True:
       if hourA==datetime.datetime.now().hour:
           if minA==datetime.datetime.now().minute:
               winsound.Beep(1111,1111)


def wishMe():
    hour = datetime.datetime.now().hour
    if hour >= 0 and hour < 12:
        print("Hello,Good Morning")
        speak("Hello,Good Morning")

    elif hour >= 12 and hour < 18:
        print("Hello,Good Afternoon")
        speak("Hello,Good Afternoon")
    else:
        print("Hello,Good Evening")
        speak("Hello,Good Evening")

if __name__=='__main__':
   word=takeCommand()

   if len(word) != 0 and re.search("galaxy", word):
       print('Loading your AI personal assistant Galaxy')
       speak("Loading your AI personal assistant Galaxy")
       wishMe()
       while True:
           print("Tell me how can I help you now?")
           speak("Tell me how can I help you now?")

           statement = takeCommand().lower()
           if statement is None:
               pass

           elif re.search("goodbye|good bye|bye|exit",statement):
               print('your personal assistant Galaxy is shutting down,Good bye')
               speak('your personal assistant Galaxy is shutting down,Good bye')
               hour = datetime.datetime.now().hour
               if hour >= 0 and hour < 12:
                   print("Have a wonderful Day")
                   speak("Have a wonderful Day")
               elif hour >= 12 and hour < 18:
                   print("Have a Good Afternoon")
                   speak("Have a Good Afternoon")
               else:
                   print("Have a splendid Evening")
                   speak("Have a splendid Evening")
               break

           elif "wikipedia" in statement:
               path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
               print('Searching Wikipedia...')
               speak('Searching Wikipedia...')
               print("what do you want to search for?")
               speak("what do you want to search for?")
               wiki=takeCommand()
               url = "https://en.wikipedia.org/wiki/" + wiki
               webbrowser.get().open(url)
               #webbrowser.get(path).open(statement)
               try:

                       # Generate your App ID from WolframAlpha
                   app_id = "Your WolframAlpha App ID here"
                   client = wolframalpha.Client(app_id)
                   res = client.query(wiki)
                   answer = next(res.results).text
                   print("Your answer is" + answer)
                   speak("Your answer is " + answer)
               except:

                   wiki = wiki.split(' ')
                   wiki = " ".join(wiki[0:])
                   print("I am searching for " + wiki)
                   speak("I am searching for " + wiki)
                   speak(wikipedia.summary(wiki, sentences=3))



           elif re.search("on youtube| in youtube|open youtube",statement):

               print("what do you want to search for")
               speak("what do you want to search for")
               search=takeCommand()
               words = search.split()

               link = "http://www.youtube.com/results?search_query="

               for i in words:
                   link += i + "+"

               time.sleep(1)
               webbrowser.open_new(link[:-1])
               #webbrowser.open_new_tab("https://www.youtube.com")
               print("youtube is open now")
               speak("youtube is open now")
               time.sleep(5)

           elif re.search("search for|search about",statement):
               statement=statement.split(" ")
               path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
               if re.search('.com$', statement[2]):
                   try:
                       print("searching for : " + str(statement[2]))
                       speak("searching for : " + str(statement[2]))
                       webbrowser.get(path).open(str(statement[2]))

                   except Exception as e:
                       print("Error : " + str(e))
               else:
                   url="https://google.com/search?q=" +str(statement[2])
                   webbrowser.get().open(url)
                   print("Here is what i found for"+str(statement[2]))
                   speak("Here is what i found for"+str(statement[2]))

           elif re.search("search image|search images on",statement):
               statement=statement.split(" ")
               path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"

               url="https://www.google.com/search?q=" + statement[-1] +"&tbm=isch&ved=2ahUKEwjD6vK8wu7uAhWOSCsKHV0tBt0Q2-cCegQIABAA&oq=manche&gs_lcp=CgNpbWcQARgAMgQIABBDMgUIABCxAzICCAAyAggAMgIIADICCAAyBQgAELEDMgIIADICCAAyAggAOgcIIxDqAhAnOgQIIxAnOggIABCxAxCDAVCDfljViwFg8ZkBaAFwAHgAgAGHAYgBjAWSAQMyLjSYAQCgAQGqAQtnd3Mtd2l6LWltZ7ABCsABAQ&sclient=img&ei=xskrYMPvLI6RrQHd2pjoDQ&bih=678&biw=1536&rlz=1C1CHBF_enIN928IN928" +str(statement[2])
               webbrowser.get().open(url)
               print("Here is what i found for"+str(statement[-1]))
               speak("Here is what i found for"+str(statement[-1]))

           elif re.search("shop|in shopping$| shop for", statement):
               statement = statement.split(" ")
               path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"

               url="https://www.google.com/search?q="+statement[-1]+"&rlz=1C1CHBF_enIN928IN928&sxsrf=ALeKk03MEZJ8eUDyinvDx1VFkvz8KMs80w:1613485572732&source=lnms&tbm=shop&sa=X&ved=2ahUKEwi6mKaTzu7uAhVvzjgGHbbKDbcQ_AUoAXoECAgQAw&biw=1536&bih=722"
               webbrowser.get().open(url)
               print("Here is what i found for" + str(statement[-1]))
               speak("Here is what i found for" + str(statement[-1]))


           elif re.search("weather",statement):
               api_key="8ef61edcf1c576d65d836254e11ea420"
               base_url="https://api.openweathermap.org/data/2.5/weather?"
               print("what's the city name")
               speak("what's the city name")
               city_name=takeCommand()
               complete_url=base_url+"appid="+api_key+"&q="+city_name
               response = requests.get(complete_url)
               x=response.json()
               if x["cod"]!="404":
                   y=x["main"]
                   current_temperature = y["temp"]
                   current_humidiy = y["humidity"]
                   z = x["weather"]
                   weather_description = z[0]["description"]
                   print(" Temperature in kelvin unit = " +
                         str(current_temperature) +
                         "\n humidity (in percentage) = " +
                         str(current_humidiy) +
                         "\n description = " +
                         str(weather_description))
                   speak(" Temperature in kelvin unit is " +
                         str(current_temperature) +
                         "\n humidity in percentage is " +
                         str(current_humidiy) +
                         "\n description  " +
                         str(weather_description))


               else:
                   print("City not found")
                   speak(" City Not Found ")


           elif re.search("time",statement):
               strTime=datetime.datetime.now().strftime("%H:%M:%S")
               print(f"the time is {strTime}")
               speak(f"the time is {strTime}")

           elif re.search("date",statement):
               x = datetime.datetime.now()
               print(x)
               speak(x)

           elif re.search("day",statement):
               x = datetime.datetime.now()
               print(x.strftime("%A"))
               speak(x.strftime("%A"))

           elif re.search("month",statement):
               print(x.strftime("%B"))
               speak(x.strftime("%B"))

           elif re.search("year",statement):
               print(x.strftime("%Y"))
               speak(x.strftime("%Y"))


           elif re.search("who made you|who created you|who discovered you",statement):
               print("I was built by some brilliant to be engineers")
               speak("I was built by some brilliant to be engineers")

           elif re.search("music",statement):
               os.system("C:\\Users\\Ritis\\Music\\music1.mp3")


           elif re.search("news",statement):
               news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
               print('Here are some headlines from the Times of India,Happy reading')
               speak('Here are some headlines from the Times of India,Happy reading')
               time.sleep(6)

           elif re.search("capture|camera|pic",statement):
               ec.capture(0,"robo camera","img.jpg")

           elif re.search("don't listen|stop listening",statement):
               print("for how much time you want to stop galaxy from listening commands")
               speak("for how much time you want to stop galaxy from listening commands")
               a = int(takeCommand())
               time.sleep(a)
               print(a)



           elif re.search("calculate",statement):
               speak('I can answer to computational questions ,what question do you want to ask now')
               print('I can answer to computational questions ,what question do you want to ask now')
               question=takeCommand()
               app_id="R2K75H-7ELALHR35X"
               client = wolframalpha.Client('R2K75H-7ELALHR35X')
               res = client.query(question)
               answer = next(res.results).text
               print(answer)
               speak(answer)

           elif 'empty recycle bin' in statement:
               winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=True)
               print("Recycle Bin Recycled")
               speak("Recycle Bin Recycled")

           elif re.search("meaning of",statement):
               dict = PyDictionary()
               st = statement.split(" ")
               print(st[-1])
               meaning = dict.meaning(st[-1])
               print(meaning)
               speak(meaning)



           elif re.search("story|stories",statement):
               print("I have an interesting interactive story for you")
               speak("I have an interesting interactive story for you")
               print('''1. diamond hunt
               2.warrior''')
               speak('''1. diamond hunt
               2.warrior''')
               choice=takeCommand()
               if re.search("1|diamond hunt|one|choice one",choice):
                   story1()
               elif re.search("choice 2|warrior|two|choice two",choice):
                   story2()
               else:
                   print("no such choice available")
                   speak("no such choice available")

           elif re.search("joke",statement):
               joke()

           elif re.search("game",statement):
               print('''I have a few games
                              1.tic tac toe
                              2.snake
                              3.pac man''')
               speak('''I have a few games
               1.tic tac toe
               2.snake
               3.pac-man''')

               choice = takeCommand().lower()
               if re.search("one|1|tictactoe|tictac|Tic Tac Toe",choice):
                   tictactoe()
               elif re.search("two|1|snake|snakes",choice):
                   snake()
               elif re.search("three|3|pac man|pacman",choice):
                   pcman()


           elif "where is" in statement:
               listening = True
               statement= statement.split(" ")
               location_url = "https://www.google.com/maps/place/" + str(statement[2])
               print("Hold on , I will show you where " + statement[2] + " is.")
               speak("Hold on , I will show you where " + statement[2] + " is.")
               webbrowser.get().open(location_url)

           elif 'change background' in statement:
               ctypes.windll.user32.SystemParametersInfoW(20,
                                                          0,
                                                          "C:\\Users\\Ritis\\OneDrive\\Desktop\\wallpapers\\deadpool.jpg",
                                                          0)
               print("Background changed succesfully")
               speak("Background changed succesfully")

           elif re.search("set an alarm at",statement):
               alarm(statement)

           elif re.search(  "i love you|be my girlfriend|marry me",statement):
               print("get a life man, you can do better")
               speak("get a life man, you can do better")

           elif re.search("dinner at my place|date with me",statement):
               print("I would if I could, wouldn't I")
               speak("I would if I could, wouldn't I")

           elif re.search("signoff|logoff|lock screen|sign off", statement.lower()):
               print("Ok , your pc will log off in 10 sec make sure you exit from all applications")
               speak("Ok , your pc will log off in 10 sec make sure you exit from all applications")
               subprocess.call(["shutdown", "/l"])

           elif "restart" in statement:
               subprocess.call(["shutdown", "/r"])

           elif re.match("who are you | what is your name", statement):
               print(
                   "I am Galaxy one point o, your personal assistant. I am still under development but I can do various tasks")
               speak(
                   "I am Galaxy one point o, your personal assistant. I am still under development but I can do various tasks")

           elif "how are you" in statement:
               print("I am fine, thank you for asking")
               speak("I am fine, thank you for asking")

           elif re.search("play music | play songs", statement):
               print("Here you go with music")
               speak("Here you go with music")
               music_dir = "C:\\Users\\Ritis\\Music"
               songs = os.listdir(music_dir)
               print(songs)
               random = os.startfile(os.path.join(music_dir, songs[1]))

           elif re.search("shutdown system", statement):
               print("Hold On a Sec ! Your system is on its way to shut down")
               speak("Hold On a Sec ! Your system is on its way to shut down")
               subprocess.call('shutdown / p /f')

           elif re.search("write a note", statement):
               print("What should i write, sir")
               speak("What should i write, sir")
               note = takeCommand()
               print("what should be the name of file")
               speak("what should be the name of file")
               filename=takeCommand()
               file = open('{}.txt'.format(filename), 'w')
               print("Sir, Should i include date and time")
               speak("Sir, Should i include date and time")
               snfm = takeCommand()
               if 'yes' in snfm or 'sure' in snfm:
                   strTime =datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")#datetime.datetime.now().strftime("% H:% M:% S")
                   file.write(strTime)
                   file.write(" :- ")
                   file.write(note)
               else:
                   file.write(note)

           elif "show note" in statement:
               print("Showing Notes")
               speak("Showing Notes")
               print("which file do you want to open")
               speak("which file do you want to open")
               filename=takeCommand()
               file = open("{}.txt".format(filename), "r")
               print(file.read())
               speak(file.read(6))

           elif re.search("play video|play movie" ,statement):
               media = vlc.MediaPlayer("C:\\Users\\Ritis\\Videos\\WW1984.mkv")
               media.play()
               time.sleep(100)


           elif re.search("cortana|alexa|siri",statement):
               print("Don't even get me started on that bugger")
               speak("Don't even get me started on that bugger")

               print("Ask my sister cortana, if you want anything about her... why waste my time")
               speak("Ask my sister cortana, if you want anything about her... why waste my time")




           elif re.match("open|start",statement):
               st=statement.split(" ")
               print("Opening" + st[-1])
               speak("Opening"+st[-1])
               if os.system(st[-1])==0:
                   os.system(st[-1])
               else:
                   path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"

                   url = "https://google.com/search?q=" + str(st[-1])
                   webbrowser.get().open(url)
                   print("Here is what i found for" + str(st[-1]))
                   speak("Here is what i found for" + str(st[-1]))



           else:

               path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"

               url = "https://google.com/search?q=" + str(statement)
               webbrowser.get().open(url)
               print("Here is what i found for" + str(statement))
               speak("Here is what i found for" + str(statement))


   else:
       print("Sorry")
       speak("sorry")

time.sleep(3)
