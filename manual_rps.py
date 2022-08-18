from random import choice

rps_list = ['rock', 'paper', 'scissors']

def get_computer_choice() -> str:
    return choice(rps_list)

def get_user_choice() -> str:
    while True:
        user_choice = input('Rock, Paper, Scissors? ').lower()
        if user_choice != 'rock' and user_choice != 'paper' and user_choice != 'scissors':
            print('Please choose rock, paper, or scissors')
            continue
        break
    return user_choice

def get_winner(computer_choice: str, user_choice:str):
    if computer_choice == 'rock':
        if user_choice =='rock':
            winner = None
        elif user_choice =='paper':
            winner = 'The user'
        elif user_choice == 'scissors':
            winner = 'The computer'
    elif computer_choice == 'paper':
        if user_choice =='rock':
            winner = 'The computer'
        elif user_choice =='paper':
            winner = None
        elif user_choice == 'scissors':
            winner = 'The user'
    elif computer_choice == 'scissors':
        if user_choice =='rock':
            winner = 'The user'
        elif user_choice =='paper':
            winner = 'The computer'
        elif user_choice == 'scissors':
            winner = None
    return winner

def play():
    while True:
        computer_choice = get_computer_choice()
        user_choice = get_user_choice()
        winner = get_winner(computer_choice = computer_choice, user_choice = user_choice)
        print(f'The computer picked {computer_choice}')
        if winner != None:
            break
        print('It was a tie, play again')
    print(f'{winner} wins!')

if __name__ == '__main__':
    play()