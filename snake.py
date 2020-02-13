import pygame
from random import randint
from tkinter import *

class Transform():
	def __init__(self, x, y, w = None, h = None):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.color = (0,130,255)
	def Draw(self, differenColor = None):
		if(differenColor == None):
			differenColor = self.color
		pygame.draw.rect(root, differenColor, (self.x, self.y, self.w, self.h))

class Snake():
	def __init__(self, gridX, gridY):
		self.gridX = gridX
		self.gridY = gridY
		startingPos = (randint(0,gridX-1),randint(0,gridY-2))
		self.body = [startingPos,(startingPos[0],startingPos[1]+1)]
		self.xSpeed = 0
		self.ySpeed = -1
		self.color = (255,255,0)
		self.food = tuple()
		self.NewFood()

	def Move(self):
		nextHeadPos = list((self.body[0][0] + self.xSpeed, self.body[0][1] + self.ySpeed))
		if(nextHeadPos[0] == -1):
			nextHeadPos[0] = self.gridX-1
		elif(nextHeadPos[0] == self.gridX):
			nextHeadPos[0] = 0
		elif(nextHeadPos[1] == -1):
			nextHeadPos[1] = self.gridY-1
		elif(nextHeadPos[1] == self.gridY):
			nextHeadPos[1] = 0
			
		if(nextHeadPos == list(self.food)):
			self.body.insert(0, self.food)
			self.NewFood()
		else:
			for index in range(len(self.body)-1, 0, -1):
				self.body[index] = self.body[index-1]
			self.body[0] = tuple(nextHeadPos)

	def NewFood(self):
		foodPos = (randint(0,self.gridX-1),randint(0,self.gridY-1))
		if(foodPos not in self.body):
			self.food = foodPos
		else:
			self.NewFood()


settings = [30,15,15,10]
def AssignTheValues():
	values = [int(lengthEntry.get()), int(gridXEntry.get()), int(gridYEntry.get()), tickScale.get()]
	settings.clear()
	for value in values:
		settings.append(value)
	tkWindow.destroy()

tkWindow = Tk()
tkWindow.title("Settings")
lengthLabel = Label(tkWindow, text="Length").grid(column=0,row=0, sticky=W)
lengthEntry = Entry(tkWindow)
lengthEntry.grid(column=1,row=0)
gridXLabel = Label(tkWindow, text="Number Of Columns").grid(column=0,row=1, sticky=W)
gridXEntry = Entry(tkWindow)
gridXEntry.grid(column=1,row=1)
gridYLabel = Label(tkWindow, text="Number Of Row").grid(column=0,row=2, sticky=W)
gridYEntry = Entry(tkWindow)
gridYEntry.grid(column=1,row=2)
tickScale = Scale(tkWindow,to=20, from_=5, border=0)
tickScale.set(10)
tickScale.grid(column=2,row=0, rowspan=4)
enterButton = Button(tkWindow, text="Enter Settings",command=lambda: AssignTheValues())
enterButton.grid(column=0,row=4,columnspan=2)
tkWindow.mainloop()


pygame.init()
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

grid = []
markedPlatforms = []
offset = 0

length, numberX, numberY, tick = settings

for y in range(numberY):
	platformLine = []
	for x in range(numberX):
		cPlatform = Transform(offset + x*length + x*offset, offset + y*length + y*offset, length, length)
		platformLine.append(cPlatform)
	grid.append(platformLine)

root = pygame.display.set_mode((round(offset + numberX*length + numberX*offset), round(offset + numberY*length + numberY*offset)))

snake = Snake(numberX, numberY)
#snake2 = Snake(numberX, numberY)

main = True
while (main):
	clock.tick(tick)
	for event in pygame.event.get():
		if (event.type == pygame.QUIT):
			main = False

	if(pygame.mouse.get_pressed()[0]):
		mousePos = pygame.mouse.get_pos()
		for platformLine in grid:
			for platform in platformLine:
				if(platform.x < mousePos[0] and platform.x + length > mousePos[0]):
					if(platform.y < mousePos[1] and platform.y + length > mousePos[1]):
						platform.color = (255,255,255)
						markedPlatforms.append(platform)

	keys = pygame.key.get_pressed()
	if((keys[pygame.K_RIGHT] and snake.xSpeed != -1) or (keys[pygame.K_d] and snake.xSpeed != -1)):
		snake.xSpeed = 1
		snake.ySpeed = 0
	if((keys[pygame.K_LEFT] and snake.xSpeed != 1) or (keys[pygame.K_a] and snake.xSpeed != 1)):
		snake.xSpeed = -1
		snake.ySpeed = 0
	if((keys[pygame.K_UP] and snake.ySpeed != 1) or (keys[pygame.K_w] and snake.ySpeed != 1)):
		snake.ySpeed = -1
		snake.xSpeed = 0
	if((keys[pygame.K_DOWN] and snake.ySpeed != -1) or (keys[pygame.K_s] and snake.ySpeed != -1)):
		snake.ySpeed = 1
		snake.xSpeed = 0
	#snake2.xSpeed = snake.xSpeed
	#snake2.ySpeed = snake.ySpeed

	root.fill((0,0,0))
	for platformLine in grid:
		for platform in platformLine:
			platform.Draw()
	for bodyPart in snake.body:
		grid[bodyPart[1]][bodyPart[0]].Draw((255,255,0))
	grid[snake.food[1]][snake.food[0]].Draw((255,0,0))
	snake.Move()

	'''
	for bodyPart in snake2.body:
		grid[bodyPart[1]][bodyPart[0]].Draw((255,255,0))
	grid[snake2.food[1]][snake2.food[0]].Draw((255,0,0))
	snake2.Move()
	'''

	for part in (snake.body):
		if(part is not snake.body[0]):
			if(part == snake.body[0]):
				snake = Snake(numberX, numberY)
	
	pygame.display.update()

pygame.quit()
