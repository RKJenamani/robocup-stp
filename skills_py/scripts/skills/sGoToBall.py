import skill_node
import math
import sys

sys.path.insert(0, '../../../navigation_py/scripts/navigation')
sys.path.insert(0, '../../../navigation_py/scripts/navigation/src')
sys.path.insert(0, '../../../plays_py/scripts/utils')

from config import *
from wrapperpy import *
from obstacle import Obstacle
from geometry import *
from math import exp

POINTPREDICTIONFACTOR = 2

def execute(param,state,bot_id, pub):
    # print("gar mra bhosdike")
    obs = Vector_Obstacle()
    for i in range(0,len(state.homeDetected)):
        if state.homeDetected[i] and i != bot_id:
            o = Obstacle()     
            o.x=state.homePos[i].x
            o.y=state.homePos[i].y
            o.radius=3.3*BOT_RADIUS
            obs.push_back(o)

    for j in range(0,len(state.awayDetected)):
        if state.awayDetected[j]:
            o = Obstacle()
            o.x=state.awayPos[j].x
            o.y=state.awayPos[j].y
            o.radius=3.3*BOT_RADIUS
            obs.push_back(o)


    ballfinalpos = Vector2D()
    ballfinalpos.x = int(state.ballPos.x + (state.ballVel.x)/POINTPREDICTIONFACTOR)
    ballfinalpos.y = int(state.ballPos.y + (state.ballVel.y)/POINTPREDICTIONFACTOR)

    point = Vector2D()
    nextWP = Vector2D()
    nextNWP = Vector2D()

    pathplanner = MergeSCurve()

    botPos = Vector2D(int(state.homePos[bot_id].x),int(state.homePos[bot_id].y))

    pathplanner.plan(botPos,ballfinalpos,nextWP,nextNWP,obs,len(obs),bot_id,not state.isteamyellow)


    ballPos = Vector2D(int(state.ballPos.x), int(state.ballPos.y))
    dist = ballPos.dist(botPos)
    maxDisToTurn = dist -  DRIBBLER_BALL_THRESH
    angleToTurn = ballPos.normalizeAngle((ballPos.angle(botPos))-(state.homePos[bot_id].theta))

    minReachTime = maxDisToTurn / MAX_BOT_SPEED
    maxReachTime = maxDisToTurn / MIN_BOT_SPEED

    minTurnTime = angleToTurn / MAX_BOT_OMEGA
    maxTurnTime = angleToTurn / MIN_BOT_OMEGA

    speed = 0.0
    omega = angleToTurn * MAX_BOT_OMEGA / (2 * math.pi)

    if omega < MIN_BOT_OMEGA and omega > -MIN_BOT_OMEGA:
        if omega < 0:
            omega = -MIN_BOT_OMEGA
        else:
            omega = MIN_BOT_OMEGA

   
    speed= 2*maxDisToTurn*MAX_BOT_SPEED/(HALF_FIELD_MAXX)
    if (speed)< 2*MIN_BOT_SPEED:
        speed=2*MIN_BOT_SPEED
    if  (speed > MAX_BOT_SPEED):
        speed=MAX_BOT_SPEED    

    vec = Vector2D()
    motionAngle = nextWP.angle(botPos)
    theta  = motionAngle - state.homePos[bot_id].theta
   
    if dist < DRIBBLER_BALL_THRESH:
        if dist < 1*BOT_BALL_THRESH:
            skill_node.send_command(pub, state.isteamyellow, bot_id, 0, 0, omega, 0, True)
        else:
            skill_node.send_command(pub, state.isteamyellow, bot_id, speed * math.sin(-theta), speed * math.cos(-theta), omega, 0, True)

    else:
        skill_node.send_command(pub, state.isteamyellow, bot_id, speed * math.sin(-theta), speed * math.cos(-theta), omega, 0, False)

  

