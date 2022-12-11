import pygame
import time
import math

from actors import *

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode([1600, 900])

# Game class
class Game:
    def __init__(self):
        self.gamePhase = 1  # 1 = Main menu, 2 = Help screen, 3 = Playing Game, 4 = Game End

        # Main Menu
        self.aiType = 0
        self.aiDifficulty = 0
        
        # Mouse Controls
        self.leftClicked = False
        self.rightClicked = False
        
        # Fonts
        self.titleFont = pygame.font.SysFont('Arial Black', 40)
        self.optionFont = pygame.font.SysFont('Arial Black', 30)
        
        self.statFont = pygame.font.SysFont('Arial Black', 20)
        self.shopHeaderFont = pygame.font.SysFont('Arial Black', 30)
        self.shopBodyFont = pygame.font.SysFont('Arial Black', 25)

        # Plaer statistics
        self.gold = 20
        self.lives = 20

        # Cooldowns
        self.spawnCooldown = 0
        self.incomeTimer = 100
        
        # Shop
        self.towers = ["Turret", "Collector", "Wall", "Staller", "Bomb", "Area Denial", "Cannon", "Destroyer"]
        self.towerCosts = [10, 5, 10, 20, 30, 40, 50, 100]
        self.units = ["Runner", "Sprinter", "Cyro-Walker", "Swarmer", "Breacher", "Heavy Walker", "Bulldozer", "Omega"]
        self.unitCosts = [5, 2, 10, 50, 15, 30, 100, 500]
        self.selectedTower = 0
        self.selectedUnit = 0

        # Units, Towers, Projectiles, and Explosives
        self.pTowers = []
        self.pUnits = []
        self.pProjectiles = []
        
        self.eTowers = []
        self.eUnits = []
        self.eProjectiles = []

        self.explosions = []

        # Placing Spots
        self.towerSpots = []
        self.towerTextCollision = [[44, 653, 260, 680], [44, 688, 286, 710], [44, 716, 234, 739], [44, 747, 269, 770], [44, 777, 254, 799], [44, 804, 335, 828], [44, 836, 278, 858], [44, 866, 313, 889]]
        self.unitTextCollision = [[1246, 657, 1458, 678], [1246, 687, 1469, 707], [1246, 718, 1540, 736], [1246, 745, 1502, 767], [1246, 777, 1504, 800], [1246, 807, 1566, 826], [1246, 835, 1525, 858], [1247, 868, 1494, 889]]

    def logic(self):
        global gameRunning
        
        if self.gamePhase == 1:  # Main Menu
            mouseInp = pygame.mouse.get_pressed()
            if mouseInp[0] and not self.leftClicked:
                self.leftClicked = True
                mouseLoc = pygame.mouse.get_pos()
                if 724 <= mouseLoc[0] <= 870 and 382 <= mouseLoc[1] <= 414:
                    self.gamePhase = 3
                    self.ai = AI(self.aiDifficulty, self.aiType)
                elif 724 <= mouseLoc[0] <= 870 and 780 <= mouseLoc[1] <= 815:
                    self.gamePhase = 2
                elif 724 <= mouseLoc[0] <= 870 and 830 <= mouseLoc[1] <= 865:
                    gameRunning = False
                else:
                    clickPoints = [[145, 263, 334, 356], [150, 260, 365, 388], [146, 290, 395, 416], [144, 284, 425, 448], [143, 286, 453, 476], [144, 234, 484, 505], [1147, 1217, 337, 361], [1147, 1252, 365, 385], [1146, 1219, 396, 419], [1146, 1273, 426, 449]]
                    for point in clickPoints:
                        if point[0] <= mouseLoc[0] <= point[1] and point[2] <= mouseLoc[1] <= point[3]:
                            if clickPoints.index(point) > 5:
                                self.aiDifficulty = clickPoints.index(point) - 6
                            else:
                                self.aiType = clickPoints.index(point)
                            break
            elif self.leftClicked and not mouseInp[0]:
                self.leftClicked = False
            
        elif self.gamePhase == 2:  # Help screen
            mouseInp = pygame.mouse.get_pressed()
            if mouseInp[0] and not self.leftClicked:
                self.leftClicked = True
                mouseLoc = pygame.mouse.get_pos()
                if 724 <= mouseLoc[0] <= 870 and 780 <= mouseLoc[1] <= 815:
                    self.gamePhase = 1
            elif self.leftClicked and not mouseInp[0]:
                self.leftClicked = False
            
        elif self.gamePhase == 3:  # Playing Game
            self.spawnCooldown -= 1
            
            # Mouse input
            mouseInp = pygame.mouse.get_pressed()
            if mouseInp[0] and not self.leftClicked:
                self.leftClicked = True
                mouseLoc = pygame.mouse.get_pos()
                for pos in self.towerSpots:
                    if pos[0] <= mouseLoc[0] <= pos[2] and pos[1] <= mouseLoc[1] <= pos[3] and self.gold >= self.towerCosts[self.selectedTower]:
                        placedTower = True
                        for tower in self.pTowers:
                            if pos[0] == tower.x and pos[1] == tower.y:
                                placedTower = False
                                break
                        if placedTower:
                            newTower = Tower(0, self.selectedTower, pos[0], 0)
                            newTower.y = pos[1]
                            self.pTowers.append(newTower)
                            self.gold -= self.towerCosts[self.selectedTower]
                            break
                for pos in self.unitTextCollision:
                    if pos[0] <= mouseLoc[0] <= pos[2] and pos[1] <= mouseLoc[1] <= pos[3]:
                        self.selectedUnit = self.unitTextCollision.index(pos)
                        break
                for pos in self.towerTextCollision:
                    if pos[0] <= mouseLoc[0] <= pos[2] and pos[1] <= mouseLoc[1] <= pos[3]:
                        self.selectedTower = self.towerTextCollision.index(pos)
                        break

                spawnLocs = [250, 330, 410, 490, 570]
                for pos in spawnLocs:
                    if 0 <= mouseLoc[0] <= 30 and pos <= mouseLoc[1] <= pos + 40 and self.gold >= self.unitCosts[self.selectedUnit]and self.spawnCooldown <= 0:
                        self.pUnits.append(Unit(0, self.selectedUnit, -40, spawnLocs.index(pos)))
                        self.gold -= self.unitCosts[self.selectedUnit]
                        self.spawnCooldown = 30
                        
            elif self.leftClicked and not mouseInp[0]:
                self.leftClicked = False

            if mouseInp[2] and not self.rightClicked:
                self.rightClicked = True
                mouseLoc = pygame.mouse.get_pos()
                for pos in self.towerSpots:
                    if pos[0] <= mouseLoc[0] <= pos[2] and pos[1] <= mouseLoc[1] <= pos[3]:
                        for tower in self.pTowers:
                            if pos[0] == tower.x and pos[1] == tower.y:
                                self.pTowers.remove(tower)
                                break
            elif self.rightClicked and not mouseInp[2]:
                self.rightClicked = False

            # Win Condition
            if self.lives <= 0 or self.ai.lives <= 0:
                self.gamePhase = 4

            # Income
            self.incomeTimer -= 1
            if self.incomeTimer <= 0:
                self.incomeTimer = 100
                self.gold += 1

            # Projectiles
            for projectile in self.pProjectiles:
                projectile.update()
                if projectile.x >= 1000 or not -100 <= projectile.y <= 1700:
                    self.pProjectiles.remove(projectile)
                else:
                    for enemy in self.eUnits:
                        if enemy.x - 40 <= projectile.x <= enemy.x and enemy.y <= projectile.y <= enemy.y + 40:
                            enemy.health -= projectile.damage
                            if projectile.slowDown:
                                enemy.slowDown = 500
                            if projectile.isBomb:
                                self.explosions.append(Explosive(0, projectile.x, projectile.y, 200, 120))
                            self.pProjectiles.remove(projectile)
                            break

            for projectile in self.eProjectiles:
                projectile.update()
                if projectile.x <= 600 or not -100 <= projectile.y <= 1700:
                    self.eProjectiles.remove(projectile)
                else:
                    for enemy in self.pUnits:
                        if enemy.x <= projectile.x <= enemy.x + 40 and enemy.y <= projectile.y <= enemy.y + 40:
                            enemy.health -= projectile.damage
                            if projectile.slowDown:
                                enemy.slowDown = 500
                            if projectile.isBomb:
                                self.explosions.append(Explosive(0, projectile.x, projectile.y, 200, 120))
                            self.eProjectiles.remove(projectile)
                            break
            
            # Towers
            for tower in self.pTowers:  # Player
                tower.update()
                if tower.isFiring:
                    tower.isFiring = False
                    if tower.uType == 1:
                        self.gold += 1
                    elif tower.uType == 0 or tower.uType ==3 or tower.uType == 6 or tower.uType == 7:
                        self.pProjectiles.append(Projectile(0, tower.x + 20, tower.y + 20, 8, 0, tower.damage, (tower.uType == 3), (tower.uType == 6)))
                    elif tower.uType == 4:
                        self.explosions.append(Explosive(0, tower.x, tower.y, tower.damage, 200))
                        self.pTowers.remove(tower)
                    elif tower.uType == 5:
                        xSpeeds = [8, 4, 0, -4, -8, -4, 0, 4]
                        ySpeeds = [0, -4, -8, -4, 0, 4, 8, 4]
                        for i in range(0, 8):
                            self.pProjectiles.append(Projectile(0, tower.x + 20, tower.y + 20, xSpeeds[i], ySpeeds[i], tower.damage, False, False))

            for tower in self.eTowers:  # Enemy
                tower.update()
                if tower.isFiring:
                    tower.isFiring = False
                    if tower.uType == 0 or tower.uType ==3 or tower.uType == 6 or tower.uType == 7:
                        self.eProjectiles.append(Projectile(1, tower.x + 20, tower.y + 20, -8, 0, tower.damage, (tower.uType == 3), (tower.uType == 6)))
                    elif tower.uType == 4:
                        self.explosions.append(Explosive(1, tower.x, tower.y, tower.damage, 200))
                        self.eTowers.remove(tower)
                    elif tower.uType == 5:
                        xSpeeds = [8, 4, 0, -4, -8, -4, 0, 4]
                        ySpeeds = [0, -4, -8, -4, 0, 4, 8, 4]
                        for i in range(0, 8):
                            self.eProjectiles.append(Projectile(0, tower.x + 20, tower.y + 20, xSpeeds[i], ySpeeds[i], tower.damage, False, False))
            
            # Units
            for unit in self.pUnits:  # Player
                unit.update()
                if unit.x >= 1640:
                    self.pUnits.remove(unit)
                    self.ai.lives -= 1
                elif unit.health <= 0:
                    self.pUnits.remove(unit)
                else:
                    for tower in self.eTowers:
                        if tower.x <= unit.x + 40 <= tower.x + 40 and unit.y == tower.y:
                            unit.x -= unit.speed
                            tower.health -= unit.damage
                            if tower.health <= 0:
                                if tower.uType == 1:
                                    self.ai.potentialIncome -= 1
                                self.eTowers.remove(tower)
                                if unit.uType == 4:
                                    unit.health = -9999
                                break
                    for enemy in self.eUnits:
                        if enemy.x - 40 <= unit.x + 40 <= enemy.x and unit.y == enemy.y:
                            unit.x -= unit.speed
                            enemy.health -= unit.damage
                            if unit.uType == 4 and enemy.health <= 0:
                                unit.health = -9999

                if unit.uType == 3 and unit.spawnCountdown <= 0:
                    unit.spawnCountdown = 90
                    self.pUnits.append(Unit(unit.team, 8, unit.x - 50, unit.lane))
            
            for unit in self.eUnits:  # Enemy
                unit.update()
                if unit.x <= 0:
                    self.eUnits.remove(unit)
                    self.lives -= 1
                elif unit.health <= 0:
                    self.eUnits.remove(unit)
                else:
                    for tower in self.pTowers:
                        if tower.x <= unit.x - 40 <= tower.x + 40 and unit.y == tower.y:
                            unit.x += unit.speed
                            tower.health -= unit.damage
                            if tower.health <= 0:
                                self.pTowers.remove(tower)
                                if unit.uType == 4:
                                    unit.health = -9999
                                break
                    for enemy in self.pUnits:
                        if enemy.x <= unit.x - 40 <= enemy.x + 40 and unit.y == enemy.y:
                            unit.x += unit.speed
                            enemy.health -= unit.damage
                            if unit.uType == 4 and enemy.health <= 0:
                                unit.health = -9999

                if unit.uType == 3 and unit.spawnCountdown <= 0:
                    unit.spawnCountdown = 90
                    self.eUnits.append(Unit(unit.team, 8, unit.x + 50, unit.lane))

            # Explosions
            for explosion in self.explosions:
                if explosion.hasExploded:
                    explosion.size -= 8
                    if explosion.size <= 0:
                        self.explosions.remove(explosion)
                else:
                    selectedArray = self.pUnits
                    if explosion.team == 0:
                        selectedArray = self.eUnits

                    for unit in selectedArray:
                        if max(abs(explosion.x - unit.x), abs(explosion.y - unit.y)) <= explosion.size:
                            unit.health -= explosion.damage

                    explosion.hasExploded = True

            # AI
            self.ai.update(self.pTowers, self.pUnits, self.eTowers, self.eUnits)
            if self.ai.placingUnit:
                self.ai.placingUnit = False
                self.eUnits.append(Unit(1, self.ai.placeType, 1700, self.ai.placeLane))

            if self.ai.placingTower:
                self.ai.placingTower = False
                self.eTowers.append(Tower(1, self.ai.placeType, self.ai.placeX, self.ai.placeLane))
                if self.ai.placeType == 1:
                    self.ai.potentialIncome += 1
            
        elif self.gamePhase == 4:  # Game End
            # Reset Units, Towers, Projectiles, Explosives, and other things
            self.pTowers = []
            self.pUnits = []
            self.pProjectiles = []
        
            self.eTowers = []
            self.eUnits = []
            self.eProjectiles = []

            self.explosions = []

            self.gold = 20
            self.lives = 20

            self.spawnCooldown = 0
            self.incomeTimer = 100
            
            self.selectedTower = 0
            self.selectedUnit = 0
            
            mouseInp = pygame.mouse.get_pressed()
            if mouseInp[0] and not self.leftClicked:
                self.leftClicked = True
                mouseLoc = pygame.mouse.get_pos()
                if 724 <= mouseLoc[0] <= 870 and 780 <= mouseLoc[1] <= 815:
                    self.gamePhase = 1
            elif self.leftClicked and not mouseInp[0]:
                self.leftClicked = False

    def draw(self):
        if self.gamePhase == 1:  # Main Menu
            screen.fill((40, 40, 40)) # Clear Screen

            # Title
            line = self.titleFont.render("Da Swarm:", False, (255, 255, 255))
            line_rect = line.get_rect(center = (800, 50))
            screen.blit(line, line_rect)

            line = self.statFont.render("The game of back-and-forth warfare.", False, (255, 255, 255))
            line_rect = line.get_rect(center = (800, 80))
            screen.blit(line, line_rect)
            
            # Headers
            screen.blit(self.shopHeaderFont.render("AI Strategy:", False, (255, 255, 255)), (150, 300))
            screen.blit(self.shopHeaderFont.render("AI Difficulty:", False, (255, 255, 255)), (1150, 300))
            
            # Buttons
            strategyNames = ["Random", "All Rush", "All Defend", "Balanced", "Agressive", "Turtle"]
            difficultyNames = ["Easy", "Normal", "Hard", "Cheating"]
            for text in strategyNames:
                colour = (100, 100, 100)
                if self.aiType == strategyNames.index(text):
                    colour = (255, 255, 255)
                screen.blit(self.shopBodyFont.render(text, False, colour), (150, 330 + (strategyNames.index(text) * 30)))
            for text in difficultyNames:
                colour = (100, 100, 100)
                if self.aiDifficulty == difficultyNames.index(text):
                    colour = (255, 255, 255)
                screen.blit(self.shopBodyFont.render(text, False, colour), (1150, 330 + (difficultyNames.index(text) * 30)))

            line = self.shopHeaderFont.render("> Play <", False, (255, 255, 255))
            line_rect = line.get_rect(center = (800, 400))
            screen.blit(line, line_rect)
            
            line = self.shopHeaderFont.render("> Help <", False, (255, 255, 255))
            line_rect = line.get_rect(center = (800, 800))
            screen.blit(line, line_rect)

            line = self.shopHeaderFont.render("> Quit <", False, (255, 255, 255))
            line_rect = line.get_rect(center = (800, 850))
            screen.blit(line, line_rect)
            
        elif self.gamePhase == 2:  # Help screen
            screen.fill((40, 40, 40)) # Clear Screen
            # Title
            line = self.titleFont.render("Da Swarm:", False, (255, 255, 255))
            line_rect = line.get_rect(center = (800, 50))
            screen.blit(line, line_rect)

            line = self.statFont.render("The game of back-and-forth warfare.", False, (255, 255, 255))
            line_rect = line.get_rect(center = (800, 80))
            screen.blit(line, line_rect)

            line = self.shopHeaderFont.render("How to play:", False, (255, 255, 255))
            line_rect = line.get_rect(center = (800, 120))
            screen.blit(line, line_rect)

            # Tutorial Text
            tutorialText = [
                "- Place towers on your side to defend your exit from enemy units -",
                "- Spawn in units to rush and defeat your enemy's defence -",
                "- Reduce your opponent's lives to 0 before they kill you -",
                "",
                "- Click on an item in either selection areas to select them -",
                "- Click on one of the transparent boxes on the green lane to place a tower -",
                "- Click on one of the green boxes at the back of the green lane to spawn a unit -",
                "",
                "- Turrets, destroyers, and cannons fire striaght forwards. Destroyers do more damage. Cannons create explosions -",
                "- Collectors generate money for you to use to build more towers or spawn more units -",
                "- Stallers slow down incoming enemies, but deal little damage -",
                "- Area Denials fire in eight directions and are best used in groups -",
                "- Walls halt incoming enemies, while bombs explode after a short amount of time -",
                "",
                "- Runners, Sprinters, and Cyro-Walkers move forwards. Sprinters are the fastest, while Cyro-Walkers are the slowest (but can't be slowed) -",
                "- Breachers move really fast and deal high damage, but kill themselves after killing a unit or tower -",
                "- Swarmers summon weak but fast units every now and then -",
                "- Heavy walkers and Bulldozers are slow, but are storng in both health and damage (Bulldozers are stronger).",
                "- Omega is the most powerful unit. It's fast, strong, and nearly unkillable -"
            ]

            for text in tutorialText:
                line = self.statFont.render(text, False, (255, 255, 255))
                line_rect = line.get_rect(center = (800, 150 + (30 * tutorialText.index(text))))
                screen.blit(line, line_rect)

            # Button
            line = self.shopHeaderFont.render("> Back <", False, (255, 255, 255))
            line_rect = line.get_rect(center = (800, 800))
            screen.blit(line, line_rect)
            
        elif self.gamePhase == 3:  # Playing Game
            screen.fill((0, 0, 0)) # Clear Screen

            lineLocations = [250, 330, 410, 490, 570]
            self.towerSpots = []
            # Gameboard generation
            for location in lineLocations:
                # Base lines
                pygame.draw.rect(screen, (0, 100, 0), pygame.Rect(0, location, 600, 40))
                pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(600, location, 400, 40))
                pygame.draw.rect(screen, (100, 0, 0), pygame.Rect(1000, location, 600, 40))

                # Unit spawn locations
                pygame.draw.rect(screen, (0, 200, 0), pygame.Rect(0, location, 30, 40))
                pygame.draw.rect(screen, (200, 0, 0), pygame.Rect(1570, location, 30, 40))

                # Tower spawn locations
                offsets = [50, 150, 250, 350, 450, 550]
                for offset in offsets:
                    self.towerSpots.append([offset, location, offset + 40, location + 40])
                    pygame.draw.rect(screen, (0, 120, 0), pygame.Rect(offset, location, 40, 40))
                    pygame.draw.rect(screen, (120, 0, 0), pygame.Rect(1600 - (offset + 40), location, 40, 40))
            
            # Projectiles
            for projectile in self.pProjectiles:
                pygame.draw.circle(screen, (255, 255, 0), (projectile.x, projectile.y), 8)

            for projectile in self.eProjectiles:
                pygame.draw.circle(screen, (255, 255, 0), (projectile.x, projectile.y), 8)
                        
            # Towers
            for tower in self.pTowers:
                pygame.draw.rect(screen, tower.colour, pygame.Rect(tower.x, tower.y, 40, 40))

            for tower in self.eTowers:
                pygame.draw.rect(screen, tower.colour, pygame.Rect(tower.x, tower.y, 40, 40))

            # Units
            for unit in self.eUnits:
                pygame.draw.polygon(screen, (255, 0, 0), ((unit.x, unit.y), (unit.x, unit.y + 40), (unit.x - 40, unit.y + 20)))
                pygame.draw.polygon(screen, unit.midColour, ((unit.x, unit.y), (unit.x, unit.y + 40), (unit.x - 20, unit.y + 20)))
            
            for unit in self.pUnits:
                pygame.draw.polygon(screen, (0, 255, 0), ((unit.x, unit.y), (unit.x, unit.y + 40), (unit.x + 40, unit.y + 20)))
                pygame.draw.polygon(screen, unit.midColour, ((unit.x, unit.y), (unit.x, unit.y + 40), (unit.x + 20, unit.y + 20)))
            
            # Explosions
            for explosion in self.explosions:
                pygame.draw.circle(screen, (255, 135, 0), (explosion.x, explosion.y), explosion.size)
            
            # Player and enemy statistics
            screen.blit(self.statFont.render("Gold: " + str(self.gold), False, (255, 255, 0)), (30, 190))
            screen.blit(self.statFont.render("Lives: " + str(self.lives), False, (255, 0, 0)), (30, 210))
            screen.blit(self.statFont.render("Lives: " + str(self.ai.lives), False, (255, 0, 0)), (1460, 210))

            screen.blit(self.shopHeaderFont.render("Tower Selection:", False, (255, 255, 255)), (50, 615))
            # Tower selection
            for i in range(0, len(self.towers)):
                colour = (150, 150, 150)
                if self.selectedTower == i:
                    colour = (255, 255, 255)
                towerText = self.shopBodyFont.render(self.towers[i] + ": " + str(self.towerCosts[i]) + " gold.", False, (colour))
                screen.blit(towerText, (50, 680 + (30 * (i - 1))))

            screen.blit(self.shopHeaderFont.render("Unit Selection:", False, (255, 255, 255)), (1250, 615))
            # Unit selection
            for i in range(0, len(self.units)):
                colour = (150, 150, 150)
                if self.selectedUnit == i:
                    colour = (255, 255, 255)
                screen.blit(self.shopBodyFont.render(self.units[i] + ": " + str(self.unitCosts[i]) + " gold.", False, (colour)), (1250, 680 + (30 * (i - 1))))
        elif self.gamePhase == 4:  # Game End
            if self.ai.lives > 0: # Game Over
                screen.fill((255, 0, 0)) # Clear Screen
                line = self.titleFont.render("=== DEFEAT ===", False, (255, 255, 255))
                line_rect = line.get_rect(center = (800, 50))
                screen.blit(line, line_rect)

                line = self.statFont.render("Your defences have fallen to the enemy's attack.", False, (255, 255, 255))
                line_rect = line.get_rect(center = (800, 80))
                screen.blit(line, line_rect)

                line = self.shopHeaderFont.render("Enemy lives left: " + str(self.ai.lives), False, (255, 255, 255))
                line_rect = line.get_rect(center = (800, 120))
                screen.blit(line, line_rect)

                difficulties = ["Easy", "Normal", "Hard", "Cheating"]
                strategies = ["Random", "All Rush", "All Defend", "Balanced", "Agressive", "Turtle"]
                AI = difficulties[self.ai.difficulty] + " " + strategies[self.ai.strategy]
                
                line = self.shopHeaderFont.render("AI: " + AI, False, (255, 255, 255))
                line_rect = line.get_rect(center = (800, 160))
                screen.blit(line, line_rect)

                line = self.shopHeaderFont.render("> Back <", False, (255, 255, 255))
                line_rect = line.get_rect(center = (800, 800))
                screen.blit(line, line_rect)
                
            else: # Victory
                screen.fill((0, 255, 0)) # Clear Screen
                line = self.titleFont.render("=== VICTORY ===", False, (255, 255, 255))
                line_rect = line.get_rect(center = (800, 50))
                screen.blit(line, line_rect)

                line = self.statFont.render("You have successfully overwhelmed the enemy.", False, (255, 255, 255))
                line_rect = line.get_rect(center = (800, 80))
                screen.blit(line, line_rect)

                line = self.shopHeaderFont.render("Your lives left: " + str(self.lives), False, (255, 255, 255))
                line_rect = line.get_rect(center = (800, 120))
                screen.blit(line, line_rect)

                difficulties = ["Easy", "Normal", "Hard", "Cheating"]
                strategies = ["Random", "All Rush", "All Defend", "Balanced", "Agressive", "Turtle"]
                AI = difficulties[self.ai.difficulty] + " " + strategies[self.ai.strategy]
                
                line = self.shopHeaderFont.render("AI: " + AI, False, (255, 255, 255))
                line_rect = line.get_rect(center = (800, 160))
                screen.blit(line, line_rect)

                line = self.shopHeaderFont.render("> Back <", False, (255, 255, 255))
                line_rect = line.get_rect(center = (800, 800))
                screen.blit(line, line_rect)
        
        pygame.display.flip()

game = Game()

gameRunning = True
while gameRunning:
    ev = pygame.event.get()
    
    game.logic()

    for event in ev:
        if event.type == pygame.QUIT:
            gameRunning = False

    game.draw()
    time.sleep(0.01)

pygame.quit()
