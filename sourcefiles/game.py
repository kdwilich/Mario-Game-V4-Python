import pygame
import time
import random

from pygame.locals import*
from time import sleep

class Sprite():
	def __init__(self, model):
		self.x = 0
		self.y = 0
		self.w = 0
		self.h = 0
		self.gravity = 4.20
		self.numhits = 0
		self.vvel = 0
		self.hvel= 0
		self.model = model

	def isBrick(self):
		return False;

	def isCoinBlock(self):
		return False;


class Mario(Sprite):
	def __init__(self, model):
		Sprite.__init__(self, model)
		self.prev_x = 0
		self.prev_y = 0
		self.grounded = False
		self.colonbottom = False
		self.mimages = []
		self.mimages.append(pygame.image.load("sourcefiles/images/mario1.png"))
		self.mimages.append(pygame.image.load("sourcefiles/images/mario2.png"))
		self.mimages.append(pygame.image.load("sourcefiles/images/mario3.png"))
		self.mimages.append(pygame.image.load("sourcefiles/images/mario4.png"))
		self.mimages.append(pygame.image.load("sourcefiles/images/mario5.png"))

		#redefine sprite var
		self.x = 250
		self.y = 0
		self.w = 65
		self.h = 90

	def rememberPrevStep(self):
		self.prev_x = self.x
		self.prev_y = self.y

	def doesCollide(self, x, y, w, h):
		if self.x + self.w <= x:
			return False
		elif self.x >= x + w:
			return False
		elif self.y + self.h <= y:
			return False
		elif self.y >= y + h:
			return False
		else:
			return True

	def getOut(self, x, y, w, h):
		if self.x + self.w > x and self.prev_x + self.w <= x:
			self.x = x - self.w
		elif self.x < x + w and self.prev_x >= w + x:
			self.x = x + w
		elif self.y + self.h > y and self.prev_y + self.h <= y:
			self.y = y - self.h
			self.vvel = 0
			self.grounded = True
		elif self.y < y + h and self.prev_y <= y + h:
			self.colonbottom = True
			self.y = y + h
			self.vvel = 0

	def update(self):
		#print("in morio upodate")
		if self.x > 250:
			self.model.scrollpos = self.x - 250
		if self.x <= 0:
			self.x = 0

		self.vvel += self.gravity
		self.y += self.vvel

		if self.y >= 500:
			self.y = 500
			self.vvel = 0
			self.grounded = True
		else:
			self.grounded = False

		#test for collision
		for s in self.model.sprites:
			if s.isBrick():
				if self.doesCollide(s.x, s.y, s.w, s.h):
					self.getOut(s.x, s.y, s.w, s.h)
			if s.isCoinBlock():
				if self.doesCollide(s.x, s.y, s.w, s.h):
					self.getOut(s.x, s.y, s.w, s.h)
					if self.colonbottom:
						if s.numhits < 5:
							s.popout(self.model, s.x, s.y)
						s.numhits += 1
						self.colonbottom = False

	def draw(self, screen):
		marioframe = (self.x/20) % 5
		screen.blit(self.mimages[int(marioframe)], (self.x - self.model.scrollpos, self.y))

class Brick(Sprite):
	def __init__(self, model, x, y, w, h):
		Sprite.__init__(self, model)
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.color = (207,83,0)

	def isBrick(self):
		return True

	def update(self):
		return

	def draw(self, screen):
		pygame.draw.rect(screen, self.color, (self.x - self.model.scrollpos, self.y, self.w, self.h), 0)

class CoinBlock(Sprite):
	def __init__(self, model, x, y):
		Sprite.__init__(self, model)
		self.x = x
		self.y = y
		self.w = 75
		self.h = 75
		self.cbhit = pygame.image.load("sourcefiles/images/blockHit.png")
		self.cbunhit = pygame.image.load("sourcefiles/images/blockUnhit.png")

	def isCoinBlock(self):
		return True

	def popout(self, m, x, y):
		self.hvel = random.random() * 16 - 8
		self.vvel = -20

		coin = Coin(m, x, y, self.vvel, self.hvel)
		self.model.sprites.append(coin)

	def update(self):
		return

	def draw(self, screen):
		if self.numhits < 5:
			screen.blit(self.cbunhit, (self.x - self.model.scrollpos, self.y, self.w, self.h))
		else:
			screen.blit(self.cbhit, (self.x - self.model.scrollpos, self.y, self.w, self.h))

class Coin(Sprite):
	def __init__(self, model, x, y, vv, hv):
		Sprite.__init__(self, model)
		self.x = x + 15
		self.y = y - 25
		self.w = 60
		self.h = 60
		self.vvel = vv
		self.hvel = hv
		self.coin = pygame.image.load("sourcefiles/images/coin.png")

	def update(self):
		self.x += self.hvel

		self.vvel += self.gravity
		self.y += self.vvel

	def draw(self, screen):
		screen.blit(self.coin, (self.x - self.model.scrollpos, self.y, self.w, self.h))


class Model():
	def __init__(self):
		self.scrollpos = 0
		self.mario = Mario(self)
		self.sprites = []
		self.sprites.append(self.mario)
		self.map()

	def rememberPrevStep(self):
		self.mario.rememberPrevStep(self)

	def update(self):
		#print("in modle upodate")
		for s in self.sprites:
			s.update()

	def map(self):
		self.sprites.append(Brick(self, 345,495,369,44))
		self.sprites.append(Brick(self, 710,355,155,240))
		self.sprites.append(Brick(self, 846,397,285,74))
		self.sprites.append(Brick(self, 1308,346,120,70))
		self.sprites.append(Brick(self, 1631,463,160,89))
		self.sprites.append(Brick(self, 1891,356,130,239))
		self.sprites.append(Brick(self, 2100,295,250,78))
		self.sprites.append(CoinBlock(self, 501,295))
		self.sprites.append(CoinBlock(self, 1328,146))
		self.sprites.append(CoinBlock(self, 2300,95))

# def addBrick(x, y, w, h):
#     b = Brick(self, x, y, w, h)
#     sprites.append(b)
#
# def addCoinBlock(x, y):
# 	cb = CoinBlock(this, x, y)
# 	sprites.append(cb)


class View():
	def __init__(self, model):
		screen_size = (900,700)
		self.screen = pygame.display.set_mode(screen_size, 32)
		# self.turtle_image = pygame.image.load("turtle.png")
		self.model = model
		# self.model.rect = self.turtle_image.get_rect()

	def update(self):
		self.screen.fill([66,134,244])
		pygame.draw.rect(self.screen, [119,70,38], (0,595,900,700), 0)
		for s in self.model.sprites:
			s.draw(self.screen)
		pygame.display.flip()


class Controller():
	def __init__(self, model):
		self.model = model
		self.keep_going = True

	def update(self):
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
			#elif event.type == pygame.MOUSEBUTTONUP:
				#self.model.set_dest(pygame.mouse.get_pos())
		self.model.mario.rememberPrevStep()

		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.model.mario.x -= 12.5
		if keys[K_RIGHT]:
			self.model.mario.x += 12.5
		if keys[K_SPACE]:
			if self.model.mario.grounded == True:
				self.model.mario.grounded = False
				self.model.mario.vvel -= 40

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")
