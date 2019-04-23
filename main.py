#main
import pygame
import math
from settings import *
import random
from sprites import *



class Game:
	def __init__(self):
		#sets up game
		self.running=True
		pygame.init()
		pygame.mixer.init()
		self.clock = pygame.time.Clock()
		self.window = pygame.display.set_mode((RESOLUTIONW,RESOLUTIONH))
		pygame.display.set_caption(TITLE)
		self.font_name = pygame.font.match_font(FONT_NAME)

	def restart(self):
		#creates a new game
		self.distance=vector(0.0,0.0)
		self.score=0
		self.sprites = pygame.sprite.Group()
		self.platforms = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()
		self.plat_tick = 0
		self.enemy_tick = ETICK		
		self.enemy_que = EQUE[:]
		self.enemy_que = []
		#spawn sprite
		
		self.player = Player()
		self.sprites.add(self.player)
		
		for platform in PLATFORMS:
			p = Platform(*platform)
			self.sprites.add(p)
			self.platforms.add(p)
		
		self.run()

	def run(self):
		#actual game loop
		self.clock.tick(FPS)
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.redraw()
		
	def update(self):
		#update game loop
		self.sprites.update()

		#if hitting platform
		hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
		if (hits and (self.player.v.y>=0)):
			lowest = hits[0]
			for hit in hits:
				if hit.rect.top > lowest.rect.top:
					lowest = hit
			if self.player.p.y <= lowest.rect.centery+1:
				#self.distance.y+=(1+lowest.rect.top-self.player.p.y)
				self.player.p.y = 1+lowest.rect.top
				self.player.v.y = 0
				self.player.jumps=JUMPS
				self.player.dashes=DASHES

		#if hitting enemy
		if(pygame.sprite.spritecollide(self.player, self.enemies, False)):
			self.playing = False

		#if enemy hitting platform
		for plat in self.platforms:		
			hits = pygame.sprite.spritecollide(plat, self.enemies, False)
			for enem in hits:
				if(enem.type=="bullet"):			
					enem.kill()
			
		
					

			
		#push up
		if self.player.rect.top <= RESOLUTIONH /SCROLLRATIO:
			self.player.p.y += ((RESOLUTIONH/SCROLLRATIO)-self.player.rect.top)
			for plat in self.platforms:
				plat.rect.y += ((RESOLUTIONH/SCROLLRATIO)-self.player.rect.top)
			for enemy in self.enemies:
				enemy.rect.y += ((RESOLUTIONH/SCROLLRATIO)-self.player.rect.top)

		#push down
		if self.player.rect.bottom >= (SCROLLRATIO-1) * RESOLUTIONH /SCROLLRATIO:
			self.player.p.y += -(self.player.rect.bottom-((SCROLLRATIO-1)*RESOLUTIONH/SCROLLRATIO))
			for plat in self.platforms:
				plat.rect.y += -(self.player.rect.bottom-((SCROLLRATIO-1)*RESOLUTIONH/SCROLLRATIO))
			for enemy in self.enemies:
				enemy.rect.y += -(self.player.rect.bottom-((SCROLLRATIO-1)*RESOLUTIONH/SCROLLRATIO))

		#push left
		if self.player.rect.left <= RESOLUTIONW /(SCROLLRATIO+1):
			self.player.p.x += ((RESOLUTIONW/(SCROLLRATIO+1))-self.player.rect.left)
			for plat in self.platforms:
				plat.rect.x += ((RESOLUTIONW/(SCROLLRATIO+1))-self.player.rect.left)
			for enemy in self.enemies:
				enemy.rect.x += ((RESOLUTIONW/(SCROLLRATIO+1))-self.player.rect.left)
				

		#push right
		if self.player.rect.right >= (SCROLLRATIO-2) * RESOLUTIONW /(SCROLLRATIO-1):
			self.player.p.x += -(self.player.rect.right-((SCROLLRATIO-2)*RESOLUTIONW/(SCROLLRATIO-1)))
			for plat in self.platforms:
				plat.rect.x += -(self.player.rect.right-((SCROLLRATIO-2)*RESOLUTIONW/(SCROLLRATIO-1)))
			for enemy in self.enemies:
				enemy.rect.x += -(self.player.rect.right-((SCROLLRATIO-2)*RESOLUTIONW/(SCROLLRATIO-1)))

		self.distance+=self.player.v

		#spawn platforms
		if(self.distance.x >= self.plat_tick):
			self.plat_tick += random.randrange(0, PLATSPACEW)
			width = random.randrange(50,300)
			self.plat_tick += width
			
			rightestx = -1000
			for plat in self.platforms:
				if (plat.rect.x > rightestx):
					rightest = plat
					rightestx = plat.rect.x
			
			height = random.randrange(rightest.rect.y-PLATSPACEUP,rightest.rect.y+PLATSPACEDOWN)

			p = Platform(RESOLUTIONW*2,height, width, 20)

			self.platforms.add(p)
			self.sprites.add(p)


		#no enemies?
		if(self.enemy_que == []):
			roll = random.randrange(1,6)
			difficulty = 1000 - (self.score*10)
			if(self.score == 1):
				self.enemy_que.append([0,difficulty,"boss", 300, 20, 10])
			if(difficulty < 100):
				difficulty = 100
			if(roll==1):
				self.enemy_que.append([0,difficulty,"crawler",30,20,1])
			if(roll==2):
				self.enemy_que.append([0,difficulty,"shooter",20,30,1])
			if(roll==3):
				self.enemy_que.append([0,difficulty,"fcrawler",30,20,1])
			if(roll==4):
				self.enemy_que.append([0,difficulty,"fpsshooter",20,30,1])
			if(roll==5):
				self.enemy_que.append([0,difficulty,"tracker",20,20,1])
		
		#add enemies
		if(self.distance.x >= self.enemy_tick):
			if(self.enemy_que != []):
				if(self.score >= self.enemy_que[0][0]):
					rightestx = -1000
					for plat in self.platforms:
						if (plat.rect.x > rightestx):
							rightest = plat
							rightestx = plat.rect.x
					e = Enemy(self.enemy_que[0][2], rightest, self.enemy_que[0][3], self.enemy_que[0][4], self.enemy_que[0][5])
					self.enemies.add(e)
					self.sprites.add(e)
					self.enemy_tick = self.enemy_que[0][1] + self.distance.x
					del self.enemy_que[0]		

		for enem in self.enemies:

			#create shooter bullets			
			if(enem.type=="shooter"):
				if(enem.rect.left < RESOLUTIONW):
					enem.shot_time += -1
					if(enem.shot_time==0):
						b = Bullet(BLUE, SHOOTBSPEED, enem.rect.centerx, enem.rect.centery, 8, 8, self.player, False, False)
						self.enemies.add(b)
						self.sprites.add(b)
						enem.shot_time = random.randrange(SHOTMIN,SHOTMAX)

			#create fpsshooter bullets
			if(enem.type=="fpsshooter"):
				if(enem.rect.left < RESOLUTIONW):
					enem.shot_time += -1
					if(enem.shot_time==0):
						b = Bullet(BLUEGREEN, FPSSHOOTBSPEED, enem.rect.centerx, enem.rect.centery, 8, 8, self.player, False, False)
						self.enemies.add(b)
						self.sprites.add(b)
						enem.shot_time = random.randrange(FPSSHOTMIN,FPSSHOTMAX)

			#boss
			if(enem.type=="boss"):
				enem.a.x = RESOLUTIONW - enem.rect.centerx
				enem.a.y = (self.player.rect.centery-200) - enem.rect.centery
				
				#set max accelearation
				if(enem.a.x>BOSSAX):
					enem.a.x=BOSSAX
				if(enem.a.x<-BOSSAX):
					enem.a.x=-BOSSAX
				if(enem.a.y>BOSSAY):
					enem.a.y=BOSSAY
				if(enem.a.y<-BOSSAY):
					enem.a.y=-BOSSAY

				enem.v += enem.a
				
				#set max velocity
				if(enem.v.x>BOSSSMAX):
					enem.v.x=BOSSSMAX
				if(enem.v.x<-BOSSSMAX):
					enem.v.x=-BOSSSMAX
				if(enem.v.y>BOSSSMAX):
					enem.v.y=BOSSSMAX
				if(enem.v.y<-BOSSSMAX):
					enem.v.y=-BOSSSMAX
				
				if(enem.dashes>0):
					if(enem.rect.left < 0):
						enem.dashing = True
						enem.dashes += -1
						enem.dasht = BOSSDASHT * FPS
				
				if(enem.dashing):
					enem.a = vector(0.0,0.0)
					enem.v = vector(BOSSDASHS,0.0)
					enem.dasht += -1
					if(enem.dasht == 0):
						enem.dashing = False
									
				enem.rect.center += (enem.v+(enem.a/2))
				


				#boss shooting 
				enem.shot_timea += -1
				enem.shot_timeb += -1
				if(enem.shot_timea==0):
					enem.shot_timea = random.randrange(BOSSSHOTMIN,BOSSSHOTMAX)
					b = Bullet(WHITE, BOSSSHOOTBSPEED, enem.rect.left, enem.rect.centery, 8, 8, self.player, False, False)
					self.enemies.add(b)
					self.sprites.add(b)
				if(enem.shot_timeb==0):
					enem.shot_timeb = random.randrange(BOSSSHOTMIN,BOSSSHOTMAX)
					b = Bullet(WHITE, BOSSSHOOTBSPEED, enem.rect.right, enem.rect.centery, 8, 8, self.player, False, False)
					self.enemies.add(b)
					self.sprites.add(b)
					
				
			#trackers move
			if(enem.type=="tracker"):
				toplayer = vector(self.player.rect.centerx-enem.rect.centerx, self.player.rect.centery-enem.rect.centery)
				hyp = math.sqrt((toplayer.x**2)+(toplayer.y**2))
				toplayer *= (TRACKERS/hyp)
				enem.rect.center += toplayer
				

			#kill all to the left of screen
			if(enem.rect.right < 0):
				self.score += enem.points
				
				enem.kill()


		alive = False	
		
		#end game if player falls
		for plat in self.platforms:
			if self.player.rect.y < plat.rect.y + 400:
				alive = True
			if plat.rect.right <= -RESOLUTIONH:
				plat.kill()

		if alive==False:
			self.playing = False

		
		
	def events(self):
		#events game loop
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				if self.playing:
					self.playing = False				
				self.running = False

	def redraw(self):
		#redraw game loop
		self.window.fill(LIGHT_BLUE)
		self.sprites.draw(self.window)
		self.draw_text(str(int(round(self.score))), 24, BLACK, 100, 100)
		pygame.display.flip()

	def disp_menu(self):
		#show start menu
		self.window.fill(WHITE)
		self.draw_text(TITLE, 52, BLACK, RESOLUTIONW/2, 3*RESOLUTIONH/8)
		self.draw_text("Arrows to move, Up to Jump or Double Jump", 20, BLACK, RESOLUTIONW/2, 5*RESOLUTIONH/8)
		self.draw_text("The only way to defeat enemies is to run", 20, BLACK, RESOLUTIONW/2, 3*RESOLUTIONH/4)
		self.draw_text("Press any key to start", 20, BLACK, RESOLUTIONW/2, 7*RESOLUTIONH/8)
		pygame.display.flip()
		self.input_wait()

	def disp_go(self):
		#show gameover window
		pass
	
	def draw_text(self, text, size, color, x, y):
		font = pygame.font.Font(self.font_name, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		text_rect.center = (x,y)
		self.window.blit(text_surface, text_rect)

	def input_wait(self):
		wait = True
		while wait:
			self.clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					wait = False
					self.running = False
				if event.type == pygame.KEYUP:
					wait = False

	


game = Game()
game.disp_menu()
while game.running:
	game.restart()
	game.disp_go()


pygame.quit()

