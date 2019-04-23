#sprites
import pygame
import random
import math
from settings import *
vector = pygame.math.Vector2

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((PW,PH))
		self.image.fill(BLACK)
		self.rect = self.image.get_rect()
		
		#movement
		self.p=vector(RESOLUTIONW/2,RESOLUTIONH-20) #position
		self.pp=self.p #previous position
		self.v=vector(0.0,0.0) #velocity
		self.a=vector(0.0,0.0) #acceleration
		self.jumps=JUMPS
		self.up=False
		self.dashing=0
		self.dashes=DASHES
		self.left=False
		self.right=False
		self.lDoubleTime=0
		self.rDoubleTime=0
		self.dashTime = 0
		
	def update(self):
		self.pp=self.p
		self.a=vector(0.0,GRAVITY)
		keys= pygame.key.get_pressed()	
		
		if keys[pygame.K_UP]:
			if (self.jumps>0 and self.dashing == 0):
				if (self.up==False):		
					self.v.y=-JUMPH
					self.jumps+=-1
					self.up=True
		if (keys[pygame.K_UP]==False):
			self.up=False
		
		if keys[pygame.K_RIGHT]:
			self.a.x+=HSPEED	
			if(self.right==False):
				self.right=True
				if (self.rDoubleTime == 0):
					self.rDoubleTime=(FPS/2)
				else:
					if(self.dashing==0 and self.dashes > 0):
						self.rDoubleTime=0		
						self.dashing = 1
						self.dashTime = (DASHT*FPS)
						self.dashes += -1
		else:
			self.right=False
		
		if keys[pygame.K_LEFT]:
			self.a.x+=-HSPEED	
			if(self.left==False):
				self.left=True
				if (self.lDoubleTime == 0):
					self.lDoubleTime=(FPS/2)
				else:
					if(self.dashing==0 and self.dashes > 0):
						self.lDoubleTime=0		
						self.dashing = -1
						self.dashTime = (DASHT*FPS)
						self.dashes += -1
		else:
			self.left=False

		if (self.dashing != 0):
			self.a = vector(0.0,0.0)
			self.v = vector(self.dashing*DASHV,0.0)
			self.dashTime+=-1
			if (self.dashTime==0):
				self.dashing=0
		if (self.rDoubleTime>0):
			self.rDoubleTime += -1
		if (self.lDoubleTime>0):
			self.lDoubleTime += -1	


		#update position
		#friction		
		self.a.x += self.v.x * HFRICTION
		#calculate position
		self.v+=self.a
		if(self.v.x>MAXVX):
			self.v.x=MAXVX
		if(self.v.x<-MAXVX):
			self.v.x=-MAXVX
		if(self.v.y>MAXVY):
			self.v.y=MAXVY


		self.p+=(self.v+(self.a/2))
		self.rect.midbottom=self.p
			
class Platform(pygame.sprite.Sprite):
	def __init__(self, x, y, w, h):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((w,h))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.pp=vector(x,y)
	def update(self):
		self.pp = (self.rect.x,self.rect.y)

class Enemy(pygame.sprite.Sprite):
	def __init__(self, t, platform, w, h, points):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((w,h))
		self.type = t
		self.rect = self.image.get_rect()
		self.points = points

		#crawler
		if(self.type=="crawler"):	
			self.platform = platform	
			self.image.fill(RED)
			self.rect.centerx = self.platform.rect.centerx
			self.rect.bottom = self.platform.rect.top
			self.direction = -1
		
		#fcrawler
		if(self.type=="fcrawler"):	
			self.platform = platform	
			self.image.fill(REDORANGE)
			self.rect.centerx = self.platform.rect.centerx
			self.rect.bottom = self.platform.rect.top
			self.direction = -1
			

		#shooter
		if(self.type=="shooter"):
			self.platform = platform
			self.image.fill(BLUE)
			self.rect.left = random.randrange(platform.rect.left, platform.rect.right-self.rect.width)
			self.rect.bottom = self.platform.rect.top
			self.shot_time = 1
		
		#fpsshooter
		if(self.type=="fpsshooter"):
			self.platform = platform
			self.image.fill(BLUEGREEN)
			self.rect.left = random.randrange(platform.rect.left, platform.rect.right-self.rect.width)
			self.rect.bottom = self.platform.rect.top
			self.shot_time = 1

		#tracker
		if(self.type=="tracker"):		
			self.image.fill(YELLOW)
			self.rect.centerx = RESOLUTIONW*1.5
			self.rect.centery = random.randrange(0,RESOLUTIONH)

		#boss
		if(self.type=="boss"):		
			self.image.fill(WHITE)
			self.rect.centerx = RESOLUTIONW*1.5
			self.rect.centery = random.randrange(0,RESOLUTIONH)
			self.shot_timea = 1
			self.shot_timeb = 10
			self.a=vector(0.0,0.0)
			self.v=vector(0.0,0.0)
			self.dashes = BOSSDASHES
			self.dashing = False
			self.dasht = 0
		

	def update(self):
		#crawler		
		if(self.type=="crawler"):
			self.rect.x += self.direction * CRAWLERS
			if(self.rect.left < self.platform.rect.left):
				self.rect.left += (self.platform.rect.left - self.rect.left)
				self.direction = 1
			if(self.rect.right > self.platform.rect.right):
				self.rect.right += (self.platform.rect.right - self.rect.right)
				self.direction = -1

		#fcrawler
		if(self.type=="fcrawler"):
			self.rect.x += self.direction * FCRAWLERS
			if(self.rect.left < self.platform.rect.left):
				self.rect.left += (self.platform.rect.left - self.rect.left)
				self.direction = 1
			if(self.rect.right > self.platform.rect.right):
				self.rect.right += (self.platform.rect.right - self.rect.right)
				self.direction = -1
	
		#shooter
		#fpsshooter
		#tracker
		
		
					

class Bullet(pygame.sprite.Sprite):
	def __init__(self, c, s, x, y, w, h, target, tracking, through):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((w,h))
		self.image.fill(c)
		self.type="bullet"
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.xtoplayer = target.rect.centerx - self.rect.centerx
		self.ytoplayer = target.rect.centery - self.rect.centery
		self.hyp = math.sqrt((self.xtoplayer ** 2) + (self.ytoplayer ** 2))
		self.xtoplayer *= (s / self.hyp)
		self.ytoplayer *= (s / self.hyp)
		self.points = 0

	def update(self):
		self.rect.x += self.xtoplayer
		self.rect.y += self.ytoplayer
		
			
			
			

		
		
		
