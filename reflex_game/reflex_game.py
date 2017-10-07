# import modules
import RPi.GPIO as GPIO
import time
import random

def right_wins():
    global right_score
    right_score += 1
    GPIO.output(13, True)
    time.sleep(1)
    GPIO.output(13, False)   

def left_wins():
    global left_score
    left_score += 1
    GPIO.output(15, True)
    time.sleep(1)
    GPIO.output(15, False)      

# tell the system what numbering to use
GPIO.setmode(GPIO.BOARD)

# setup the notification led
GPIO.setup(5, GPIO.OUT)

# setup button 1
GPIO.setup(7, GPIO.IN)

# setup button 2
GPIO.setup(11, GPIO.IN)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)


# flick three times
GPIO.output(5, True)
time.sleep(0.5)
GPIO.output(5, False)
time.sleep(0.5)
GPIO.output(5, True)
time.sleep(0.5)
GPIO.output(5, False)
time.sleep(0.5)
GPIO.output(5, True)
time.sleep(0.5)
GPIO.output(5, False)

# start scores
left_score = 0
right_score = 0

try:
    while True:
        # initialise game - and random start time
        game_in_progress = False
        game_time = time.time() + random.randrange(5, 10)

        # link buttons to actions
        GPIO.add_event_detect(7, GPIO.FALLING, bouncetime=1000)
        GPIO.add_event_detect(11, GPIO.FALLING, bouncetime=1000)

        # setup inner loop
        winner = None

        # during the game, if no winner 
        while not winner:
            # if we haven't started the game and we are past the start..
            if not game_in_progress and time.time() > game_time:
                # flash the light
                GPIO.output(5, True)
                time.sleep(0.2)
                GPIO.output(5, False)

                #start
                game_in_progress = True

            # check the button presses
            player_1_pressed = GPIO.event_detected(7)
            player_2_pressed = GPIO.event_detected(11)

            # decide on a winner
            if player_1_pressed and player_2_pressed:
                winner = "Tie: Both players at once.."
            elif player_1_pressed:
                if game_in_progress:
                    winner = "Right player won!"
                    right_wins()
                else:
                    winner = "Left player won! Right went too early."
                    left_wins()
                    
            elif player_2_pressed:
                if game_in_progress:
                    winner = "Left player won!"
                    left_wins()
                else:
                    winner = "Right player won! Left went too early."
                    right_wins()
                    
            if winner:
                # remove actions
                GPIO.remove_event_detect(7)
                GPIO.remove_event_detect(11)

        print("{} [{} vs {}]".format(winner, left_score, right_score))
        time.sleep(2)
        
except KeyboardInterrupt:
    print("Thanks for playing.. final score: {} vs {}".format(left_score, right_score))
    
finally:
    # clean up
    GPIO.cleanup()
