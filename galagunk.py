import sys, logging, os, random, math, open_color, arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Galagunk"

NUM_ENEMIES = 5
STARTING_LOCATION = (400,100)
BULLET_DAMAGE = 10
ENEMY_HP = 100
HIT_SCORE = 10
KILL_SCORE = 100

class Bullet(arcade.Sprite):
    def __init__(self, position, velocity, damage):
        ''' 
        initializes the bullet
        Parameters: position: (x,y) tuple
            velocity: (dx, dy) tuple
            damage: int (or float)
        '''
        super().__init__("assets/bullet.png", 0.15)
        (self.center_x, self.center_y) = position
        (self.dx, self.dy) = velocity
        self.damage = damage

    def update(self):
        '''
        Moves the bullet
        '''
        self.center_x += self.dx
        self.center_y += self.dy

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/player.png", 0.1)
        (self.center_x, self.center_y) = STARTING_LOCATION

class Enemy(arcade.Sprite):
    def __init__(self, position):
        '''
        initializes a penguin enemy
        Parameter: position: (x,y) tuple
        '''
        super().__init__("assets/boss.png", 0.05)
        self.hp = ENEMY_HP
        (self.center_x, self.center_y) = position

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
        self.bullet_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.player = Player()
        self.score = 0
        self.l1_list = arcade.SpriteList()
        self.l2_list = arcade.SpriteList()
        self.l3_list = arcade.SpriteList()

    def setup(self):
        """ Set up starfall and initialize variables. """
        self.star_list = arcade.SpriteList()

        for i in range(50):
            # Create snowflake instance
            singlestar = Singlestar()
            # Add snowflake to snowflake list
            self.star_list.append(singlestar)
        
        for i in range(NUM_ENEMIES):
            x = 120 * (i+1) + 40
            y = 500
            enemy = Enemy((x,y))
            self.enemy_list.append(enemy)     

        # Don't show the mouse pointer
        self.set_mouse_visible(False)

        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

        self.l1_sprite = arcade.Sprite("assets/life1.png", 0.13)
        self.l1_sprite.center_x = 20
        self.l1_sprite.center_y = 20
        self.l1_list.append(self.l1_sprite)

        self.l2_sprite = arcade.Sprite("assets/life2.png", 0.13)
        self.l2_sprite.center_x = 60
        self.l2_sprite.center_y = 20
        self.l2_list.append(self.l2_sprite)

        self.l3_sprite = arcade.Sprite("assets/life3.png", 0.13)
        self.l3_sprite.center_x = 100
        self.l3_sprite.center_y = 20
        self.l3_list.append(self.l3_sprite)  
    
    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """
        for b in self.star_list:
            b.update() 
        
        self.bullet_list.update()
        for e in self.enemy_list:
            damage = arcade.check_for_collision_with_list(e, self.bullet_list)
            for d in damage:
                e.hp = e.hp - d.damage
                d.kill()
                if e.hp < 0:
                    e.kill()
                    self.score = self.score + KILL_SCORE
        
    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        for b in self.star_list:
            b.draw()
        
        arcade.draw_text("1UP", 20, SCREEN_HEIGHT - 40, open_color.red_9, 16)
        arcade.draw_text("High Score", SCREEN_WIDTH/2, SCREEN_HEIGHT - 40, open_color.red_9, 16)
        arcade.draw_text("?????????", SCREEN_WIDTH/2, SCREEN_HEIGHT - 60, open_color.white, 16)
        arcade.draw_text(str(self.score), 20, SCREEN_HEIGHT - 60, open_color.white, 16)
        
        self.player.draw()
        self.bullet_list.draw()
        self.enemy_list.draw()
        self.l1_list.draw()
        self.l2_list.draw()
        self.l3_list.draw()
    
    def on_mouse_motion(self, x, y, dx, dy):
        '''
        The player moves left and right with the mouse
        '''
        self.player.center_x = x
    
    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            #fire a bullet
            #the pass statement is a placeholder. Remove line 97 when you add your code
            x = self.player.center_x
            y = self.player.center_y + 15
            bullet = Bullet((x,y),(0,10),BULLET_DAMAGE)
            self.bullet_list.append(bullet)
            return



def main():
    window = Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()