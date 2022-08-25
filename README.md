# Computer-Vision-Rock-Paper-Scissors

## Milestone 2: Create the model

The model was made on Teachable Machine, with 4 classes, Rock, Paper, Scissors, and Nothing. A variety of light levels, poses,
and hands were used to try and make the model more robust.

## Milestone 4: Create a Rock Paper Scissors Game 

Creating a rock paper scissors game with manual (non-Computer Vision) was relatively simple, the choice function from random was
used to pick rock, paper, or scissors for the computer, and an input was used for the user. A series of if statements was then used
to determine the winner.

## Milestone 5: Use the camera to play rock paper scissors

A fucntion was written to get the user prediction from the camera input, returning the relevant label and being given a picture. Initially, the 
time module was used, however, datetime was the final choice as the total_seconds() method on timedelta objects provided a more intuitive way to time
3 seconds without sleeping the camera.

The decision to wrap the entire game in a class was made early, before the task suggested to do so. The ability to only have to change a single line of code:
```python
game = Computer_Vision_RPS(countdown_time = 3, model_file = 'keras_model.h5', labels_file = 'labels.txt', num_wins = 3)
```
and see changes made debugging much easier.

The major variance from the manual rps was the use of a dictionary of dictionaries to return a winner of the game, rather than a series of if/elif statements.
Dictionaries have constant lookup times, so this solution is likely more performant, and is incidentally easier to read. It also allowed this dictionary to be initialised once in the initialiser function, which prevented having to generate anything on any call of the method. 
