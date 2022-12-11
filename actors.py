import random
import math

class Unit:
    def __init__(self, team, uType, x, lane):
        self.team = team
        self.x = x
        self.lane = lane
        self.y = 250 + (lane * 80)
        self.uType = uType

        self.health = 0
        self.speed = 0
        self.damage = 0
        self.midColour = (0, 0, 0)
        self.spawnCountdown = 0  # Swarmer
        if uType == 0:  # Runner
            self.health = 600
            self.speed = 1.1
            self.damage = 2
            self.midColour = (140, 0, 0)
            self.spawnCountdown = 0
        elif uType == 1:  # Sprinter
            self.health = 300
            self.speed = 2
            self.damage = 1
            self.midColour = (255, 180, 0)
            self.spawnCountdown = 0
        elif uType == 2:  # Cyro-Walker
            self.health = 900
            self.speed = 0.9
            self.damage = 2
            self.midColour = (0, 0, 255)
            self.spawnCountdown = 0
        elif uType == 3:  # Swarmer
            self.health = 1000
            self.speed = 0.7
            self.damage = 3
            self.midColour = (135, 255, 0)
            self.spawnCountdown = 90
        elif uType == 4:  # Breacher
            self.health = 200
            self.speed = 3
            self.damage = 10
            self.midColour = (255, 255, 255)
            self.spawnCountdown = 0
        elif uType == 5:  # Heavy Walker
            self.health = 1500
            self.speed = 0.4
            self.damage = 4
            self.midColour = (80, 0, 0)
            self.spawnCountdown = 0
        elif uType == 6:  # Bulldozer
            self.health = 5000
            self.speed = 0.3
            self.damage = 12
            self.midColour = (40, 77, 0)
            self.spawnCountdown = 0
        elif uType == 7: # Omega
            self.health = 4500
            self.speed = 1
            self.damage = 10
            self.midColour = (0, 0, 0)
            self.spawnCountdown = 0
        else: # Spawner spammer
            self.health = 50
            self.speed = 2
            self.damage = 1
            self.midColour = (200, 200, 200)
            self.spawnCountdown = 0

        self.slowDown = 0
        self.isSlow = False

    def update(self):
        if self.team == 0:
            self.x += self.speed
        else:
            self.x -= self.speed

        self.slowDown -= 1
        
        if self.slowDown > 0 and self.isSlow == False and self.uType != 2:
            self.isSlow = True
            self.speed = self.speed / 2
        elif self.slowDown <= 0 and self.isSlow == True:
            self.isSlow = False
            self.speed = self.speed * 2

        if self.uType == 3:  # Spawner code
            self.spawnCountdown -= 1

class Tower:
    def __init__(self, team, uType, x, lane):
        self.team = team
        self.x = x
        self.lane = lane
        self.y = 250 + (lane * 80)
        self.uType = uType

        self.health = 0
        self.damage = 0
        self.fireRate = 0
        self.canFire = True
        self.colour = (0, 0, 0)
        if uType == 0:  # Turret
            self.health = 1000
            self.damage = 100
            self.fireRate = 100
            self.colour = (255, 255, 255)
        elif uType == 1:  # Collector
            self.health = 500
            self.damage = 0
            self.fireRate = 120
            self.colour = (255, 255, 0)
        elif uType == 2:  # Wall
            self.health = 4000
            self.damage = 0
            self.fireRate = 0
            self.canFire = False
            self.colour = (100, 100, 100)
        elif uType == 3:  # Staller
            self.health = 700
            self.damage = 50
            self.fireRate = 150
            self.colour = (0, 0, 255)
        elif uType == 4:  # Bomb
            self.health = 500
            self.damage = 500
            self.fireRate = 100
            self.colour = (0, 0, 0)
        elif uType == 5:  # Area Denial
            self.health = 750
            self.damage = 100
            self.fireRate = 110
            self.colour = (173, 0, 110)
        elif uType == 6:  # Cannon
            self.health = 1100
            self.damage = 200
            self.fireRate = 200
            self.colour = (173, 70, 0)
        else: # Destroyer
            self.health = 300
            self.damage = 700
            self.fireRate = 150
            self.colour = (255, 0, 0)
        
        self.nextShot = self.fireRate
        self.isFiring = False

    def update(self):
        if self.canFire:
            self.nextShot -= 1
            if self.nextShot <= 0:
                self.nextShot = self.fireRate
                self.isFiring = True

class Projectile:
    def __init__(self, team, x, y, xSpeed, ySpeed, damage, slowDown, isBomb):
        self.x = x
        self.y = y
        self.team = team
        self.xSpeed = xSpeed
        self.ySpeed = ySpeed
        self.damage = damage
        self.slowDown = slowDown
        self.isBomb = isBomb
        self.colour = (255, 255, 0)
        if self.isBomb:
            self.colour = (50, 50, 50)
        elif self.slowDown:
            self.colour = (0, 0, 200)

    def update(self):
        self.x += self.xSpeed
        self.y += self.ySpeed

class Explosive:
    def __init__(self, team, x, y, damage, size):
        self.team = team
        self.x = x
        self.y = y
        self.damage = damage
        self.size = size

        self.hasExploded = False

class AI:
    def __init__(self, difficulty, strategy):
        self.difficulty = difficulty # 0 = Easy, 1 = Normal, 2 = Hard, 3 = Cheating
        self.strategy = strategy # 0 = Random, 1 = All rush, 2 = All defend, 3 = Balanced, 4 = Agressive, 5 = Turtle
        self.lives = 20
        self.potentialIncome = 1

        # Random
        self.nextMoveRandom = random.choice(range(400, 600)) - (difficulty * 150)

        # All Rush
        self.nextUnitAR = random.choice(range(400, 500)) - (difficulty * 150)
        self.nextCollectorAR = random.choice(range(1200, 1600)) - (difficulty * 150)
        self.nextCollectorAR = 10

        # All Defend
        self.nextCollectorAD = 10
        self.nextWallAD = 50
        self.nextTowerAD = 30

        # Turtle
        self.nextSpam = random.choice(range(2500, 3500)) - (difficulty * 300)
        self.spamCount = 0
        self.spamTimer = 10
        
        self.placingTower = False
        self.placingUnit = False
        self.placeX = 0
        self.placeLane = 0
        self.placeType = 0

    def findPlacableArea(self, eTowers):
        if len(eTowers) >= 30:
            self.placingTower = False
        else:
            gotPoint = False
            while not gotPoint:
                self.placeX = 1600 - (random.choice([50, 150, 250, 350, 450, 550]) + 40)
                self.placeLane = random.choice(range(0, 5))
                gotPoint = True
                for tower in eTowers:
                    if tower.x == self.placeX and tower.lane == self.placeLane:
                        gotPoint = False

    def getPossibleUnits(self):
        spawnableUnits = [0, 1]
        if self.potentialIncome >= 15:
            spawnableUnits = [2, 3, 4, 5, 6, 7]
        elif self.potentialIncome > 12:
            spawnableUnits = [0, 1, 2, 3, 4, 5, 6]
        elif self.potentialIncome > 8:
            spawnableUnits = [0, 1, 2, 3, 4, 5, 0, 1, 2, 3, 4, 5, 6]
        elif self.potentialIncome > 6:
            spawnableUnits = [0, 1, 2, 3, 4, 5]
        elif self.potentialIncome > 3:
            spawnableUnits = [0, 1, 2, 3, 4]
        elif self.potentialIncome > 2:
            spawnableUnits = [0, 1, 2, 4]
        elif self.potentialIncome > 0:
            spawnableUnits = [0, 1, 2]

        return spawnableUnits
    
    def update(self, pTowers, pUnits, eTowers, eUnits):
        if self.strategy == 0:
            self.nextMoveRandom -= 1
            if self.nextMoveRandom <= 0:
                self.nextMoveRandom = random.choice(range(400, 600)) - min((self.difficulty * 150), 380) - (min(self.potentialIncome, 6) * 20)
                if random.choice([0, 1]) == 0: # Place unit
                    self.placingUnit = True
                    self.placeType = random.choice(self.getPossibleUnits())
                    self.placeLane = random.choice(range(0, 5))
                else: # Place tower
                    self.placingTower = True
                    self.placeType = random.choice(range(0, min(self.potentialIncome + 1, 8)))
                    self.findPlacableArea(eTowers)
        elif self.strategy == 1:
            self.nextUnitAR -= 1
            self.nextCollectorAR -= 1
            if self.nextUnitAR <= 0:
                self.nextUnitAR = random.choice(range(400, 500)) - (self.difficulty * 80) - (self.potentialIncome * 20)
                self.placingUnit = True
                self.placeType = random.choice(self.getPossibleUnits())
                spawnLanes = [0, 1, 2, 3, 4]
                for unit in pUnits:
                    spawnLanes.append(unit.lane)
                self.placeLane = random.choice(spawnLanes)
            elif self.nextCollectorAR <= 0:
                self.nextCollectorAR = random.choice(range(1200, 1600)) - (self.difficulty * 150) - (min(self.potentialIncome, 10) * 20)
                if len(eTowers) < 30:
                    self.placingTower = True
                    self.placeType = 1
                    self.placeX = 1510
                    self.placeLane = 0
                    hasSpot = False
                    while not hasSpot:
                        hasSpot = True
                        for tower in eTowers:
                            if tower.x == self.placeX and tower.lane == self.placeLane:
                                hasSpot = False
                                break
                        if not hasSpot:
                            self.placeLane += 1
                            if self.placeLane >= 5:
                                self.placeLane = 0
                                self.placeX -= 100
        else:
            self.nextCollectorAD -= 1
            self.nextWallAD -= 1
            self.nextTowerAD -= 1

            if self.nextCollectorAD <= 0:
                self.nextCollectorAD = random.choice(range(800, 1100)) - (self.difficulty * 150) - (min(self.potentialIncome, 10) * 20)
                if len(eTowers) < 30:
                    self.placingTower = True
                    self.placeType = 1
                    self.placeX = 1510
                    self.placeLane = 0
                    hasSpot = False
                    while not hasSpot:
                        hasSpot = True
                        for tower in eTowers:
                            if tower.x == self.placeX and tower.lane == self.placeLane:
                                hasSpot = False
                                break
                        if not hasSpot:
                            self.placeLane += 1
                            if self.placeLane >= 5:
                                self.placeLane = 0
                                self.placeX -= 100
                                if (self.placeX <= 1300 and self.strategy == 4) or (self.placeX <= 1400 and self.strategy != 4):
                                    self.placingTower = False
                                    break
            elif self.nextWallAD <= 0 and self.strategy != 4:
                self.nextWallAD = random.choice(range(900, 1000)) - (self.difficulty * 150) - (min(self.potentialIncome, 10) * 20)
                self.placingTower = True
                self.placeType = 2
                self.placeX = 1010
                spawnLanes = [0, 1, 2, 3, 4]
                for unit in pUnits:
                    spawnLanes.append(unit.lane)
                self.placeLane = random.choice(spawnLanes)
                for tower in eTowers:
                    if tower.x == self.placeX and tower.lane == self.placeLane:
                        self.placingTower = False
                        break
                if not self.placingTower and self.potentialIncome >= 4:
                    self.placeX = 1110
                    self.placingTower = True
                    self.placeType = 4
                    for tower in eTowers:
                        if tower.x == self.placeX and tower.lane == self.placeLane:
                            self.placingTower = False
                            break
            elif self.nextTowerAD <= 0:
                if self.strategy == 2:
                    self.nextTowerAD = random.choice(range(800, 900)) - (self.difficulty * 150)  - (min(self.potentialIncome, 10) * 20)
                elif self.strategy == 3:
                    self.nextTowerAD = random.choice(range(1000, 1100)) - (self.difficulty * 150)  - (min(self.potentialIncome, 10) * 20)
                elif self.strategy == 4:
                    self.nextTowerAD = random.choice(range(1100, 1300)) - (self.difficulty * 150)  - (min(self.potentialIncome, 10) * 20)
                elif self.strategy == 5:
                    self.nextTowerAD = random.choice(range(900, 1100)) - (self.difficulty * 150)  - (min(self.potentialIncome, 10) * 20)
                defenceTowers = 0
                for tower in eTowers:
                    if tower.uType != 1 and tower.uType != 2:
                        defenceTowers += 1
                if defenceTowers < 15:
                    self.placingTower = True
                    placableTowers = [0]
                    if self.potentialIncome > 6:
                        placableTowers = [0, 3, 5, 6, 7]
                    elif self.potentialIncome > 4:
                        placableTowers = [0, 3, 5, 6]
                    elif self.potentialIncome > 3:
                        placableTowers = [0, 3, 5]
                    elif self.potentialIncome > 1:
                        placableTowers = [0, 3]
                    self.placeType = random.choice(placableTowers)
                    gotPoint = False
                    while not gotPoint:
                        if self.strategy == 4:
                            self.placeX = 1600 - (random.choice([350, 450, 550]) + 40)
                        else:
                            self.placeX = 1600 - (random.choice([250, 350, 450]) + 40)
                        spawnLanes = [0, 1, 2, 3, 4]
                        for unit in pUnits:
                            spawnLanes.append(unit.lane)
                        self.placeLane = random.choice(spawnLanes)
                        gotPoint = True
                        for tower in eTowers:
                            if tower.x == self.placeX and tower.lane == self.placeLane:
                                gotPoint = False
                else:
                    self.placingUnit = True
                    self.placeType = random.choice(range(0, min(self.potentialIncome + 1, 7)))
                    spawnLanes = [0, 1, 2, 3, 4]
                    for unit in pUnits:
                        spawnLanes.append(unit.lane)
                    self.placeLane = random.choice(spawnLanes)

        if self.strategy == 3 or self.strategy == 4:  # Balanced Spawning
            self.nextUnitAR -= 1
            if self.nextUnitAR <= 0:
                if self.strategy == 4:
                    self.nextUnitAR = random.choice(range(500, 600)) - (self.difficulty * 150) - (min(self.potentialIncome, 10) * 20)
                else:
                    self.nextUnitAR = random.choice(range(600, 700)) - (self.difficulty * 150) - (min(self.potentialIncome, 10) * 20)
                self.placingUnit = True
                self.placeType = random.choice(self.getPossibleUnits())
                spawnLanes = [0, 1, 2, 3, 4]
                for unit in pUnits:
                    spawnLanes.append(unit.lane)
                self.placeLane = random.choice(spawnLanes)
        elif self.strategy == 5: # Turtle Spawning
            self.nextSpam -= 1
            self.spamTimer -= 1
            if self.nextSpam <= 0:
                self.nextSpam = random.choice(range(2500, 3500)) - (self.difficulty * 300)  - (min(self.potentialIncome, 10) * 20)
                self.spamCount = (min(self.potentialIncome, 10) * 2) + 6 + (self.difficulty * 2)
                self.spamTimer = 10
                self.nextSpam += self.spamTimer * self.spamCount
            if self.spamTimer <= 0 and self.spamCount > 0:
                self.spamCount -= 1
                self.spamTimer = 10
                self.placingUnit = True
                self.placeType = random.choice(self.getPossibleUnits())
                self.placeLane = random.choice([0, 1, 2, 3, 4])
