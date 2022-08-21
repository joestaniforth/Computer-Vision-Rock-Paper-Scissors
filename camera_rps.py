import cv2 
from keras.models import load_model
import numpy as np
from datetime import datetime
from random import choice


class Computer_Vision_RPS:
    
    def __init__(self, countdown_time: int, model_file, labels_file, num_wins: int):
        self.countdown_time = countdown_time if countdown_time > 0 else 3
        self.timer_text = [f'{i}' for i in range(1, self.countdown_time+1)]
        self.timer_text = self.timer_text[::-1]
        self.timer_text.append('Go!')
        self.num_wins= num_wins
        self.user_wins = 0
        self.computer_wins = 0
        self.user_choice_dict = {
        'rock':{'rock':None, 'paper':'computer', 'scissors':'user'},
        'paper':{'rock':'user', 'paper':None, 'scissors':'computer'},
        'scissors':{'rock':'computer', 'paper':'user', 'scissors':None},
        'nothing':{'rock':None, 'paper':None, 'scissors':None}
        }
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
        seconds_passed = int()
        init_time = datetime.now()
        while seconds_passed < self.countdown_time + 1:
            time_delta = (datetime.now() - init_time).total_seconds()
            ret, frame = self.capture.read()
            textsize = cv2.getTextSize(text = self.timer_text[seconds_passed], fontFace = cv2.FONT_HERSHEY_SIMPLEX, fontScale = 6, thickness = 5)[0]
            textX = (frame.shape[1] - textsize[0]) / 2
            textY = (frame.shape[0] + textsize[1]) /  2
            cv2.putText(
                    img = frame, 
                    text = self.timer_text[seconds_passed], 
                    fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
                    fontScale = 6, 
                    color = (255,255,255),
                    thickness = 5,
                    org = (int(textX), int(textY)), 
                    lineType= cv2.LINE_AA)
            cv2.imshow('frame', frame)
            if time_delta > 1:
                seconds_passed +=1
                init_time = datetime.now()
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return
        ret, frame = self.capture.read()
        resized_frame = cv2.resize(frame, (224, 224), interpolation = cv2.INTER_AREA)
        image_np = np.array(resized_frame)
        normalized_image = (image_np.astype(np.float32) / 127.0) - 1
        self.data[0] = normalized_image
        user_choice = self.labels[np.argmax(self.model.predict(self.data))]
        return user_choice
    
    def get_computer_choice(self) -> str:
        return choice(['rock', 'paper', 'scissors'])

    def round(self):
        try:
            user_choice = self.get_prediction().lower()
        except AttributeError:
            print('You canceled the round')
            return 'quit'
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
            if self.round() == 'quit':
                return
        if self.user_wins == self.num_wins:
            print(f'You won {self.num_wins} times! You won!')
        elif self.computer_wins == self.num_wins:
            print(f'The computer won {self.num_wins} times, you lost!')

    def get_winner(self, computer_choice: str, user_choice:str):
        return self.user_choice_dict[user_choice][computer_choice]


    def reset(self):
        self.user_wins = 0
        self.computer_wins = 0


def play_game():
    game = Computer_Vision_RPS(
        countdown_time = 3, 
        model_file = 'keras_model.h5', 
        labels_file = 'labels.txt', 
        num_wins = 3)
    print('Welcome to computer vision rock paper scissors!\nPress c to play or press q to quit')
    while True:
        ret, frame = game.capture.read()
        cv2.imshow('frame', frame)
        key_pressed_startup = cv2.waitKey(1) & 0xFF
        if key_pressed_startup == ord('c'):
            game.reset()
            break
        if key_pressed_startup == ord('q'):
            return
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
