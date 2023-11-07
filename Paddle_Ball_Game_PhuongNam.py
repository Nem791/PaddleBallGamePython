from tkinter import *
import pygame
import os
from PIL import ImageTk, Image

from multi_player import game_multi
from single_player import game_single

image_dir = "img"
audio_dir = "audio"


class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Paddle Ball Game Ball")
        self.tk.resizable(0, 0)
        self.tk.iconbitmap(os.path.join(image_dir, 'Paddle_Ball_Game_Icon.ico'))
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=600, height=400, bd=0, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()

        # Load Images
        self.load_images()

        # Create background label
        self.backgroundLabel = Label(self.tk, image=self.backgroundImage)
        self.backgroundLabel.place(x=0, y=0)
        self.background = self.canvas.create_image(0, 0, image=self.tempBackground, anchor='nw')

    def load_images(self):
        # Load various images
        self.backgroundImage = ImageTk.PhotoImage(Image.open(os.path.join(image_dir, 'menu_glow.png')))
        self.cre = Image.open(os.path.join(image_dir, 'credit.png'))
        self.x_button = Image.open(os.path.join(image_dir, 'x.png'))
        self.x_button_pic = ImageTk.PhotoImage(self.x_button)
        self.speed_1 = Image.open(os.path.join(image_dir, 'Speed1.png'))
        self.pic_speed_1 = ImageTk.PhotoImage(self.speed_1)
        self.speed_2 = Image.open(os.path.join(image_dir, 'Speed2.png'))
        self.pic_speed_2 = ImageTk.PhotoImage(self.speed_2)
        self.speed_3 = Image.open(os.path.join(image_dir, 'Speed3.png'))
        self.pic_speed_3 = ImageTk.PhotoImage(self.speed_3)
        self.images_background = [
            Image.open(os.path.join(image_dir, 'Background.png')),
            Image.open(os.path.join(image_dir, 'Background-Glow-Left.png')),
            Image.open(os.path.join(image_dir, 'Background-Glow-Top.png')),
            Image.open(os.path.join(image_dir, 'Background-Glow-Right.png')),
            Image.open(os.path.join(image_dir, 'Background-Glow-Bottom.png'))
        ]
        self.tempRestartPic = Image.open(os.path.join(image_dir, 'restartIconButton.png'))
        self.restartPic = ImageTk.PhotoImage(self.tempRestartPic)
        self.tempMenuPic = Image.open(os.path.join(image_dir, 'menuIconButton.png'))
        self.menuPic = ImageTk.PhotoImage(self.tempMenuPic)
        self.tempQuitPic = Image.open(os.path.join(image_dir, 'quitIconButton.png'))
        self.quitPic = ImageTk.PhotoImage(self.tempQuitPic)
        self.crepic = ImageTk.PhotoImage(self.cre)
        self.tempBackground = ImageTk.PhotoImage(self.images_background[0])

    def hitSound(self):
        # Initialize pygame and play the hit sound
        pygame.init()
        pygame.mixer.music.load(os.path.join(audio_dir, 'cc.wav'))
        pygame.mixer.music.play(loops=0)

    def winSound(self):
        # Initialize pygame and play the win sound
        pygame.init()
        pygame.mixer.music.load(os.path.join(audio_dir, 'f.wav'))
        pygame.mixer.music.play(loops=0)


g = Game()

# Open Image
startGameImage = Image.open(os.path.join(image_dir, 'single_player_button.png'))
newPic = ImageTk.PhotoImage(startGameImage)
startGameImage2 = Image.open(os.path.join(image_dir, 'multi_player_button.png'))
newPic2 = ImageTk.PhotoImage(startGameImage2)
open_exit_pic = Image.open(os.path.join(image_dir, 'exit_game_button.png'))
exitPic = ImageTk.PhotoImage(open_exit_pic)
open_credit_pic = Image.open(os.path.join(image_dir, 'credit_button.png'))
creditPic = ImageTk.PhotoImage(open_credit_pic)


def menu_buttons():
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

    # Singleplayer button
    nut1 = Button(g.tk, image=newPic, command=lambda: [hide(), game_single(g, menu_buttons)])
    nut1.place(x=300, y=80, anchor='center')

    # Multiplayer Button
    nut = Button(g.tk, image=newPic2, command=lambda: [hide(), game_multi(g, menu_buttons)])
    nut.place(x=300, y=160, anchor='center')

    # Credits Button
    nut_credit = Button(g.tk, image=creditPic, command=credits)
    nut_credit.place(x=300, y=240, anchor='center')

    # Exit Button
    nut_exit = Button(g.tk, image=exitPic, command=g.tk.quit)
    nut_exit.place(x=300, y=320, anchor='center')


menu_buttons()
g.tk.mainloop()
