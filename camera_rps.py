import cv2 
from keras.models import load_model
import numpy as np
from time import time
from random import choice


class Computer_Vision_RPS:
    
    def __init__(self, countdown_time: int, model_file, labels_file, num_wins):
        self.countdown_time = countdown_time #validate to > 0
        self.num_wins= num_wins
        self.user_wins = 0
        self.computer_wins = 0 
        self.capture = cv2.VideoCapture(0)
        self.model = load_model(model_file)
        self.data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        self.labels = self.load_labels(labels_file)
        
    def load_labels(self, labels):
        label_dict = {}
        with open(labels) as file:
            for line in file:
                key, value = line.split()
                label_dict[int(key)] = value
        return label_dict

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
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1
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
            self.user_wins +=1
        elif winner == 'computer':
            print('The computer won this round!')
            self.computer_wins +=1
        else:
            print('Nobody won this round!')

    def play(self):
        while self.user_wins < self.num_wins and self.computer_wins < self.num_wins:
            self.round()
        if self.user_wins == self.num_wins:
            print(f'You won {self.num_wins} times! You won!')
        elif self.computer_wins == self.num_wins:
            print(f'The computer won {self.num_wins} times, you lost!')

    def get_winner(self, computer_choice: str, user_choice:str):
        
        logic_dict = {'rock':{'rock':None, 'paper':'computer', 'scissors':'user'},
        'paper':{'rock':'user', 'paper':None, 'scissors':'computer'},
        'scissors':{'rock':'computer', 'paper':'user', 'scissors':None},
        'nothing':{'rock':None, 'paper':None, 'scissors':None}}

        return logic_dict[user_choice][computer_choice]


    def reset(self):
        self.user_wins = 0
        self.computer_wins = 0


def play_game():
    game = Computer_Vision_RPS(countdown_time = 3, model_file = 'keras_model.h5', labels_file = 'labels.txt', num_wins = 3)
    while True:
        game.play()
        print('Press c to play again, or q quit')
        while True:
            ret, frame = game.capture.read()
            cv2.imshow('frame', frame)
            key_pressed = cv2.waitKey(1) & 0xFF
            if key_pressed == ord('c'):
                game.reset()
                break
            if key_pressed == ord('q'):
                return

if __name__ == '__main__':
    play_game()
