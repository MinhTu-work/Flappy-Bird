from itertools import cycle
import random
import sys
import pygame
from pygame.locals import *

FPS = 30
SCREENWIDTH  = 1200
SCREENHEIGHT = 1000
PIPEGAPSIZE  = 250 # gap between upper and lower part of pipe
BASEY        = SCREENHEIGHT * 0.90
check = True
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}

# list of all possible players (tuple of 3 positions of flap)
PLAYERS_LIST = (
	'assets/sprites/bird/1.png',
	'assets/sprites/bird/2.png',
	'assets/sprites/bird/3.png',
	'assets/sprites/bird/4.png',
	'assets/sprites/bird/5.png',
	'assets/sprites/bird/6.png',
	'assets/sprites/bird/7.png',
	'assets/sprites/bird/8.png',
	'assets/sprites/bird/9.png',
)
BACKGROUND_LIST = (
	'assets/sprites/background/1.jpg',
	'assets/sprites/background/2.jpg',
	'assets/sprites/background/3.jpg',
	'assets/sprites/background/4.jpg',
	'assets/sprites/background/5.jpg',
	'assets/sprites/background/6.jpg',
)
try:
    xrange
except NameError:
    xrange = range
 
def main():
    global SCREEN, FPSCLOCK
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Báo Cáo Đồ Án - Nguyễn Minh Tú')

    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )
    # game over sprite
    gameover_cv_size = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
    gameover_width = gameover_cv_size.get_width() * 1.5
    gameover_height = gameover_cv_size.get_height() * 1.5

    IMAGES['gameover'] = pygame.transform.scale(gameover_cv_size,(gameover_width,gameover_height))
    # message sprite for welcome screen
    message_cv_size = pygame.image.load('assets/sprites/message.png').convert_alpha()
    height_message = message_cv_size.get_height()
    width_message = message_cv_size.get_width()
    IMAGES['message'] = pygame.transform.scale(message_cv_size,(width_message * 1.5, height_message * 1.5))
    # message dongan for welcome screen
    dongan_message = pygame.image.load('assets/sprites/dongan_message.png')
    height_message_dongan = dongan_message.get_height()
    width_message_dongan = dongan_message.get_width()
    IMAGES['dongan_message'] = pygame.transform.scale(dongan_message,(width_message_dongan * 1.5 , height_message_dongan * 1.5))
    # convert size of base
    base_cv_size = pygame.image.load('assets/sprites/base/1.png').convert_alpha()
    IMAGES['base'] = pygame.transform.scale(base_cv_size,(1200,100)) # 192
    # convert size of pipe
    pipe_cv_size = pygame.image.load('assets/sprites/pipe/3.png').convert_alpha()
    pipe = pygame.transform.scale(pipe_cv_size, (100,500)) #320
    # bird
    IMAGES['player']= ( #152 x 129
    	pygame.image.load('assets/sprites/bird/1.png').convert_alpha(),
    	pygame.image.load('assets/sprites/bird/2.png').convert_alpha(),
    	pygame.image.load('assets/sprites/bird/3.png').convert_alpha(),
    	pygame.image.load('assets/sprites/bird/4.png').convert_alpha(),
    	pygame.image.load('assets/sprites/bird/5.png').convert_alpha(),
    	pygame.image.load('assets/sprites/bird/6.png').convert_alpha(),
    	pygame.image.load('assets/sprites/bird/7.png').convert_alpha(),
    	pygame.image.load('assets/sprites/bird/8.png').convert_alpha(),
    	pygame.image.load('assets/sprites/bird/9.png').convert_alpha(),
    	)
    #['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()
    # sounds
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    SOUNDS['die']    = pygame.mixer.Sound('assets/audio/die' + soundExt)
    SOUNDS['hit']    = pygame.mixer.Sound('assets/audio/hit' + soundExt)
    SOUNDS['point']  = pygame.mixer.Sound('assets/audio/point' + soundExt)
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
    SOUNDS['wing']   = pygame.mixer.Sound('assets/audio/wing' + soundExt)

    while True:
	# convert size of background 
        background_index = random.randint(0, len(BACKGROUND_LIST) - 1)
        background_cv_size = pygame.image.load(BACKGROUND_LIST[background_index]).convert_alpha()
        IMAGES['background'] = pygame.transform.scale(background_cv_size,(1200,1000))
        # select random pipe sprites
        IMAGES['pipe'] = (
            pygame.transform.flip(pipe, False, True),
            pipe.convert_alpha(),
        )

        # hitmask for pipes
        HITMASKS['pipe'] = (
            getHitmask(IMAGES['pipe'][0]),
            getHitmask(IMAGES['pipe'][1]),
        )

        # hitmask for player
        HITMASKS['player'] = (
        	getHitmask(IMAGES['player'][0]),
            getHitmask(IMAGES['player'][1]),
            getHitmask(IMAGES['player'][2]),
            getHitmask(IMAGES['player'][3]),
            getHitmask(IMAGES['player'][4]),
            getHitmask(IMAGES['player'][5]),
            getHitmask(IMAGES['player'][6]),
            getHitmask(IMAGES['player'][7]),
            getHitmask(IMAGES['player'][8]),

        )

        movementInfo = showWelcomeAnimation()
        crashInfo = mainGame(movementInfo)
        showGameOverScreen(crashInfo)


def showWelcomeAnimation():
    """Shows welcome screen animation of flappy bird"""
    # index of player to blit on screen
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 3, 4, 5, 6, 7, 8])
    # iterator used to change playerIndex after every 5th iteration
    loopIter = 0

    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.12)


    dongan_x = messagex - 70
    dongan_y = int(messagey - IMAGES['dongan_message'].get_height() - 10)

    basex1 = 0
    basex2 = 700
    # amount by which base can maximum shift to left
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # make first flap sound and return values for mainGame
                SOUNDS['wing'].play()
                return {
                    'playery': playery,
                    'basex1': basex1,
                    'basex2': basex2,
                    'playerIndexGen': playerIndexGen,
                    'messagex': messagex,
                    'messagey': messagey,
                    'playerIndex': playerIndex,
                }

        # adjust playery, playerIndex, basex
        if (loopIter + 1) % 5 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30

        # base move to left
        basex1 -= 5
        basex2 -= 5
        if basex1 <= - 700:
        	basex1 = 700
        if basex2 <= - 700:
        	basex2 = 700

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))
        SCREEN.blit(IMAGES['player'][playerIndex],
                    (playerx, playery))
        SCREEN.blit(IMAGES['message'], (messagex, messagey))
        SCREEN.blit(IMAGES['base'], (basex1, BASEY))
        SCREEN.blit(IMAGES['base'], (basex2, BASEY))
        SCREEN.blit(IMAGES['dongan_message'],(dongan_x,dongan_y))

        pygame.display.update()
        FPSCLOCK.tick(FPS)

def mainGame(movementInfo):
    score = playerIndex = loopIter = 0
    playerIndexGen = movementInfo['playerIndexGen']
    playerx, playery = int(SCREENWIDTH * 0.2), movementInfo['playery']
    messagex = movementInfo['messagex']
    messagey = movementInfo['messagey']	
    basex1 = movementInfo['basex1']
    basex2 = movementInfo['basex2']

    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # get 2 new pipes to add to upperPipes lowerPipes list
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    # list of lowerpipe
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    dt = FPSCLOCK.tick(FPS)/1000
    pipeVelX = -128 * dt

    # player velocity, max velocity, downward acceleration, acceleration on flap
    playerVelY    =  -9   # player's velocity along Y, default same as playerFlapped
    playerMaxVelY =  10   # max vel along Y, max descend speed
    playerMinVelY =  -8   # min vel along Y, max ascend speed
    playerAccY    =   1   # players downward acceleration
    playerRot     =  45   # player's rotation
    playerVelRot  =   3   # angular speed
    playerRotThr  = 0  # rotation threshold
    playerFlapAcc =  -9   # players speed on flapping
    playerFlapped = False # True when player flaps


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > -2 * IMAGES['player'][playerIndex].get_height():
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    SOUNDS['wing'].play()
        # check for crash here
        crashTest = checkCrash({'x': playerx, 'y': playery, 'index': playerIndex},
                               upperPipes, lowerPipes)
        if crashTest[0]:
            return {
                'y': playery,
                'groundCrash': crashTest[1],
                'basex1': basex1,
                'basex2': basex2,
                'upperPipes': upperPipes,
                'lowerPipes': lowerPipes,
                'score': score,
                'playerVelY': playerVelY,
                'playerRot': playerRot,
                'messagex': messagex,
                'messagey': messagey,
                'playerIndex': playerIndex,
            }
        # check for score
        playerMidPos = playerx + IMAGES['player'][playerIndex].get_width() / 2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + IMAGES['pipe'][0].get_width() / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 3:
                score += 1
                SOUNDS['point'].play()

        # playerIndex basex change
        if (loopIter + 1) % 3 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        #basex = -((-basex + 100) % baseShift)

        # move base to left
        basex1 -= 5
        basex2 -= 5
        if basex1 <= - 700:
        	basex1 = 700
        if basex2 <= - 700:
        	basex2 = 700

        # rotate the player
        # if playerRot > -90:
        #     playerRot -= playerVelRot

        # player's movement
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False
            playerRot = 45

        playerHeight = IMAGES['player'][playerIndex].get_height()
        playery += min(playerVelY, BASEY - playery - playerHeight)

        # move pipes to left
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 3 > len(upperPipes) > 0 and 0 < upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if len(upperPipes) > 0 and upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex1, BASEY))
        SCREEN.blit(IMAGES['base'], (basex2,BASEY))
        # print score so player overlaps the score
        showScore(score)
        # Player rotation has a threshold
        visibleRot = playerRotThr
        if playerRot <= playerRotThr:
            visibleRot = playerRot
        
        playerSurface = pygame.transform.rotate(IMAGES['player'][playerIndex], visibleRot)
        SCREEN.blit(playerSurface, (playerx, playery))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def showGameOverScreen(crashInfo):
    """crashes the player down and shows gameover image"""
    score = crashInfo['score']
    playerx = SCREENWIDTH * 0.2
    playery = crashInfo['y']
    playerIndex = crashInfo['playerIndex']
    playerHeight = IMAGES['player'][playerIndex].get_height()
    playerVelY = crashInfo['playerVelY']
    playerAccY = 2
    playerRot = crashInfo['playerRot']
    playerVelRot = 7
    messagex = crashInfo['messagex']
    messagey = crashInfo['messagey']
    basex1 = crashInfo['basex1']
    basex2 = crashInfo['basex2']

    upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

    # play hit and die sounds
    SOUNDS['hit'].play()
    if not crashInfo['groundCrash']:
        SOUNDS['die'].play()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery + playerHeight >= BASEY - 1:
                    return

        # player y shift
        if playery + playerHeight < BASEY - 1:
            playery += min(playerVelY, BASEY - playery - playerHeight)

        # player velocity change
        if playerVelY < 15:
            playerVelY += playerAccY

        # rotate only when it's a pipe crash
        if not crashInfo['groundCrash']:
            if playerRot > -90:
                playerRot -= playerVelRot

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (basex1, BASEY))
        SCREEN.blit(IMAGES['base'], (basex2, BASEY))
        showScore(score)
        playerSurface = pygame.transform.rotate(IMAGES['player'][playerIndex], playerRot)
        SCREEN.blit(playerSurface, (playerx,playery))
        SCREEN.blit(IMAGES['gameover'], (messagex, messagey + 50))
        FPSCLOCK.tick(FPS)
        pygame.display.update()
# def playerShm(playerShm):
#     """oscillates the value of playerShm['val'] between 8 and -8"""
#     if abs(playerShm['val']) == 8:
#         playerShm['dir'] *= -1

#     if playerShm['dir'] == 1:
#          playerShm['val'] += 1
#     else:
#         playerShm['val'] -= 1

def getRandomPipe():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10
    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
    ]
def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()

def checkCrash(player, upperPipes, lowerPipes):
    """returns True if player collides with base or pipes."""
    pi = player['index']
    player['w'] = IMAGES['player'][pi].get_width()
    player['h'] = IMAGES['player'][pi].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])
        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return [True, False]
    return [False, False]

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False

def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

#if __name__ == '__main__':
main()
