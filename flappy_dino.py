import pygame
import math
import random

# task for u sucker
# start intro, gameover intro, animation(dino[3], cactus[1])

pygame.init()

# basic thing
screen_width = 1200
screen_height = 700

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Flappy Dino")

# Image Path
images_path = 'images'

# score
text = pygame.font.SysFont("Impact", 80)
grey = (83,83,83) # color
score = 0

# background for dino and its value
bg = pygame.image.load(f"{images_path}/dino_background.png").convert()
pygame.transform.scale(bg, (screen_width - (screen_width/3), screen_height))
bg_width = bg.get_width()

# game over
scaleGo = 0.8
gameoverImg = pygame.image.load(f"{images_path}/gameover.png").convert()
gameoverImg.set_colorkey((255,255,255))
gameoverImg = pygame.transform.scale(gameoverImg, (gameoverImg.get_width()*scaleGo, gameoverImg.get_height()*scaleGo))

# dino image
del_color = (250,250,250)
dino = pygame.image.load(f"{images_path}/dino.png").convert()
dino.set_colorkey(del_color)
temp = dino

# cactus
cactus_img = pygame.image.load(f"{images_path}/cactus.png").convert()
cactus_img.set_colorkey(del_color)
cactus_gap = 200
cactus_frequency = 1250
last_cactus = pygame.time.get_ticks()

# count how many tiles needed
tiles = math.ceil(screen_width/bg.get_width()) + 1

#scoll value
scoll = 0
scoll_speed = 1.2

class Dino(pygame.sprite.Sprite):
	def __init__(self, image, x, y):
		super().__init__()
		self.image = image
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.rect.center = [x,y]
		self.velocity = 0
		self.clicked = False

	def update(self):
		# gravity
		if flying:
			self.velocity += 0.2
			if self.velocity > 1:
				self.velocity = 1
			if self.rect.bottom < screen_height - 5 or self.clicked:
				self.rect.y += int(self.velocity)
				self.clicked = False
			if self.rect.top < 0:
				self.rect.y = 0

		# jump
		if pygame.key.get_pressed()[pygame.K_SPACE] and not self.clicked and not game_over:
			self.velocity = -3
			self.clicked = True

class Cactus(pygame.sprite.Sprite):
	def __init__(self, x, y, pos, width, height, image):
		super().__init__()
		self.image = image
		if pos == -1:
			self.image = pygame.transform.flip(self.image, False, True)
		self.image = pygame.transform.scale(self.image, (width, height))
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)
		self.rect.x = x
		self.rect.y = y
		self.trigger = True

	def update(self, other, x, y):

		global game_over

		if not game_over:
			self.rect.x -= scoll_speed

			if self.rect.x < -(dino.get_width()+4):
				self.kill()

			if self.rect.x < 200 and self.trigger:
				
				global score

				score += 0.5

				self.trigger = False

			# collision
			if self.mask.overlap(other, (x - self.rect.x, y - self.rect.y)):
				game_over = True


# Dino group
adino = Dino(dino, 200,300)
dino_group = pygame.sprite.Group()
dino_group.add(adino)
width = dino.get_width() + 4

# Cactus group
cactus_group = pygame.sprite.Group()

# Trigger
flying = False
game_over = False
trigger = False

# Loop the game eternally
running = True

while running:
	
	for i in range(tiles):
		screen.blit(bg, (i * bg_width + scoll,0))

	if flying and not game_over:
		# scolling section
		scoll -= scoll_speed

		# generate cactus
		time_now = pygame.time.get_ticks()
		if time_now - last_cactus > cactus_frequency:
			x = screen_width
			y = random.randint(120, 350)

			cactus_up = Cactus(x, 0, -1, width, y, cactus_img)		# need to wait for some time => fine function clock tick
			cactus_down = Cactus(x, y + cactus_gap, 1,width, screen_height - cactus_gap - y, cactus_img)

			cactus_group.add(cactus_up)
			cactus_group.add(cactus_down)

			last_cactus = time_now

	if abs(scoll) > bg_width:
		scoll = 0

	# if pygame.sprite.groupcollide(dino_group, cactus_group, False, False):
	# 	game_over = True

	# if pygame.sprite.spritecollide(adino, cactus_group, False, pygame.sprite.collide_mask):
	# 	game_over = True
	
	# rectangle = pygame.Surface((20,20))
	# rectangle.fill((0,0,0))	
	# screen.blit(rectangle, (adino.rect.x + dino.get_width() - 20,adino.rect.y + dino.get_height() - 20))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			
			if not game_over:
				if event.key == pygame.K_SPACE and not flying:
					flying = True

				if event.key == pygame.K_SPACE and flying:	# rotate 1
					rotate = pygame.transform.rotate(dino, 5)
					adino.image = rotate

			if event.key == pygame.K_SPACE and trigger and game_over:	#restart
				cactus_group.empty()
				adino.rect.center = [200,300]
				adino.image = dino
				score = 0
				trigger = False
				game_over = False

		if event.type == pygame.KEYUP:
			if flying:
				if event.key == pygame.K_SPACE:	# rotate 2
					rotate = pygame.transform.rotate(dino, -5)
					adino.image = rotate

	dino_group.draw(screen)
	dino_group.update()
	cactus_group.draw(screen)
	cactus_group.update(adino.mask, adino.rect.x, adino.rect.y)

	if game_over:
		adino.image = pygame.transform.rotate(dino, -90)
		if adino.rect.bottom >= screen_height - 5:
			flying = False
			trigger = True
			screen.blit(gameoverImg,(screen_width/2 - gameoverImg.get_width()/2, screen_height/2 - gameoverImg.get_height()/2 - 200))


	if not game_over:
		score_render = text.render(str(int(score)), True, grey)
		screen.blit(score_render, (screen_width/2 - len(str(score)), screen_height/6))

	pygame.display.update()

pygame.quit()