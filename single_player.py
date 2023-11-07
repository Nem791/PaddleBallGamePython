from tkinter import *
import random
import time
import os
from PIL import ImageTk, Image

image_dir = "img"


# Single player
def game_single(g, menu_buttons):
    # Xoa background menu
    g.backgroundLabel.destroy()

    class Ball:
        def __init__(self, canvas, paddle, score):
            # Initialize the Ball object
            self.canvas = canvas
            self.paddle = paddle
            self.score = score

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
            starts = [-3, -2, -1, 1, 2, 3]
            random.shuffle(starts)
            self.x = starts[0]
            self.y = -8
            self.last_time = time.time()
            self.canvas_height = self.canvas.winfo_height()
            self.canvas_width = self.canvas.winfo_width()
            self.hit_bottom = False

        def hit_paddle(self, pos):
            # Check if the ball hits the paddle
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
            # Move the ball and handle collisions
            self.canvas.move(self.id, self.x, self.y)
            pos = self.canvas.coords(self.id)
            pos.append(pos[0] + 27)
            pos.append(pos[1] + 27)

            if pos[1] <= 37:
                # Handle collision with the top of the canvas
                g.tempBackground = ImageTk.PhotoImage(g.images_background[2])
                g.canvas.itemconfig(g.background, image=g.tempBackground)
                self.y = 4 + self.paddle.i
                self.paddle.i += 0.1
                if self.y >= 10:
                    self.y = 10

            if pos[3] >= self.canvas_height - 37:
                # Handle collision with the bottom of the canvas
                g.tempBackground = ImageTk.PhotoImage(g.images_background[4])
                g.canvas.itemconfig(g.background, image=g.tempBackground)

            if pos[0] <= 10:
                # Handle collision with the left wall
                g.tempBackground = ImageTk.PhotoImage(g.images_background[1])
                g.canvas.itemconfig(g.background, image=g.tempBackground)
                self.x = random.randint(1, 9)

            if pos[2] >= self.canvas_width - 10:
                # Handle collision with the right wall
                g.tempBackground = ImageTk.PhotoImage(g.images_background[3])
                g.canvas.itemconfig(g.background, image=g.tempBackground)
                self.x = random.randint(-9, -1)

            if self.hit_paddle(pos):
                # Handle collision with the paddle
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
                # Reset ball and paddle glow
                if time.time() - self.last_time > 0.3:
                    self.sgi = ImageTk.PhotoImage(self.images_ball[0])
                    self.canvas.itemconfig(self.id, image=self.sgi)
                    self.paddle.sgi = ImageTk.PhotoImage(self.paddle.images_paddle[0])
                    self.canvas.itemconfig(self.paddle.id, image=self.paddle.sgi)

            if pos[3] >= self.canvas_height:
                # Check if the ball hit the bottom
                self.hit_bottom = True

    class Paddle:
        def __init__(self, canvas):
            # Initialize the Paddle object
            self.canvas = canvas
            self.i = 0.1

            # Load paddle images
            self.load_images()

            # Create the paddle on the canvas
            self.create_paddle()

            # Initialize paddle's attributes
            self.init_paddle_attributes()

            # Bind keys for paddle movement
            self.bind_movement_keys()

        def load_images(self):
            # Load paddle images
            self.images_paddle = [
                Image.open(os.path.join(image_dir, 'paddle_image.png')),
                Image.open(os.path.join(image_dir, 'paddle_glow_image.png'))
            ]
            self.sgi = ImageTk.PhotoImage(self.images_paddle[0])

        def create_paddle(self):
            # Create the paddle on the canvas
            self.id = self.canvas.create_image(250, 340, anchor='nw', image=self.sgi)
            self.x = 0

        def init_paddle_attributes(self):
            # Initialize paddle's attributes
            self.canvas_width = self.canvas.winfo_width()

        def bind_movement_keys(self):
            # Bind keys for paddle movement
            self.canvas.bind_all('<KeyPress-a>', self.turn_left)
            self.canvas.bind_all('<KeyPress-d>', self.turn_right)

        def draw(self):
            # Move the paddle and handle boundaries
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
            # Turn the paddle left
            self.x = -8

        def turn_right(self, ev):
            # Turn the paddle right
            self.x = 8

    class Score:
        def __init__(self, canvas, color):
            # Initialize the Score object
            self.score = 0
            self.canvas = canvas

            # Create the score display on the canvas
            self.create_score_display(color)

        def create_score_display(self, color):
            # Create the score display on the canvas
            self.id = self.canvas.create_text(50, 10, text='Score: %s' % self.score,
                                              font=('Helvetica', 16), fill=color)

        def hit(self):
            # Increment the score and update the display
            self.score += 10
            self.canvas.itemconfig(self.id, text='Score: %s' % self.score)

    def restart_game():
        # Restart the game
        nut_restart.destroy()
        nut_quit.destroy()
        nut_return_menu.destroy()
        g.canvas.delete('all')
        g.background = g.canvas.create_image(0, 0, image=g.tempBackground, anchor='nw')
        game_single(g, menu_buttons)

    def return_menu():
        # Return to the main menu
        nut_restart.destroy()
        nut_quit.destroy()
        nut_return_menu.destroy()
        g.canvas.delete('all')
        g.backgroundLabel = Label(g.tk, image=g.backgroundImage)
        g.backgroundLabel.place(x=0, y=0)
        menu_buttons()
        g.background = g.canvas.create_image(0, 0, image=g.tempBackground, anchor='nw')

    def start_game(speed):
        # Start the game with the given speed
        global nut_restart, nut_quit, nut_return_menu
        paddle = Paddle(g.canvas)
        score = Score(g.canvas, 'white')
        ball = Ball(g.canvas, paddle, score)
        nut_1.destroy()
        nut_2.destroy()
        nut_3.destroy()
        game_over = g.canvas.create_text(300, 100, text='Game Over', font=('Helvetica', 24), fill='red', state='hidden')

        while True:
            if not ball.hit_bottom:
                ball.draw()
                paddle.draw()

            if ball.hit_bottom:
                # g.winSound()
                nut_restart = Button(g.tk, image=g.restartPic, command=restart_game)
                nut_restart.place(x=150, y=200, anchor='center')
                nut_return_menu = Button(g.tk, image=g.menuPic, command=return_menu)
                nut_return_menu.place(x=300, y=200, anchor='center')
                nut_quit = Button(g.tk, image=g.quitPic, command=quit)
                nut_quit.place(x=450, y=200, anchor='center')
                time.sleep(0)
                g.canvas.itemconfig(game_over, state='normal')
                break

            g.tk.update()
            time.sleep(speed)

    nut_1 = Button(g.tk, image=g.pic_speed_1, command=lambda: start_game(0.03))
    nut_1.place(x=150, y=200, anchor='center')
    nut_2 = Button(g.tk, image=g.pic_speed_2, command=lambda: start_game(0.02))
    nut_2.place(x=300, y=200, anchor='center')
    nut_3 = Button(g.tk, image=g.pic_speed_3, command=lambda: start_game(0.01))
    nut_3.place(x=450, y=200, anchor='center')
