
# Silnik 2D Autorstwa Mikołaja Chajewskiego
class Vector2:
    def __init__(self, X, Y):
        self.x = X
        self.y = Y


class Overlay(Sprite):
    def __init__(self, vector, KeepPiority=False):
        self.keepPiority = KeepPiority
        self.RelVector = vector
        self.AbsVector = Vector2(self.RelVector.x, self.RelVector.y)

    def OnRemove(self):
        if self.keepPiority:
            if self.size == 0:
                return
            self.CarrySize = self.size
            self.size = 0
        else:
            self.IsVisible = False

    def OnAdd(self):
        if self.keepPiority and self.IsVisible:
            self.size = self.CarrySize
        else:
            game.add(self)

    def SetPosition(self, X, Y):
        self.RelVector = Vector2(X, Y)
        if X <= 100 and X >= -100 and Y <= 100 and Y >= -100:
            if not self.IsVisible or self.size == 0:
                self.OnAdd()
            self.position = Vector(X, Y)
        else:
            self.OnRemove()

    # internal
    def CamMove(self, dist, rot):
        multiply = 0.017453292519944
        num = 90.0
        num2 = dist * math.sin(multiply * (-rot + num))
        num3 = dist * math.cos(multiply * (-rot + num))
        self.SetPosition(self.RelVector.x + num2, self.RelVector.y + num3)

    def Move(self, dist, rot):
        self.CamMove(dist, rot)
        self.AbsVector = Vector2(self.RelVector.x, self.RelVector.y)


class Engine:
    def __init__(self):
        self.Sprites = []
        self.camera = Camera(self)

    def append(self, sprite):
        if self.Sprites.count(sprite) == 0:
            self.Sprites.append(sprite)

    def remove(self, sprite):
        self.Sprites.remove(sprite)
        game.remove(sprite)

    def InitSprites(self):
        self.camera.Move(0, 0)


class Camera:
    def __init__(self, Engine):
        self.engine = Engine
        self.vector = Vector2(0, 0)

    def Move(self, dist, rot):
        for obj in self.engine.Sprites:
            obj.CamMove(dist, rot)
        self.__move(dist, rot)

    def __move(self, dist, rot):
        num = 90.0
        multiply = 0.017453292519944
        num2 = dist * math.sin(multiply * (-rot + num))
        num3 = dist * math.cos(multiply * (-rot + num))
        self.vector.x += num2
        self.vector.y += num3


##################################################
size = 20


class Player(Overlay):
    def __init__(self, pointer):
        self.pointer = pointer
        Overlay.__init__(self, Vector2(0, 0))
        self.position = Vector(0, 0)
        self.size = 10
        self.speed = 0
        self.image = 0
        self.Grounded = False

    def update(self):
        if game.key('a'):
            self.flip = True
            manager.camera.Move(5, 0)
            for block in blocksManager.ActiveBlocks:
                if self.IsCollisionBlock(block) and block.RelVector.y >= -6:
                    manager.camera.Move(5, -180)
                    break
        elif game.key('d'):
            self.flip = False
            manager.camera.Move(5, -180)
            for block in blocksManager.ActiveBlocks:
                if self.IsCollisionBlock(block) and block.RelVector.y >= -6:
                    manager.camera.Move(5, 0)
                    break
        if game.key('space') and self.Grounded:
            self.Grounded = False
            self.speed = 6
        ###
        for block in blocksManager.ActiveBlocks:
            if self.IsCollisionBlock(block):
                if block.RelVector.y <= -8:
                    self.Grounded = True

                    if self.speed < 0:
                        self.speed = 0
                elif block.RelVector.y > 0:
                    if self.speed > 0:
                        self.speed = -self.speed
                        manager.camera.Move(2, 90)

        if self.speed != 0:
            manager.camera.Move(self.speed, -90)
        if self.speed > -6:
            self.speed = self.speed - 1

    def IsVectorInRange(self, vector, range):
        res = vector.y > range or vector.y < -range or vector.x > range or vector.x < -range
        return not res

    def IsCollisionBlock(self, block):
        num = False
        if block.size != 0:
            num = self.IsVectorInRange(block.RelVector, 14)
        return num


##########################################
class Pointer(Overlay):
    def __init__(self, manager):
        Overlay.__init__(self, Vector2(0, 0))
        self.manager = manager
        self.size = 5
        self.image = 56
        self.LastFoliage = None

    def update(self):
        if game.key("c"):
            self.point.X = self.LastFoliage.Block.X
            self.point.Y = self.LastFoliage.Block.Y + 19
        elif game.key("left"):
            self.Move(20, -180, )
        elif game.key("right"):
            self.Move(20, 0)
        elif game.key("up"):
            self.Move(20, 90)
        elif game.key("down"):
            self.Move(20, -90)
        elif game.key("l"):
            game.Log = True
        elif game.key("m"):
            for b in blocksManager.ActiveBlocks:
                if self.collide(b):
                    blocksManager.RemoveTile(b)
                    break
        elif game.key("n"):
            for b in blocksManager.ActiveBlocks:
                if self.collide(b):
                    return
            blocksManager.AddBlockTile(Block(self.RelVector.x/20, self.RelVector.y/20, 1), True)


#########################
class BlocksManager:
    def __init__(self, manager):
        self.manager = manager
        self.ActiveBlocks = []

    def AddBlockTile(self, block, draw):
        manager.append(block)
        self.ActiveBlocks.append(block)
        if draw:
            block.Move(0, 0)

    def RemoveTile(self, block):
        manager.remove(block)
        self.ActiveBlocks.remove(block)


#################
class Block(Overlay):
    def __init__(self, X, Y, ID):
        Overlay.__init__(self, Vector2(X*size, Y*size), True)
        self.image = 63
        self.size = size
        self.ID = ID
        IDProcessor().ProcessID(self.ID, self)

#################
class Noise:
	def __init__(self,minHeight,maxHeight):
		self.minHeight = minHeight;
		self.maxHeight = maxHeight;
		self.current = 3;
	def generateNext(self):
		num = random.randint(-1,1);
		self.current+=num;
		if self.current<self.minHeight:
			self.current = self.minHeight
		elif self.current>self.maxHeight:
			self.current = self.maxHeight
		return self.current
#################
class Generator:
    def __init__(self, engine,noise,noise2):
	self.engine = engine
	self.noise = noise;
	self.dirt_noise = noise2;
	self.CanGenerateTree = 0

    def Generate(self, blocks):
        self.GenerateTerrian(blocks)
        

    def GenerateTerrian(self, blocks):
        for i in range(-blocks, blocks):
            num = self.noise.generateNext();
            dirtSize = self.dirt_noise.generateNext();
            for j in range(num,num-dirtSize,-1):
              self.GenerateFillarOfDirt(j, i, num)
            self.GenerateStoneCollumn(i,num-dirtSize);

    def GenerateFillarOfDirt(self, BlockY, BlockX, num):
        if num  == BlockY:
            self.engine.AddBlockTile(Block(BlockX,BlockY, 1), False)
            if random.randint(0, 4) == 3 and num >= 3 and self.CanGenerateTree == 3:
                self.GenerateTree(BlockX, BlockY)
            elif self.CanGenerateTree != 3:
                self.CanGenerateTree += 1
        else:
            self.engine.AddBlockTile(Block(BlockX, BlockY, 2), False)

    def GenerateTree(self, X, Y):
        for i in range(Y + 1, Y + 4):
            self.engine.AddBlockTile(Block(X,  i, 4), False)
        self.engine.AddBlockTile(Block(X, (Y + 4), 5), False)
        self.engine.AddBlockTile(Block((X - 1),(Y + 3), 5), False)
        self.engine.AddBlockTile(Block((X + 1),  (Y + 3), 5), False)
        self.CanGenerateTree = 0

    def GenerateStoneCollumn(self, x,startI):
        for y in range(startI, -15, -1):
            self.engine.AddBlockTile(Block(x,y, 3), False)


#################
class IDProcessor:
    def Grass(self, block):
        block.color = Color(100, 200, 50)

    def Dirt(self, block):
        block.color = Color(200, 100, 50)

    def Wood(self, block):
        block.color = Color(153, 51, 0)

    def Leaves(self, block):
        block.color = Color(102, 153, 51)

    def Stone(self, block):
        block.color = Color(156, 159, 161)

    def ProcessID(self, ID, block):
        if ID == 1:
            self.Grass(block)
        elif ID == 2:
            self.Dirt(block)
        elif ID == 3:
            self.Stone(block)
        elif ID == 4:
            self.Wood(block)
        elif ID == 5:
            self.Leaves(block)


#################
manager = Engine()
blocksManager = BlocksManager(manager)
pointer = Pointer(manager)
player = Player(pointer)
grass_noise = Noise(1,5)
dirt_noise = Noise(2,5)
generator = Generator(blocksManager,grass_noise,dirt_noise)
generator.Generate(50)
manager.camera.Move(100, -90)
manager.append(pointer)
game.add(player)
manager.InitSprites()
game.start()
