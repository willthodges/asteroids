import pgzrun, pygame, sys
import random, math

WIDTH = 1920
HEIGHT = 1080

def game_init():
    global gameover, highscore, timer, score, boost, boosting, braking, boostRegain, previous_highscore, shipX, shipY, ship, shipMagnitude, asteroids, bullets
    gameover = False
    highscore = False
    timer = 30
    score = 0
    boost = 180
    boosting = False
    braking = False
    boostRegain = True

    scores = []
    f = open(r'assignments\module 5\data\highscores.txt', 'r')
    for line in f:
        scores.append(int(line))
    if len(scores) == 0:
        scores.append(0)
    previous_highscore = max(scores)

    shipX = WIDTH/2
    shipY = HEIGHT/2
    ship = Actor('ship', center = (shipX, shipY))
    ship.angle = 0
    shipMagnitude = 4.5
    asteroids = []
    bullets = []

game_init()

class Asteroid:
    def __init__(self):
        self.radius = random.randint(30,80)
        vel = random.randint(2,7)
        spawn = random.randint(1,4)
        if spawn == 1:
            self.x = -self.radius
            self.y = random.randint(self.radius, HEIGHT-self.radius)
            self.velX = vel
            self.velY = 0
        if spawn == 2:
            self.x = WIDTH + self.radius
            self.y = random.randint(self.radius, HEIGHT-self.radius)
            self.velX = -vel
            self.velY = 0
        if spawn == 3:
            self.y = -self.radius
            self.x = random.randint(self.radius, WIDTH-self.radius)
            self.velY = vel
            self.velX = 0
        if spawn == 4:
            self.y = HEIGHT + self.radius
            self.x = random.randint(self.radius, WIDTH-self.radius)
            self.velY = -vel
            self.velX = 0
        self.shrink = 0
    def drawshape(self):
        screen.draw.filled_circle((self.x, self.y), self.radius, 'white')
        screen.draw.filled_circle((self.x, self.y), self.radius*0.75, 'grey')
    def move(self):
        self.x += self.velX
        self.y += self.velY
    def ship_collision(self):
        global gameover
        if ship.distance_to((self.x, self.y)) < self.radius + 42:
            gameover = True
            game_over()
    def bullet_collision(self):
        global score
        for bullet in bullets:
            if distance(self, bullet) <= self.radius + bullet.radius:
                bullet.clear()
                self.shrink += 6
                score += 1
    def out_of_bounds(self):
        if self.x < -self.radius:
            self.clear()
        if self.x > WIDTH + self.radius:
            self.clear()
        if self.y < -self.radius:
            self.clear()
        if self.y > HEIGHT + self.radius:
            self.clear()
    def shrinking(self):
        if self.radius >= 30 and self.shrink > 0:
            self.radius -= self.shrink
            self.shrink -= 1
        if self.radius < 30:
            self.radius -= 6
        if self.radius <= 0:
            self.clear()
    def clear(self):
        if self in asteroids:
            asteroids.remove(self)

def asteroid_append():
    asteroids.append(Asteroid())
clock.schedule_interval(asteroid_append, 0.5)


class Bullet:
    def __init__(self):
        self.x = shipX + 60*math.cos((ship.angle+90)*math.pi/180)
        self.y = shipY - 60*math.sin((ship.angle+90)*math.pi/180)
        self.radius = 6
        self.direction = ((ship.angle+90)*math.pi/180)
        self.magnitude = 15
    def drawshape(self):
        screen.draw.filled_circle((self.x, self.y), self.radius, (64,199,83))
    def move(self):
        self.x += self.magnitude*math.cos(self.direction)
        self.y -= self.magnitude*math.sin(self.direction)
    def out_of_bounds(self):
        if self.x < -self.radius:
            self.clear()
        if self.x > WIDTH + self.radius:
            self.clear()
        if self.y < -self.radius:
            self.clear()
        if self.y > HEIGHT + self.radius:
            self.clear()
    def clear(self):
        if self in bullets:
            bullets.remove(self)

def bullet_append():
    bullets.append(Bullet())
clock.schedule_interval(bullet_append, 1/3)


def draw():
    screen.clear()
    screen.fill((38,39,38))
    for bullet in bullets:
        bullet.drawshape()
    ship.draw()
    for asteroid in asteroids:
        asteroid.drawshape()
    screen.draw.text('Time: ' + str(timer), (20,20), fontsize = 48)
    screen.draw.text('Boost', (250,20), fontsize = 48)
    screen.draw.filled_rect(Rect((360,23), (180, 25)), 'white')
    screen.draw.filled_rect(Rect((360,23), (boost, 25)), (109,207,246))
    if highscore == False:
        screen.draw.text('Score: ' + str(score), midtop = (WIDTH/2, 20), fontsize = 48)
    else:
        screen.draw.text('Score: ' + str(score) + '\nNew High Score', midtop = (WIDTH/2, 20), fontsize = 48)
    if gameover:
        screen.draw.text('Game Over', center = (WIDTH/2, HEIGHT/2 - 30), fontsize = 96, owidth = 0.5, ocolor = 'black')
        screen.draw.text('Play Again? Y/N', center = (WIDTH/2, HEIGHT/2 + 30), fontsize = 48, owidth = 0.5, ocolor = 'black')
    screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        
def update():
    global gameover, highscore, boost, boosting, braking, boostRegain, shipX, shipY, shipMagnitude
    if gameover == False:
        for asteroid in asteroids:
            asteroid.ship_collision()
            asteroid.bullet_collision()
            asteroid.out_of_bounds()
            asteroid.shrinking()
            asteroid.move()
        for bullet in bullets:
            bullet.out_of_bounds()
            bullet.move()

        if shipX < 42 or shipX > WIDTH - 42 or shipY < 42 or shipY > HEIGHT - 42:
            gameover = True
            game_over()

        if keyboard.RIGHT:
            ship.angle -= 3.5
        if keyboard.LEFT:
            ship.angle += 3.5

        shipX += shipMagnitude*math.cos((ship.angle+90)*math.pi/180)
        shipY -= shipMagnitude*math.sin((ship.angle+90)*math.pi/180)
        ship.center = (shipX, shipY)

        if score > previous_highscore:
            highscore = True
        if boosting:
            if boost > 0:
                boost -= 1
                boostRegain = False
                shipMagnitude = 6.75
            if boost <= 0:
                boost = 0
                boosting = False
                clock.schedule_unique(boost_regain, 2.0)
        elif braking:
            if boost > 0:
                boost -= 1
                boostRegain = False
                shipMagnitude = 2.25
            if boost <= 0:
                boost = 0
                braking = False
                clock.schedule_unique(boost_regain, 2.0)
        else:
            shipMagnitude = 4.5
        if boostRegain:
            boost += 1/3
            if boost > 180:
                boost = 180

def boost_regain():
    global boostRegain
    boostRegain = True

def on_key_down(key):
    global boosting, braking
    if key == key.UP:
        boosting = True
        braking = False
    if key == key.DOWN:
        braking = True
        boosting = False
    if gameover == True:
        if key == key.Y:
            game_restart()
        if key == key.N:
            pygame.quit()
            sys.exit()
    
def on_key_up(key):
    global boosting, braking
    if key == key.UP:
        boosting = False
        clock.schedule_unique(boost_regain, 2.0)
    if key == key.DOWN:
        braking = False
        clock.schedule_unique(boost_regain, 2.0)

def distance(circle1, circle2):
    return ((circle2.x - circle1.x)**2 + (circle2.y - circle1.y)**2)**0.5

def countdown():
    global timer, gameover
    timer -= 1
    if timer == 0:
        gameover = True
        game_over()
clock.schedule_interval(countdown, 1.0)
 
def game_over():
    f = open(r'assignments\module 5\data\highscores.txt', 'a')
    f.write(str(score) + '\n')
    f.close()
    clock.unschedule(asteroid_append)
    clock.unschedule(bullet_append)
    clock.unschedule(countdown)

def game_restart():
    game_init()
    clock.schedule_interval(asteroid_append, 0.5)
    clock.schedule_interval(bullet_append, 0.33)
    clock.schedule_interval(countdown, 1.0)

pgzrun.go()