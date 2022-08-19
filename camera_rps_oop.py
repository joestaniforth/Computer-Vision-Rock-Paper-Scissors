import cv2 
from keras.models import load_model
import numpy as np
from time import time
from random import choice



class Computer_Vision_RPS:
    
    def __init__(self, countdown_time: int, model_file, labels, num_lives):
        self.countdown_time = countdown_time
        self.num_lives= num_lives
        self.user_lives = num_lives
        self.computer_lives = num_lives
        self.capture = cv2.VideoCapture(0)
        self.model = load_model(model_file)
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        self.labels = {}
        with open(labels) as file:
            for line in file:
                key, value = line.split()
                self.labels[int(key)] = value

    def get_prediction(self, data):
        prediction = self.model.predict(data)
        return self.labels[np.argmax(prediction)]
    
    def get_prediction(self):
        time_delta = float()
        init_time = time()
        while time_delta < self.countdown_time:
            time_delta = abs(init_time - time())
            ret, frame = self.capture.read()
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        resized_frame = cv2.resize(cv2.flip(frame, 1), (224, 224), interpolation = cv2.INTER_AREA)
        image_np = np.array(resized_frame)
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1 # Normalize the image
        self.data[0] = normalized_image
        user_choice = self.labels[np.argmax(self.model.predict(self.data))]
        return user_choice
    
    def get_computer_choice(self) -> str:
        return choice(['rock', 'paper', 'scissors'])

    def round(self):
        user_choice = self.get_prediction().lower()
        computer_choice = self.get_computer_choice()
        winner = self.get_winner(computer_choice, user_choice)
        print(f'You chose {user_choice}\nThe computer chose {computer_choice}')
        if winner == 'user':
            print('You won this round!')
            self.computer_lives -=1
        elif winner == 'computer':
            print('The computer won this round!')
            self.user_lives -=1
        else:
            print('Nobody won this round!')


    def play(self):
        while self.user_lives >0 and self.computer_lives >0:
            self.round()
        if self.user_lives == 0:
            print(f'The computer won {self.num_lives} times, you lost!')
        elif self.computer_lives == 0:
            print(f'You won {self.num_lives} times! You won!')

    def get_winner(self, computer_choice: str, user_choice:str):
        if user_choice == 'rock':
            if computer_choice =='rock':
                winner = None
            elif computer_choice =='paper':
                winner = 'computer'
            elif computer_choice == 'scissors':
                winner = 'user'
        elif user_choice == 'paper':
            if computer_choice =='rock':
                winner = 'user'
            elif computer_choice =='paper':
                winner = None
            elif computer_choice == 'scissors':
                winner = 'computer'
        elif user_choice == 'scissors':
            if computer_choice =='rock':
                winner = 'user'
            elif computer_choice =='paper':
                winner = 'user'
            elif computer_choice == 'scissors':
                winner = None
        else:
            winner = None
        return winner

game = Computer_Vision_RPS(countdown_time = 3, model_file = 'keras_model.h5', labels = 'labels.txt', num_lives = 3)
def play(exitf):
    while True:
        if exitf:
            exit()
        game.play()
        print('Press c to play again, or q quit')
        while True:
            ret, frame = game.capture.read()
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('c'):
                game.computer_lives= 3
                game.user_lives = 3
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                exitf = True
                break

if __name__ == '__main__':
    play(exitf=False)
