"""
Worked on this code first and saved it seperately as I had a hard time getting this working how I wanted it to.
"""


import sys, logging, os, random, math, open_color, arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Stars"


class Singlestar(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/star.png", 0.1)
        self.center_y = random.randrange(0, SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(0, SCREEN_WIDTH)
        self.dx = 0
        self.dy = -(random.randint(2,6))
        if self.center_y >= SCREEN_HEIGHT:
            self.reset_pos()
        if self.center_y <= 0:
            self.reset_pos()
    
    def update(self):
        self.center_x += self.dx
        self.center_y += self.dy
        if self.center_y <= 0:
            self.reset_pos()
    
    def reset_pos(self):
        # Reset star to random position above screen
        self.center_y = random.randrange(SCREEN_HEIGHT-1, SCREEN_HEIGHT)
        self.center_x = random.randrange(0, SCREEN_WIDTH)
        

class Window(arcade.Window):
    """ Main application class. """
    
    def __init__(self, width, height, title):
        """
        Initializer
        :param width:
        :param height:
        """
        # Calls "__init__" of parent class (arcade.Window) to setup screen
        super().__init__(width, height, title)
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        # Sprite lists
        self.star_list = arcade.Sprite("assets/star.png", 1)

    def setup(self):
        """ Set up snowfall and initialize variables. """
        self.star_list = arcade.SpriteList()

        for i in range(50):
            # Create snowflake instance
            singlestar = Singlestar()
            # Add snowflake to snowflake list
            self.star_list.append(singlestar)

        # Don't show the mouse pointer
        self.set_mouse_visible(False)

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)
    
    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """
        for b in self.star_list:
            b.update() 
        
    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        for b in self.star_list:
            b.draw()



def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()