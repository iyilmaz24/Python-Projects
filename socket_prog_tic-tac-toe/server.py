import socket
import time
import os
import sys


WIN_MSG = "You won the game!"
TIE_MSG = "It's a tie!"
LOSS_MSG = "You lost the game!"


def print_game():
    print_rows = ["A", "B", "C"]
    print("    1  2  3")
    for r in range(len(print_rows)):
        print(f"{print_rows[r]}   {game_board[r][0]}  {game_board[r][1]}  {game_board[r][2]}")
        
        
def make_move(move, playerMark="X", client_socket=None):
    rows = {"A": 0, "B": 1, "C": 2}
    try:
        row_ch, col = move[0].upper(), int(move[1]) - 1
        row = rows.get(row_ch)
        if row is not None and 0 <= col <= 2 and game_board[row][col] == ".":
            if client_socket and playerMark == "X":
                send_move(client_socket, move)
                
            game_board[row][col] = playerMark
            return True
        else:
            print("Invalid coordinates. Try again.")
            return False
        
    except (IndexError, ValueError):
        print("Invalid input. Try again.")
        return False
    

def get_move(client_socket):
    move = input("Enter your move (e.g. A1): ")
    if make_move(move, client_socket=client_socket):
        return True
    else:
        return get_move(client_socket)
        

def get_opponent_move(client_socket): 
    data = client_socket.recv(1024).decode('utf-8') # buffer size of 1024 bytes
    make_move(data, "O") 
    return True 


def send_move(client_socket, move):
    client_socket.sendall(move.encode('utf-8'))

def check_winner():
    lines = [
        game_board[0], game_board[1], game_board[2],  # Rows
        [game_board[0][0], game_board[1][0], game_board[2][0]],  # Columns
        [game_board[0][1], game_board[1][1], game_board[2][1]],
        [game_board[0][2], game_board[1][2], game_board[2][2]],
        [game_board[0][0], game_board[1][1], game_board[2][2]],  # Diagonals
        [game_board[0][2], game_board[1][1], game_board[2][0]]
    ]

    for line in lines:
        if line[0] == line[1] == line[2] and line[0] != ".":
            return line[0]  # returns 'X' or 'O' player mark

    if all(cell != "." for row in game_board for cell in row):
        return "Tie"

    return None


def game_over(client_socket):
    winner = check_winner()
    time.sleep(0.2) # sleep for 0.2 seconds to avoid data concatenation

    if winner:
        print_game()
        if winner == "X":
            print(WIN_MSG)
            client_socket.sendall(LOSS_MSG.encode('utf-8'))
        elif winner == "O":
            print(LOSS_MSG)
            client_socket.sendall(WIN_MSG.encode('utf-8'))
        elif winner == "Tie":
            print(TIE_MSG)
            client_socket.sendall(TIE_MSG.encode('utf-8'))
        return True
    else:
        client_socket.sendall("Continue".encode('utf-8'))
        return False
        

if __name__ == '__main__': # "python3 server.py 8000" --> uses port 8000, default is 8080
        
    serverPort = 8080
    if (len(sys.argv) > 1):
        try:
            serverPort = int(sys.argv[1])
        except:
            print("Invalid port number. Using default port 8080")
    else:
        print("No port number provided. Using default port 8080")
            
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', serverPort))
    online = True

    while online:
        game_board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]     
        playing = False
        
        server_socket.listen(1)
        print(f"Server is listening on port {serverPort}...")
        print("Waiting for opponent to connect....")

        client_socket, client_address = server_socket.accept()
        print(f"Tic-tac-toe opponent found {client_address} !")
        
        client_socket.sendall(f"Tic-tac-toe match connection established!".encode('utf-8'))
        
        playing = True
        while playing:
            print_game()
            print("Waiting for opponent to make a move....")
            
            opponent_turn = False
            while opponent_turn == False:
                opponent_turn = get_opponent_move(client_socket)
                
            if game_over(client_socket):
                playing = False
                break
            
            print_game()
            get_move(client_socket) # get the server player's move
            
            if game_over(client_socket):
                playing = False
                break
            
            
        client_socket.close()  # close the client connection
        
        restart = input("Do you want to play again? (y/n): ")
        if restart.lower() != "y":
            online = False
            
        os.system('clear') # clear the terminal screen
            
            
    server_socket.close()  # close the server socket

