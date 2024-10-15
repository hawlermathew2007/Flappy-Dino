import pygame

pygame.init()

lists = pygame.font.get_fonts()
textes = []
print(len(lists))
for i in range(len(lists)):
	text = pygame.font.SysFont(lists[i], 16)
	textes.append(text)

# basic thing
screen_width = 1200
screen_height = 700

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Flappy Dino")

del_color = (250,250,250)
cactus_img = pygame.image.load("cactus.png").convert()
cactus_img.set_colorkey(del_color)

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

		if self.mask.overlap(other, (x - self.rect.x, y - self.rect.y)):
			print("jk")

		screen.blit(self.mask.to_surface(), (400, 200))

class Bullet(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("dino.png").convert()
		self.image.set_colorkey((250,250,250))
		self.rect = self.image.get_rect()
		self.mask = pygame.mask.from_surface(self.image)

	def update(self):
		pos = pygame.mouse.get_pos()
		screen.blit(self.image, pos)

cactus = Cactus(100,200, 1, 240,400, cactus_img)
cactus_group = pygame.sprite.Group()
cactus_group.add(cactus)

bullet = Bullet()
bullet_group = pygame.sprite.Group()
bullet_group.add(bullet)

pygame.mouse.set_visible(False)

x = 10
y = 20

running = True
done = False
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	pos = pygame.mouse.get_pos()

	if not done:
		for text in range(len(textes)):
			thing = "HI, " + lists[text]
			text_render = textes[text].render(thing, True, (255,255,255))
			screen.blit(text_render, (x, y))
			y += 20
			if y > 1000:
				x += len(thing)*14
				y = 20
		done = True

	# bullet_group.draw(screen)
	# bullet_group.update()
	# cactus_group.draw(screen)
	# cactus_group.update(bullet.mask, pos[0], pos[1])
	pygame.display.update()

pygame.quit()