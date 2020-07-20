import tkinter as tk
from PIL import Image, ImageTk
from random import randint

MOVE_INCREMENT = 20
moves_per_second = 15
GAME_SPEED = 1000 // moves_per_second

# object oriented programming wiht classes
class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, background="black", highlightthickness=0)
        
        # using tuple values to represent each square of snake
        self.load_assets()
        self.play_button_screen()
        self.high_score = 0
        self.scores = []

    #loades images of the snake and the food
    def load_assets(self):
        try: 
            self.snake_body_image = Image.open("./assets/snake.png")
            self.snake_body = ImageTk.PhotoImage(self.snake_body_image)

            self.food_image = Image.open("./assets/food.png")
            self.food = ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            print('error')
            root.destroy()

    def play_button_screen(self):
        self.play_button = tk.Button(
            text="Press to play",
            fg="green",
            command=lambda: self.play()
        )
        self.play_button.pack(side='bottom')



    def play(self):
        self.delete(tk.ALL)
        self.play_button.destroy()
        self.snake_positions = [(100,100), (80, 100), (60, 100)]
        self.food_position = self.set_new_food_position()
        self.score = 0
        self.direction = 'Right'
        #runs a function when key is pressed
        self.bind_all("<Key>", self.on_key_press)
        self.create_objects()
        self.after(GAME_SPEED, self.perform_actions)

    def create_objects(self):
        for x_position, y_position in self.snake_positions:
            #creating body of snake, tag allows us to retrieve image
            self.create_image(x_position, y_position, image=self.snake_body, tag="snake")
        
        #the astrisk here destructs the food_position coordinate and passes each x and y coordinate as separate values
        #REMEBER the indent because not in snake position
        self.create_image(*self.food_position, image=self.food, tag='food')

            #displaying score
        self.create_text(
            100, 12, text=f"Score: {self.score} (speed: {moves_per_second})", tag='score', fill='#fff', font=('TkDefaultFont', 14)
        )

            #create boundaries for game
        self.create_rectangle(7, 27, 593, 613, outline="#525d69")
    
    def move_snake(self):
        head_x_position, head_y_position = self.snake_positions[0]

        if self.direction == "Left":
            new_head_position = (head_x_position - MOVE_INCREMENT, head_y_position)
        elif self.direction == "Right":
            new_head_position = (head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction == "Down":
            new_head_position = (head_x_position, head_y_position + MOVE_INCREMENT)
        elif self.direction == "Up":
            new_head_position = (head_x_position, head_y_position - MOVE_INCREMENT)

        self.snake_positions = [new_head_position] + self.snake_positions[:-1]

        #creates tupple with tage and corresponding position
        for segment, position in zip(self.find_withtag("snake"), self.snake_positions):
            self.coords(segment, position)

    def perform_actions(self):
        if self.check_collisions():
            self.end_game()
            return
        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED, self.perform_actions) #here pass in function name not call so it reexcecutes the function and doesn't just retunre return value

    def check_collisions(self):
        head_x_position, head_y_position = self.snake_positions[0]

        return(
            head_x_position in (0, 600)
            or head_y_position in (20, 620)
            or (head_x_position, head_y_position) in self.snake_positions[1:]
        )

    def on_key_press(self, e):
        new_direction = e.keysym 
        all_directions = ("Up", 'Down', 'Left', 'Right')
        opposites = ({'Up', 'Down'}, {'Left', 'Right'})
        #use sets for opposites because sets don't care about order and don't have order
        if (
            new_direction in all_directions
            and {new_direction, self.direction} not in opposites
        ):
            self.direction = new_direction

    def check_food_collision(self):
        if self.snake_positions[0] == self.food_position:
            self.score += 1
            self.snake_positions.append(self.snake_positions[-1])

            if self.score % 5 == 0:
                global moves_per_second 
                moves_per_second += 1 

            #creating new image of snake body
            self.create_image(*self.snake_positions[-1], image=self.snake_body, tag='snake')
            
            # since we have collided, set new food position
            self.food_position = self.set_new_food_position()
            self.coords(self.find_withtag("food"), self.food_position)
            #update score
            score = self.find_withtag("score")
            self.itemconfigure(score, text=f"Score: {self.score} (speed: {moves_per_second})", tag="score")
    
    def set_new_food_position(self):
        # need position of food to not be under snake
        # so keep finding new position for food until it is not under snake, then break from loop
        while True:
            x_position = randint(1, 29) * MOVE_INCREMENT 
            y_position = randint(3, 30) * MOVE_INCREMENT
            food_position = (x_position, y_position)
            if food_position not in self.snake_positions:
                return food_position

    def end_game(self):
        self.delete(tk.ALL)
        if self.score > self.high_score:
            self.high_score = self.score
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"Game over! You scored {self.score}!\nYour high score is {self.high_score}!", 
            fill="#fff",
            font=("TkDefaultFont", 24)
        )
        self.enter_name = tk.Button(
            text="Press to enter name",
            fg="red",
            command=lambda: self.enter_high_score()
        )
        self.enter_name.pack(side='bottom')

    def enter_high_score(self):
        self.enter_name.destroy()
        #self.tk.Label(text=f"Enter name:")
        self.enter_button = tk.Button(
            text="Enter",
            fg="red",
            command=lambda: self.save_scores()
        )
        self.name = tk.Entry()
        self.name.pack()
        self.enter_button.pack()
    
    def save_scores(self):
        self.enter_button.destroy()
        self.scores.append((self.name.get(), self.score))
        self.name.destroy()
        self.high_score_button = tk.Button(
            text="Press to see your high scores",
            fg="blue",
            command=lambda: self.show_high_scores()
        )

        self.high_score_button.pack(side='bottom')


    def show_high_scores(self):
        self.delete(tk.ALL)
        self.create_text(
            self.winfo_width() / 2,
            self.winfo_height() / 2,
            text=f"High scores: {self.scores}",
            fill="#fff",
            font=("TkDefaultFont", 24)
        )
        self.high_score_button.destroy()
        self.after(GAME_SPEED, self.play_button_screen)




# creates a main window for the application
root = tk.Tk()
root.title('Snake')
root.resizable(False, False)

game = Snake()
game.pack()

# runs main app
root.mainloop()
