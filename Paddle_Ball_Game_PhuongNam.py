from tkinter import *
import random
import time
import pygame
from PIL import ImageTk, Image


class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Paddle Ball Game Ball")  # Tạo title
        self.tk.resizable(0, 0)
        self.tk.iconbitmap('Paddle_Ball_Game_Icon.ico')  # Tạo icon góc trái
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=600, height=400, bd=0, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        # Open Image
        sgi = Image.open('menu_glow.png')
        self.cre = Image.open('credit.png')
        self.x_button = Image.open('x.png')
        self.x_button_pic = ImageTk.PhotoImage(self.x_button)
        self.speed_1 = Image.open('Speed1.png')
        self.pic_speed_1 = ImageTk.PhotoImage(self.speed_1)
        self.speed_2 = Image.open('Speed2.png')
        self.pic_speed_2 = ImageTk.PhotoImage(self.speed_2)
        self.speed_3 = Image.open('Speed3.png')
        self.pic_speed_3 = ImageTk.PhotoImage(self.speed_3)
        self.images_background = [
            Image.open('Background.png'),
            Image.open('Background-Glow-Left.png'),
            Image.open('Background-Glow-Top.png'),
            Image.open('Background-Glow-Right.png'),
            Image.open('Background-Glow-Bottom.png')
        ]
        self.tempRestartPic = Image.open('restartIconButton.png')
        self.restartPic = ImageTk.PhotoImage(self.tempRestartPic)
        self.tempMenuPic = Image.open('menuIconButton.png')
        self.menuPic = ImageTk.PhotoImage(self.tempMenuPic)
        self.tempQuitPic = Image.open('quitIconButton.png')
        self.quitPic = ImageTk.PhotoImage(self.tempQuitPic)
        self.crepic = ImageTk.PhotoImage(self.cre)
        self.backgroundImage = ImageTk.PhotoImage(sgi)
        self.backgroundLabel = Label(self.tk, image=self.backgroundImage)
        self.backgroundLabel.place(x=0, y=0)
        self.tempBackground = ImageTk.PhotoImage(self.images_background[0])
        self.background = self.canvas.create_image(0, 0, image=self.tempBackground, anchor='nw')

    def hitSound(self):
        pygame.init()
        pygame.mixer.music.load('cc.wav')
        pygame.mixer.music.play(loops=0)

    def winSound(self):
        pygame.init()
        pygame.mixer.music.load('f.wav')
        pygame.mixer.music.play(loops=0)


g = Game()


# Che do 1 nguoi choi
def gameSingle():
    # Xoa background menu
    g.backgroundLabel.destroy()

    class Ball:
        def __init__(self, canvas, paddle, score):
            self.canvas = canvas
            self.paddle = paddle
            self.score = score
            self.images_ball = [
                Image.open('ball_image.png'),
                Image.open('ball_glow_image.png')
            ]
            self.sgi = ImageTk.PhotoImage(self.images_ball[0])
            self.id = self.canvas.create_image(280, 180, anchor='nw', image=self.sgi)
            starts = [-3, -2, -1, 1, 2, 3]
            random.shuffle(starts)
            self.x = starts[0]
            self.y = -8
            self.last_time = time.time()
            self.canvas_height = self.canvas.winfo_height()
            self.canvas_width = self.canvas.winfo_width()
            self.hit_bottom = False

        def hit_paddle(self, pos):
            paddle_pos = self.canvas.coords(self.paddle.id)
            paddle_pos.append(paddle_pos[0] + 100)
            paddle_pos.append(paddle_pos[1] + 10)
            if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
                if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                    g.hitSound()
                    if self.paddle.x != 0:
                        self.x += self.paddle.x
                    else:
                        self.x += 1
                    self.score.hit()
                    return True
            return False

        def draw(self):
            self.canvas.move(self.id, self.x, self.y)
            pos = self.canvas.coords(self.id)
            pos.append(pos[0] + 27)
            pos.append(pos[1] + 27)
            if pos[1] <= 37:
                g.tempBackground = ImageTk.PhotoImage(g.images_background[2])
                g.canvas.itemconfig(g.background, image=g.tempBackground)
                self.y = 4 + self.paddle.i
                self.paddle.i += 0.1
                if self.y >= 10:
                    self.y = 10
                # print(self.y)
            if pos[3] >= self.canvas_height - 37:
                g.tempBackground = ImageTk.PhotoImage(g.images_background[4])
                g.canvas.itemconfig(g.background, image=g.tempBackground)
            if pos[0] <= 10:
                g.tempBackground = ImageTk.PhotoImage(g.images_background[1])
                g.canvas.itemconfig(g.background, image=g.tempBackground)
                self.x = random.randint(1, 9)
            if pos[2] >= self.canvas_width - 10:
                g.tempBackground = ImageTk.PhotoImage(g.images_background[3])
                g.canvas.itemconfig(g.background, image=g.tempBackground)
                self.x = random.randint(-9, -1)
            if self.hit_paddle(pos) == True:
                # Bong phat sang va thanh do phat sang
                self.sgi = ImageTk.PhotoImage(self.images_ball[1])
                self.canvas.itemconfig(self.id, image=self.sgi)
                self.last_time = time.time()
                self.paddle.sgi = ImageTk.PhotoImage(self.paddle.images_paddle[1])
                self.canvas.itemconfig(self.paddle.id, image=self.paddle.sgi)
                self.y = -4 - self.paddle.i
                self.paddle.i += 0.1
                if self.y <= -10:
                    self.y = -10

            if self.y < 0:
                if time.time() - self.last_time > 0.3:
                    self.sgi = ImageTk.PhotoImage(self.images_ball[0])
                    self.canvas.itemconfig(self.id, image=self.sgi)
                    self.paddle.sgi = ImageTk.PhotoImage(self.paddle.images_paddle[0])
                    self.canvas.itemconfig(self.paddle.id, image=self.paddle.sgi)

            if pos[3] >= self.canvas_height:
                self.hit_bottom = True

    class Paddle:
        def __init__(self, canvas):
            self.canvas = canvas
            self.i = 0.1
            self.images_paddle = [
                Image.open('paddle_image.png'),
                Image.open('paddle_glow_image.png')
            ]
            self.sgi = ImageTk.PhotoImage(self.images_paddle[0])
            self.id = self.canvas.create_image(250, 340, anchor='nw', image=self.sgi)
            self.x = 0
            self.canvas_width = self.canvas.winfo_width()
            self.canvas.bind_all('<KeyPress-a>', self.turn_left)
            self.canvas.bind_all('<KeyPress-d>', self.turn_right)

        def draw(self):
            self.canvas.move(self.id, self.x, 0)
            pos = self.canvas.coords(self.id)
            pos.append(pos[0] + 100)
            pos.append(pos[1] + 10)
            if pos[0] <= 20:
                self.x = 0
                self.canvas.unbind_all('<KeyPress-a>')
            if pos[0] > 20:
                self.canvas.bind_all('<KeyPress-a>', self.turn_left)

            if pos[2] >= self.canvas_width - 20:
                self.x = 0
                self.canvas.unbind_all('<KeyPress-d>')
            if pos[2] < self.canvas_width - 20:
                self.canvas.bind_all('<KeyPress-d>', self.turn_right)

        def turn_left(self, ev):
            self.x = -8

        def turn_right(self, ev):
            self.x = 8

    class Score:
        def __init__(self, canvas, color):
            self.score = 0
            self.canvas = canvas
            self.id = canvas.create_text(50, 10, text='Score: %s' % self.score,
                                         font=('Helvetica', 16), fill=color)

        def hit(self):
            self.score += 10
            self.canvas.itemconfig(self.id, text='Score: %s' % self.score)

    def restartGame():
        nutRestart.destroy()
        nutQuit.destroy()
        nutReturnMenu.destroy()
        g.canvas.delete('all')
        g.background = g.canvas.create_image(0, 0, image=g.tempBackground, anchor='nw')
        gameSingle()

    def returnMenu():
        nutRestart.destroy()
        nutQuit.destroy()
        nutReturnMenu.destroy()
        g.canvas.delete('all')
        g.backgroundLabel = Label(g.tk, image=g.backgroundImage)
        g.backgroundLabel.place(x=0, y=0)
        menuButtons()
        g.background = g.canvas.create_image(0, 0, image=g.tempBackground, anchor='nw')

    def startgame(n):
        global nutRestart
        global nutQuit
        global nutReturnMenu
        paddle = Paddle(g.canvas)
        score = Score(g.canvas, 'white')
        ball = Ball(g.canvas, paddle, score)
        nut1.destroy()
        nut2.destroy()
        nut3.destroy()
        game_over = g.canvas.create_text(300, 100, text='Game Over',
                                         font=('Helvetica', 24),
                                         fill='red', state='hidden')

        while 1:
            if ball.hit_bottom == False:
                ball.draw()
                paddle.draw()
            if ball.hit_bottom == True:
                # g.winSound()
                nutRestart = Button(g.tk, image=g.restartPic, command=restartGame)
                nutRestart.place(x=150, y=200, anchor='center')
                nutReturnMenu = Button(g.tk, image=g.menuPic, command=returnMenu)
                nutReturnMenu.place(x=300, y=200, anchor='center')
                nutQuit = Button(g.tk, image=g.quitPic, command=quit)
                nutQuit.place(x=450, y=200, anchor='center')
                time.sleep(0)
                g.canvas.itemconfig(game_over, state='normal')
                break

            g.tk.update()
            time.sleep(n)

    nut1 = Button(g.tk, image=g.pic_speed_1, command=lambda: startgame(0.03))
    nut1.place(x=150, y=200, anchor='center')
    nut2 = Button(g.tk, image=g.pic_speed_2, command=lambda: startgame(0.02))
    nut2.place(x=300, y=200, anchor='center')
    nut3 = Button(g.tk, image=g.pic_speed_3, command=lambda: startgame(0.01))
    nut3.place(x=450, y=200, anchor='center')


def gamemulti():
    g.backgroundLabel.destroy()

    class Ball:
        def __init__(self, canvas, paddle, paddle2, score1, score2):
            self.canvas = canvas
            self.paddle = paddle
            self.paddle2 = paddle2
            self.score1 = score1
            self.score2 = score2
            self.images_ball = [
                Image.open('ball_image.png'),
                Image.open('ball_glow_image.png')
            ]
            self.sgi = ImageTk.PhotoImage(self.images_ball[0])
            self.id = self.canvas.create_image(280, 180, anchor='nw', image=self.sgi)
            starts_x = [0, -2, -1, 0, 1, 2, 3]
            random.shuffle(starts_x)
            starts_y = [-4, 4]
            random.shuffle(starts_y)
            self.x = starts_x[0]
            self.y = starts_y[0]
            self.last_time = time.time()
            self.canvas_height = self.canvas.winfo_height()
            self.canvas_width = self.canvas.winfo_width()
            self.hit_bottom = False
            self.hit_top = False

        def hit_paddle(self, pos):
            paddle_pos = self.canvas.coords(self.paddle.id)
            paddle_pos.append(paddle_pos[0] + 100)
            paddle_pos.append(paddle_pos[1] + 10)
            if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
                if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                    g.hitSound()
                    self.score2.hit()
                    return True
            return False

        def hit_paddle2(self, pos):
            paddle_pos = self.canvas.coords(self.paddle2.id)
            paddle_pos.append(paddle_pos[0] + 100)
            paddle_pos.append(paddle_pos[1] + 10)
            if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
                if pos[1] <= paddle_pos[3] and pos[1] >= paddle_pos[1]:
                    self.x += self.paddle2.x
                    self.score1.hit()
                    g.hitSound()
                    return True
            return False

        def draw(self):
            self.canvas.move(self.id, self.x, self.y)
            pos = self.canvas.coords(self.id)
            pos.append(pos[0] + 27)
            pos.append(pos[1] + 27)
            if pos[1] <= 37:
                g.tempBackground = ImageTk.PhotoImage(g.images_background[2])
                g.canvas.itemconfig(g.background, image=g.tempBackground)
            if pos[3] >= self.canvas_height - 37:
                g.tempBackground = ImageTk.PhotoImage(g.images_background[4])
                g.canvas.itemconfig(g.background, image=g.tempBackground)
            if pos[0] <= 10:
                g.tempBackground = ImageTk.PhotoImage(g.images_background[1])
                g.canvas.itemconfig(g.background, image=g.tempBackground)
                self.x = 4
            if pos[2] >= self.canvas_width - 10:
                g.tempBackground = ImageTk.PhotoImage(g.images_background[3])
                g.canvas.itemconfig(g.background, image=g.tempBackground)
                self.x = -4
            # Lam qua bong phat sang va chuyen huong bong
            if self.hit_paddle(pos) == True:
                self.sgi = ImageTk.PhotoImage(self.images_ball[1])
                self.canvas.itemconfig(self.id, image=self.sgi)
                self.last_time = time.time()
                self.paddle.sgi = ImageTk.PhotoImage(self.paddle.images_paddle[1])
                self.canvas.itemconfig(self.paddle.id, image=self.paddle.sgi)
                self.y = -4
            if self.hit_paddle2(pos) == True:
                self.sgi = ImageTk.PhotoImage(self.images_ball[1])
                self.canvas.itemconfig(self.id, image=self.sgi)
                self.last_time = time.time()
                self.paddle2.sgi = ImageTk.PhotoImage(self.paddle2.images_paddle[3])
                self.canvas.itemconfig(self.paddle2.id, image=self.paddle2.sgi)
                self.y = 4
            # Tat anh sang qua bong
            if self.y < 0:
                if time.time() - self.last_time > 0.3:
                    self.sgi = ImageTk.PhotoImage(self.images_ball[0])
                    self.canvas.itemconfig(self.id, image=self.sgi)
                    self.paddle.sgi = ImageTk.PhotoImage(self.paddle.images_paddle[0])
                    self.canvas.itemconfig(self.paddle.id, image=self.paddle.sgi)
            if self.y > 0:
                if time.time() - self.last_time > 0.3:
                    self.sgi = ImageTk.PhotoImage(self.images_ball[0])
                    self.canvas.itemconfig(self.id, image=self.sgi)
                    self.paddle2.sgi = ImageTk.PhotoImage(self.paddle2.images_paddle[2])
                    self.canvas.itemconfig(self.paddle2.id, image=self.paddle2.sgi)

            if pos[3] >= self.canvas_height - 10:
                self.hit_bottom = True
            if pos[1] <= 10:
                self.hit_top = True

    class Paddle:
        def __init__(self, canvas):
            self.canvas = canvas
            self.images_paddle = [
                Image.open('blue_paddle_image.png'),
                Image.open('blue_paddle_glow_image.png'),
                Image.open('red_paddle_image.png'),
                Image.open('red_paddle_glow_image.png')
            ]
            self.i = 0.1

    class Player1Paddle(Paddle):
        def __init__(self, canvas):
            Paddle.__init__(self, canvas)
            self.sgi = ImageTk.PhotoImage(self.images_paddle[0])
            self.id = self.canvas.create_image(250, 350, anchor='nw', image=self.sgi)
            self.x = 0
            self.canvas_width = self.canvas.winfo_width()
            self.canvas.bind_all('<KeyPress-a>', self.turn_left)
            self.canvas.bind_all('<KeyPress-d>', self.turn_right)

        def draw(self):
            self.canvas.move(self.id, self.x, 0)
            pos = self.canvas.coords(self.id)
            pos.append(pos[0] + 100)
            pos.append(pos[1] + 10)
            # print(pos)
            if pos[0] <= 0:
                self.x = 0
                self.canvas.unbind_all('<KeyPress-a>')
            if pos[0] > 0:
                self.canvas.bind_all('<KeyPress-a>', self.turn_left)

            if pos[2] >= self.canvas_width:
                self.x = 0
                self.canvas.unbind_all('<KeyPress-d>')
            if pos[2] < self.canvas_width:
                self.canvas.bind_all('<KeyPress-d>', self.turn_right)

        def turn_left(self, ev):
            self.x = -2

        def turn_right(self, ev):
            self.x = 2

    class Player2Paddle(Paddle):
        def __init__(self, canvas):
            Paddle.__init__(self, canvas)
            self.sgi = ImageTk.PhotoImage(self.images_paddle[2])
            self.id = self.canvas.create_image(250, 40, anchor='nw', image=self.sgi)
            self.x = 0
            self.canvas_width = self.canvas.winfo_width()
            self.canvas.bind_all('<KeyPress-Left>', self.turn_left2)
            self.canvas.bind_all('<KeyPress-Right>', self.turn_right2)

        def draw(self):
            self.canvas.move(self.id, self.x, 0)
            pos = self.canvas.coords(self.id)
            pos.append(pos[0] + 100)
            pos.append(pos[1] + 10)
            if pos[0] <= 0:
                self.x = 0
                self.canvas.unbind_all('<KeyPress-Left>')
            if pos[0] > 0:
                self.canvas.bind_all('<KeyPress-Left>', self.turn_left2)
            if pos[2] >= self.canvas_width:
                self.x = 0
                self.canvas.unbind_all('<KeyPress-Right>')
            if pos[2] < self.canvas_width:
                self.canvas.bind_all('<KeyPress-Right>', self.turn_right2)

        def turn_left2(self, evt):
            self.x = -2

        def turn_right2(self, evt):
            self.x = 2

    class Score:
        def __init__(self, canvas, color, x, y, text):
            self.text = text
            self.score = 0
            self.canvas = canvas
            self.id = canvas.create_text(x, y, text='Score %s: %s' % (text, self.score),
                                         font=('Helvetica', 14), fill=color)

        def hit(self):
            self.score += 10
            self.canvas.itemconfig(self.id, text='Score %s: %s' % (self.text, self.score))

    def restartGame():
        nutRestart.destroy()
        nutQuit.destroy()
        nutReturnMenu.destroy()
        g.canvas.delete('all')
        g.background = g.canvas.create_image(0, 0, image=g.tempBackground, anchor='nw')
        gamemulti()

    def returnMenu():
        nutRestart.destroy()
        nutQuit.destroy()
        nutReturnMenu.destroy()
        g.canvas.delete('all')
        g.backgroundLabel = Label(g.tk, image=g.backgroundImage)
        g.backgroundLabel.place(x=0, y=0)
        menuButtons()
        g.background = g.canvas.create_image(0, 0, image=g.tempBackground, anchor='nw')

    def startgame(n):
        global nutRestart
        global nutQuit
        global nutReturnMenu
        paddle = Player1Paddle(g.canvas)
        paddle2 = Player2Paddle(g.canvas)
        score1 = Score(g.canvas, 'red', 70, 10, 'Red')
        score2 = Score(g.canvas, 'blue', 70, 385, 'Blue')
        ball = Ball(g.canvas, paddle, paddle2, score1, score2)
        red_win = g.canvas.create_text(300, 100, text='Red win',
                                       font=('Helvetica', 24),
                                       fill='red', state='hidden')
        blue_win = g.canvas.create_text(300, 100, text='Blue win',
                                        font=('Helvetica', 24),
                                        fill='blue', state='hidden')
        nut1.destroy()
        nut2.destroy()
        nut3.destroy()
        while 1:
            if ball.hit_bottom == False and ball.hit_top == False:
                ball.draw()
                paddle.draw()
                paddle2.draw()
            if ball.hit_bottom == True:
                g.winSound()
                nutRestart = Button(g.tk, image=g.restartPic, command=restartGame)
                nutRestart.place(x=150, y=200, anchor='center')
                nutReturnMenu = Button(g.tk, image=g.menuPic, command=returnMenu)
                nutReturnMenu.place(x=300, y=200, anchor='center')
                nutQuit = Button(g.tk, image=g.quitPic, command=quit)
                nutQuit.place(x=450, y=200, anchor='center')
                time.sleep(0)
                g.canvas.itemconfig(red_win, state='normal')
                break
            if ball.hit_top == True:
                g.winSound()
                nutRestart = Button(g.tk, image=g.restartPic, command=restartGame)
                nutRestart.place(x=150, y=200, anchor='center')
                nutReturnMenu = Button(g.tk, image=g.menuPic, command=returnMenu)
                nutReturnMenu.place(x=300, y=200, anchor='center')
                nutQuit = Button(g.tk, image=g.quitPic, command=quit)
                nutQuit.place(x=450, y=200, anchor='center')
                time.sleep(0)
                g.canvas.itemconfig(blue_win, state='normal')
                break
            g.tk.update_idletasks()
            g.tk.update()
            time.sleep(n)

    nut1 = Button(g.tk, image=g.pic_speed_1, command=lambda: startgame(0.03))
    nut1.place(x=150, y=200, anchor='center')
    nut2 = Button(g.tk, image=g.pic_speed_2, command=lambda: startgame(0.02))
    nut2.place(x=300, y=200, anchor='center')
    nut3 = Button(g.tk, image=g.pic_speed_3, command=lambda: startgame(0.01))
    nut3.place(x=450, y=200, anchor='center')


# Open Image
startGameImage = Image.open('single_player_button.png')
newPic = ImageTk.PhotoImage(startGameImage)
startGameImage2 = Image.open('multi_player_button.png')
newPic2 = ImageTk.PhotoImage(startGameImage2)
open_exit_pic = Image.open('exit_game_button.png')
exitPic = ImageTk.PhotoImage(open_exit_pic)
open_credit_pic = Image.open('credit_button.png')
creditPic = ImageTk.PhotoImage(open_credit_pic)


def menuButtons():
    # Singleplayer button
    nut1 = Button(g.tk, image=newPic, command=lambda: [hide(), gameSingle()])
    nut1.place(x=300, y=80, anchor='center')
    # Multiplayer Button
    nut = Button(g.tk, image=newPic2, command=lambda: [hide(), gamemulti()])
    nut.place(x=300, y=160, anchor='center')
    # Credits Button
    nut_credit = Button(g.tk, image=creditPic, command=lambda: credits())
    nut_credit.place(x=300, y=240, anchor='center')
    # Exit Button
    nut_exit = Button(g.tk, image=exitPic, command=g.tk.quit)
    nut_exit.place(x=300, y=320, anchor='center')

    def hide():
        nut.destroy()
        nut1.destroy()
        nut_credit.destroy()
        nut_exit.destroy()

    def credits():
        g.creditLabel = Label(g.tk, image=g.crepic)
        g.creditLabel.place(x=150, y=100)
        global nut_x
        nut_x = Button(g.tk, image=g.x_button_pic, command=quit_credits)
        nut_x.place(x=480, y=85, anchor='center')

    def quit_credits():
        g.creditLabel.destroy()
        nut_x.destroy()


menuButtons()
g.tk.mainloop()
