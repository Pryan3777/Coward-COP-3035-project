#settings
TITLE = "Coward!"
RESOLUTIONW = 720
RESOLUTIONH = 480
FPS = 60
GRAVITY = .5
MAXVX=10
MAXVY=10
FONT_NAME = 'arial'

#Player Sprite Properties
PW = 30 
PH = 40
JUMPS = 2
JUMPH = 12.0
HSPEED = 3.0
HFRICTION = -0.3
DASHES = 0
DASHT = 0.2
DASHV = -200.0
SCROLLRATIO = 3

#platforms
PLATFORMS = [(0, RESOLUTIONH-20, RESOLUTIONW*2, 20)]
PLATSPACEUP = 200
PLATSPACEDOWN = 200
PLATSPACEW = 250

#add a couple common constant colors
BLACK = (0,0,0)
WHITE = (255,255,255)
LIGHT_BLUE = (71,224,255)
LIGHT_GREEN = (71,255,154)
GREEN = (17,198,99)
RED = (255,0,0)
BLUE = (0,0,255)
REDORANGE = (255,95,0)
BLUEGREEN = (0,127,255)
BLUERED = (127,0,255)
YELLOW = (255,255,0)

#enemies
ETICK = 1000
#[score to spawn, tick on death, type, w, h, points on death]
EQUE = [
[0, 1032, "tracker", 20, 20, 1],
[0, 1010, "fpsshooter", 20, 30, 1],
[0, 1050, "fcrawler", 30, 20, 1],
[0, 1040, "shooter", 20, 30, 1],
[0, 1030, "crawler", 30, 20, 1],
[0, 1028, "crawler", 30, 20, 1],
[0, 1036, "shooter", 20, 30, 1],
[0, 1050, "shooter", 20, 30, 1],
[0, 1002, "shooter", 20, 30, 1],
[0, 1028, "crawler", 30, 20, 1],
[0, 1008, "crawler", 30, 20, 1],
[0, 1018, "shooter", 20, 30, 1],
[0, 1008, "shooter", 20, 30, 1],
[0, 1032, "shooter", 20, 30, 1],
[0, 1036, "crawler", 30, 20, 1],
[0, 1030, "crawler", 30, 20, 1],
[0, 1020, "shooter", 20, 30, 1],
[0, 1010, "shooter", 20, 30, 1],
[0, 1006, "shooter", 20, 30, 1],
[0, 1040, "shooter", 20, 30, 1]] 

#crawlers
CRAWLERS = 1

#shooter
SHOTMIN = 20
SHOTMAX = 50
SHOOTBSPEED = 5

#fpsshooter
FPSSHOTMIN = 100
FPSSHOTMAX = 200
FPSSHOOTBSPEED = 10

#fcrawlers
FCRAWLERS = 4

#tracker
TRACKERS = 3

#boss
BOSSSHOTMIN = 50
BOSSSHOTMAX = 100
BOSSSHOOTBSPEED = 5
BOSSSMAX = 3.0
BOSSDASHES = 2
BOSSAX = 2.0
BOSSAY = 5.0
BOSSDASHT = .5
BOSSDASHS = 30
