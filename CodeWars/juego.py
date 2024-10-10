def rps(player1, player2):
    if player1 == player2:
        return "Draw!"
    
    win_conditions = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock"
    }
    
    if win_conditions[player1] == player2:
        return "Player 1 won!"
    else:
        return "Player 2 won!"
