import turtle
import random

turtleIns = turtle.Turtle()
turtle.screensize(1280, 720)

def tree(t, forward, angle, depth):  
    if depth < 1:
        if random.random() < 0.1:
            t.stamp()
        return
    
    if depth < 3:
        t.pencolor('#339933') # Green
        t.pensize(1)
    elif depth < 5:
        t.pencolor('#cccc00') # Brown
        t.pensize(2)
    else:
        t.pencolor('#996633') # Dark brown
        t.pensize(3)
    
    t.forward(forward)

    # Middle branch
    randomAngleSmall = random.randrange(-5, 5)
    t.right(randomAngleSmall)
    tree(t, forward / 2, randomAngleSmall, depth - 3)
    t.left(randomAngleSmall)

    # Right branch
    randomAngle = angle + random.randrange(-15, 15)

    t.right(randomAngle) 

    # Left branch
    tree(t, forward * random.randrange(8, 9) * 0.1, angle, depth - 1)
    
    t.left(randomAngle * 2)
    
    tree(t, forward * random.randrange(8, 9) * 0.1, angle, depth - 1)
    
    t.right(randomAngle)
    turtleIns.penup()
    t.backward(forward)
    turtleIns.pendown()

#################
turtleIns.left(90)
turtleIns.speed(0)
turtleIns._tracer(0)
turtleIns.pencolor("blue")
turtleIns.penup()
turtleIns.sety(-400)
turtleIns.pendown()
turtleIns.fillcolor('green')
#################


tree(turtleIns, 200, 30, 12)


turtle.done()
