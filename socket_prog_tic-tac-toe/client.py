import socket
import sys
import os


def print_game():
    print_rows = ["A", "B", "C"]
    print("    1  2  3")
    for r in range(len(print_rows)):
        print(f"{print_rows[r]}   {game_board[r][0]}  {game_board[r][1]}  {game_board[r][2]}")
        
        
def make_move(move, playerMark="O", client_socket=None):
    rows = {"A": 0, "B": 1, "C": 2}
    try:
        row_ch, col = move[0].upper(), int(move[1]) - 1
        row = rows.get(row_ch)
        if row is not None and 0 <= col <= 2 and game_board[row][col] == ".":
            if client_socket and playerMark == "O":
                send_move(client_socket, move)

            game_board[row][col] = playerMark
            return True
        else:
            return False
    except (IndexError, ValueError):
        return False
    
    
def get_move(client_socket):
    move = input("Enter your move (e.g. A1): ")
    
    if not make_move(move, client_socket=client_socket):
        print("Invalid coordinates. Try again.")
        return get_move(client_socket)
        

def get_opponent_move(client_socket): 
    print("Waiting for opponent to make a move....")
    data = client_socket.recv(1024).decode('utf-8') # buffer size of 1024 bytes
    make_move(data, "X")


def check_winner(client_socket):
    data = client_socket.recv(1024).decode('utf-8')
    
    if data != "Continue":
        print_game()
        print("\n" + data)
        return True
    else:
        return False
        
        
def send_move(client_socket, move):
    client_socket.sendall(move.encode('utf-8'))


game_board = [[".", ".", "."], [".", ".", "."], [".", ".", "."]]     
os.system('clear')  # clear the terminal

if __name__ == '__main__': # "python3 client.py 8000" --> uses port 8000, default is 8080
        
    serverPort = 8080
    if (len(sys.argv) > 1):
        try:
            serverPort = int(sys.argv[1])
        except:
            print("Invalid port number. Using default port 8080")
    else:
        print("No port number provided. Using default port 8080")
            
    server_address = ('127.0.0.1', serverPort)  # Replace '127.0.0.1' with your server's IP if different
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(server_address)

    welcome_message = client_socket.recv(1024).decode('utf-8')
    print(welcome_message)
    online = True

    while online:
        
        print_game()
        get_move(client_socket)
        if check_winner(client_socket):
            break
        
        print_game()
        get_opponent_move(client_socket)
        if check_winner(client_socket):
            break
            
    client_socket.close()  # close the server connection

