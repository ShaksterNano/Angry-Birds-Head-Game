from tkinter import *
import random
import time
import subprocess
subprocess.call('angry_birds.wav', shell=True)
# subprocess.Popen(['afplay', 'AngryBirds.wav']) # For Mac use this instead

class Ball:
    def __init__(self, game, paddle, color):
        self.game = game
        self.paddle = paddle
        self.pig = PhotoImage(file="bird.png")
        self.height = self.pig.height()
        self.width = self.pig.width()
        self.id = game.canvas.create_image(0, 0, image=self.pig, anchor='s')
        self.canvas_height = game.canvas.winfo_height()
        self.canvas_width = game.canvas.winfo_width()
        self.hit_bottom = False
        
    def hit_paddle(self, pos):
        paddle_pos = self.game.canvas.coords(self.paddle.id)
        if pos[0] >= paddle_pos[0] and pos[0] <= paddle_pos[0] + 128:
            if pos[1] >= paddle_pos[1] and pos[1] <= paddle_pos[1] + 10:
                self.game.score += 1
                return True
        return False
        
    def draw(self):
        self.game.canvas.move(self.id, self.x, self.y)
        pos = self.game.canvas.coords(self.id)
        
        if pos[1] <= 0 + self.height:
            self.y = 3
        if pos[1] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos) == True:
            self.y = -3
        if pos[0] <= self.width/2:
            self.x = 3
        if pos[0] >= self.canvas_width - self.width/2:
            self.x = -3
        
        self.game.canvas.itemconfig(self.game.score_display, text=("Score:", self.game.score))
        
class Paddle:
    def __init__(self, game, color):
        self.game = game
        self.bird = PhotoImage(file="pig.png")
        self.id = game.canvas.create_image(0, 0, image=self.bird, anchor='nw')
        game.canvas.move(self.id, 350, 400)
        self.x = 0
        self.canvas_width = game.canvas.winfo_width()
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        
    def draw(self):
        self.game.canvas.move(self.id, self.x, 0)
        pos = self.game.canvas.coords(self.id)
        if pos[0] <= 0 or pos[0] >= self.canvas_width - 128:
            self.x = 0
            
    def turn_left(self, evt):
        self.x = -6
        
    def turn_right(self, evt):
        self.x = 6

class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Angry Birds Head Game")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=800, height=600, bg='yellow', bd=0, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        
        self.canvas_width = 800
        self.canvas_height = 600
        
        self.score = 0
        self.score_display = self.canvas.create_text(720, 30, text=("Score:", self.score), font=("Comic Sans MS", 20), fill="black")

        self.message1 = self.canvas.create_text(400, 250, text='Game over', fill='red', font=('Comic Sans MS', 50))
        
        self.btn = Button(self.tk, text="Play Again", command = lambda: self.mainloop(paddle, ball))
        self.btn.place(x=700, y=550)
        
    def mainloop(self, paddle, ball):
        self.canvas.coords(ball.id, 400, 200)
        ball.hit_bottom = False
        starts = [-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        ball.x = starts[0]
        ball.y = -3
        self.score = 0

        self.canvas.itemconfig(self.score_display, text=("Score:", self.score))
        self.canvas.itemconfig(self.message1, state = "hidden")
        self.btn.config(state = "disabled")
        
        while 1:
            if ball.hit_bottom == False:
                ball.draw()
                paddle.draw()
            else:
                self.canvas.itemconfig(self.message1, state = "normal")
                self.btn.config(state = "active")            

            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)
            

            
g = Game()
paddle = Paddle(g, 'blue')
ball = Ball(g, paddle, 'red')
g.mainloop(paddle, ball)
