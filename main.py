import turtle
from turtle import Screen
from game_screen import Game_screen
from paddle import Paddle
from ball import Ball
from score_board import Scoreboard
from lives import Life
import time
import tkinter
timer_for_speed_increase = 0
# screen = Screen()

def start_timer():
    global timer_for_speed_increase
    timer_for_speed_increase += 1

def start_game():
    try:
        screen = Screen()
        # global screen
        screen.clear()
        turtle.tracer(0, 0)
        screen.bgcolor("black")
        screen.title("My BreakOut Game")
        screen.setup(width=800, height=600, )
        screen.cv._rootwindow.resizable(False, False)  # to disable the maximise option of the turtle screen

        g = Game_screen()
        p = Paddle((0, -280))
        b = Ball()
        s = Scoreboard()
        l = Life()

        global timer_for_speed_increase
        floor_hit_count = 5
        g.create_bricks()
        b.ball_movement()
        turtle.getcanvas().bind('<Motion>', p.move_paddle) # mouse movement is binded with paddle
        turtle.tracer(1)
        turtle.update()
        should_continue=True
        angle = 0

        while should_continue and floor_hit_count>0 and len(g.bricks) != 0:
            start_timer()
            if timer_for_speed_increase%70==0:   ### to increase the speed of the ball gradually
                b.move_speed*=.9
            screen.update()
            # print("speed",b.move_speed)
            time.sleep(b.move_speed)
            b.ball_movement()
            if b.xcor()>380 or b.xcor()<-380:      ### left and right wall hit check
                b.ball_bounce_x()
            if b.ycor()>290:                       ### top celing hit check
                b.ball_bounce_y()
            if b.ycor()<-290:                      ###  ground floor hit check
                floor_hit_count-=1                 ### to make the game stop if there is no life
                l.calculate_life(1)                ### to calculate the life and to display it in the screen
                time.sleep(1)
                b.goto(-100,-285)
                p.goto(0,-280)
                b.move_speed =0.1
                b.ball_bounce_y()
            if p.ycor() - 19 <= b.ycor() <= p.ycor() + 19 and p.xcor() - 55 <= b.xcor() <= p.xcor() + 55 and b.ycor()>-285: ###  paddle hit check
                paddle_middle = p.xcor()  # Calculate the middle point of the paddle
                if b.xcor() < paddle_middle-8:

                    b.ball_bounce_paddle("left")  # Set ball movement to the left
                elif b.xcor() > paddle_middle+8:

                    b.ball_bounce_paddle("right")  # Set ball movement to the right
                else:
                    b.ball_bounce_paddle("center") # Set ball movement straight

            angle += 30
            # The y-coordinate range is set to p.ycor() - 19 to p.ycor() + 19, which represents a buffer of 19 units above and below the paddle's y-coordinate. This accounts for the height of the paddle.
            # The x-coordinate range is set to p.xcor() - 55 to p.xcor() + 55, which represents a buffer of 55 units to the left and right of the paddle's x-coordinate. This accounts for the width of the paddle.
            # Additionally, the condition b.ycor() > -290 ensures that the ball is above the ground floor (y-coordinate of -290) before triggering the paddle hit. This prevents the ball from bouncing when it hits the ground floor.
            for i in g.bricks:
                if b.distance(i)<50:
                    # print("brick hit")
                    hit_brick_color=i.color()[0]
                    # print(hit_brick_color)
                    current_brick_index=g.bricks.index(i)
                    # print(current_brick_index)
                    del g.bricks[current_brick_index]
                    i.hideturtle()
                    b.ball_bounce_y()
                    if hit_brick_color=="yellow":
                        s.calculate_score(1)
                    if hit_brick_color=="green":
                        s.calculate_score(3)
                    if hit_brick_color=="orange":
                        s.calculate_score(5)
                    if hit_brick_color=="red":
                        s.calculate_score(10)
        s.reset_score()
        if len(g.bricks)==0:
            b.goto(0, 190)
            b.pendown()

            b.write("Congratulations!", align="center", font=("Helvetica", 24, "bold"))

            time.sleep(2)

    except (turtle.Terminator, tkinter.TclError):

            exit()

start_game()

while True:

    answer = turtle.textinput("Play Again!!","Do you want to play again? Type 'yes' or 'no'")
    if answer is None or answer.lower().startswith('n'):

        break

    else:
        start_game()
