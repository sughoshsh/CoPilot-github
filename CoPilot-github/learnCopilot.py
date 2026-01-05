import random

def get_user_choice():
    """Get the user's choice of rock, paper, or scissors."""
    choices = ['rock', 'paper', 'scissors']
    user_choice = input("Enter your choice (rock, paper, scissors): ").lower()
    while user_choice not in choices:
        user_choice = input("Invalid choice. Please enter rock, paper, or scissors: ").lower()
    return user_choice

def get_computer_choice():
    """Randomly select the computer's choice of rock, paper, or scissors."""
    choices = ['rock', 'paper', 'scissors']
    return random.choice(choices)

def play_again():
        """Ask the user if they want to play again."""
        while True:
            again = input("Do you want to play again? (yes/no): ").lower()
            if again in ['yes', 'no']:
                return again == 'yes'
            print("Invalid input. Please enter 'yes' or 'no'.")

def determine_winner(user_choice, computer_choice):
    """Determine the winner of the game."""
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (user_choice == 'rock' and computer_choice == 'scissors') or \
         (user_choice == 'paper' and computer_choice == 'rock') or \
         (user_choice == 'scissors' and computer_choice == 'paper'):
        return "You win!"
    else:
        return "You lose!"

def play_game():
    """Play a game of rock, paper, scissors."""
    user_choice = get_user_choice()
    computer_choice = get_computer_choice()
    print(f"You chose: {user_choice}")
    print(f"Computer chose: {computer_choice}")
    result = determine_winner(user_choice, computer_choice)
    print(result)

if __name__ == "__main__":
    while True:
        play_game()
        if not play_again():
            break