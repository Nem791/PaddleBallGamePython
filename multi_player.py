from tkinter import *
import random
import time
import os
from PIL import ImageTk, Image

image_dir = "img"


# Single player
def game_multi(g, menu_buttons):
    g.backgroundLabel.destroy()

    class Ball:
        def __init__(self, canvas, paddle, paddle2, score1, score2):
            # Initialize the Ball object
            self.canvas = canvas
            self.paddle = paddle
            self.paddle2 = paddle2
            self.score1 = score1
            self.score2 = score2

            # Load ball images
            self.load_images()

            # Create the ball on the canvas
            self.create_ball()

            # Initialize ball's attributes
            self.init_ball_attributes()

        def load_images(self):
            # Load ball images
            self.images_ball = [
                Image.open(os.path.join(image_dir, 'ball_image.png')),
                Image.open(os.path.join(image_dir, 'ball_glow_image.png'))
            ]
            self.sgi = ImageTk.PhotoImage(self.images_ball[0])

        def create_ball(self):
            # Create the ball on the canvas
            self.id = self.canvas.create_image(280, 180, anchor='nw', image=self.sgi)

        def init_ball_attributes(self):
            # Initialize ball's attributes
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
            # Check if the ball hits paddle 1
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
            # Check if the ball hits paddle 2
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
            # Move the ball and handle collisions
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

            # Handle collisions with paddles and change the ball's behavior
            if self.hit_paddle(pos):
                self.handle_paddle_collision(self.paddle, self.paddle.images_paddle[1], -4)

            if self.hit_paddle2(pos):
                self.handle_paddle_collision(self.paddle2, self.paddle2.images_paddle[3], 4)

            # Reset the ball and paddle glow
            self.reset_ball_and_paddle_glow()

            # Check if the ball hit the bottom or top
            if pos[3] >= self.canvas_height - 10:
                self.hit_bottom = True

            if pos[1] <= 10:
                self.hit_top = True

        def handle_paddle_collision(self, paddle, paddle_image, new_y):
            # Handle collision with a paddle
            self.sgi = ImageTk.PhotoImage(self.images_ball[1])
            self.canvas.itemconfig(self.id, image=self.sgi)
            self.last_time = time.time()
            paddle.sgi = ImageTk.PhotoImage(paddle_image)
            self.canvas.itemconfig(paddle.id, image=paddle.sgi)
            self.y = new_y

        def reset_ball_and_paddle_glow(self):
            # Reset ball and paddle glow
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

    class Paddle:
        def __init__(self, canvas):
            # Initialize the Paddle object
            self.canvas = canvas

            # Load paddle images
            self.load_images()

            # Initialize paddle's attributes
            self.i = 0.1

        def load_images(self):
            # Load paddle images
            self.images_paddle = [
                Image.open(os.path.join(image_dir, 'blue_paddle_image.png')),
                Image.open(os.path.join(image_dir, 'blue_paddle_glow_image.png')),
                Image.open(os.path.join(image_dir, 'red_paddle_image.png')),
                Image.open(os.path.join(image_dir, 'red_paddle_glow_image.png'))
            ]

    class Player1Paddle(Paddle):
        def __init__(self, canvas):
            # Initialize Player1Paddle object based on Paddle
            super().__init__(canvas)
            self.sgi = ImageTk.PhotoImage(self.images_paddle[0])
            self.id = self.canvas.create_image(250, 350, anchor='nw', image=self.sgi)
            self.x = 0
            self.canvas_width = self.canvas.winfo_width()
            self.canvas.bind_all('<KeyPress-a>', self.turn_left)
            self.canvas.bind_all('<KeyPress-d>', self.turn_right)

        def draw(self):
            # Draw the Player1Paddle
            self.canvas.move(self.id, self.x, 0)
            pos = self.canvas.coords(self.id)
            pos.append(pos[0] + 100)
            pos.append(pos[1] + 10)

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
            # Initialize Player2Paddle object based on Paddle
            super().__init__(canvas)
            self.sgi = ImageTk.PhotoImage(self.images_paddle[2])
            self.id = self.canvas.create_image(250, 40, anchor='nw', image=self.sgi)
            self.x = 0
            self.canvas_width = self.canvas.winfo_width()
            self.canvas.bind_all('<KeyPress-Left>', self.turn_left2)
            self.canvas.bind_all('<KeyPress-Right>', self.turn_right2)

        def draw(self):
            # Draw the Player2Paddle
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
            # Initialize the Score object
            self.text = text
            self.score = 0
            self.canvas = canvas

            # Create the score text on the canvas
            self.create_score_text(x, y, color)

        def create_score_text(self, x, y, color):
            # Create the score text on the canvas
            self.id = self.canvas.create_text(x, y, text='Score %s: %s' % (self.text, self.score),
                                              font=('Helvetica', 14), fill=color)

        def hit(self):
            # Increase the score and update the score text
            self.score += 10
            self.update_score_text()

        def update_score_text(self):
            # Update the score text on the canvas
            self.canvas.itemconfig(self.id, text='Score %s: %s' % (self.text, self.score))

    def restartGame():
        # Destroy buttons and reset the game for a restart
        nutRestart.destroy()
        nutQuit.destroy()
        nutReturnMenu.destroy()
        g.canvas.delete('all')
        g.background = g.canvas.create_image(0, 0, image=g.tempBackground, anchor='nw')
        game_multi(g, menu_buttons)

    def returnMenu():
        # Return to the main menu
        nutRestart.destroy()
        nutQuit.destroy()
        nutReturnMenu.destroy()
        g.canvas.delete('all')
        g.backgroundLabel = Label(g.tk, image=g.backgroundImage)
        g.backgroundLabel.place(x=0, y=0)
        menu_buttons()
        g.background = g.canvas.create_image(0, 0, image=g.tempBackground, anchor='nw')

    def startgame(n):
        # Initialize the game with player paddles, scores, and ball
        paddle = Player1Paddle(g.canvas)
        paddle2 = Player2Paddle(g.canvas)
        score1 = Score(g.canvas, 'red', 70, 10, 'Red')
        score2 = Score(g.canvas, 'blue', 70, 385, 'Blue')
        ball = Ball(g.canvas, paddle, paddle2, score1, score2)

        # Create text elements for win conditions
        red_win = g.canvas.create_text(300, 100, text='Red win', font=('Helvetica', 24), fill='red', state='hidden')
        blue_win = g.canvas.create_text(300, 100, text='Blue win', font=('Helvetica', 24), fill='blue', state='hidden')

        # Destroy speed selection buttons
        nut1.destroy()
        nut2.destroy()
        nut3.destroy()

        while 1:
            if ball.hit_bottom == False and ball.hit_top == False:
                ball.draw()
                paddle.draw()
                paddle2.draw()
            if ball.hit_bottom == True:
                # Handle Red player win
                g.winSound()
                create_restart_buttons()
                g.canvas.itemconfig(red_win, state='normal')
                break
            if ball.hit_top == True:
                # Handle Blue player win
                g.winSound()
                create_restart_buttons()
                g.canvas.itemconfig(blue_win, state='normal')
                break
            g.tk.update_idletasks()
            g.tk.update()
            time.sleep(n)

    def create_restart_buttons():
        # Create buttons for restart, return to the menu, and quit
        global nutRestart
        global nutQuit
        global nutReturnMenu
        nutRestart = Button(g.tk, image=g.restartPic, command=restartGame)
        nutRestart.place(x=150, y=200, anchor='center')
        nutReturnMenu = Button(g.tk, image=g.menuPic, command=returnMenu)
        nutReturnMenu.place(x=300, y=200, anchor='center')
        nutQuit = Button(g.tk, image=g.quitPic, command=quit)
        nutQuit.place(x=450, y=200, anchor='center')

    # Create speed selection buttons
    nut1 = Button(g.tk, image=g.pic_speed_1, command=lambda: startgame(0.03))
    nut1.place(x=150, y=200, anchor='center')
    nut2 = Button(g.tk, image=g.pic_speed_2, command=lambda: startgame(0.02))
    nut2.place(x=300, y=200, anchor='center')
    nut3 = Button(g.tk, image=g.pic_speed_3, command=lambda: startgame(0.01))
    nut3.place(x=450, y=200, anchor='center')
