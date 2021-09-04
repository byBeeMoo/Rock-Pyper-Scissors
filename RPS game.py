import socket

IP = "{PRIVATE_IP}"
PORT = 1234 # Port modifiable. Ports above 1024 dont require privileges.
HOSTNAME = socket.gethostname()
STARTMESSAGE ="[+] Starting RPS game...\n"
WELCOMEMESSAGE = "\n=== WELCOME TO ROCK, PAPER, SCISSORS w/ PYTHON ===\n"
GAMEMESSAGE = "\n\t<:/TTTTTTTTTTTTTTTTTTT\\:>\n\t<:| Choose an option: |:>\n\t<:|       ROCK        |:>\n\t<:|      PAPER        |:>\n\t<:|     SCISSORS      |:>\n\t<:\\___________________/:>\n"
WINMESSAGE = "WINNER, GL!   \nScore is: "
LOSEMESSAGE = "Unfortunately... you lost :( \nScore is: "
TIEMESSAGE = "You tied with your opponent.  \nScore is: "

quitOption = ''
activeConections = 0
hostWins, clientWins = 0, 0
serverRPS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverRPS.bind((IP, PORT))
while True:
    if hostWins != 0 or clientWins != 0:
        while quitOption != "y" and quitOption != "yes" and quitOption != "n" and quitOption != "no":
            quitOption = input("Would you like to keep playing? [y/N]").lower()
            
        if quitOption == "n" or quitOption == "no":
                print("[-] Thanks for playing!  \n[-] Exiting...")
                serverRPS.close()
                break
            
    # Listen for connections and accepts them
    if activeConections == 0:
        print("[+] Listening for incoming connections...")
        serverRPS.listen()
        (conn, addr) = serverRPS.accept()
        try:
            activeConections +=1
            with conn:
                print(f"{addr} has connected!")
                print("[+] Starting RPS game ...")
                conn.send("[+] Starting RPS game...".encode("utf-8"))

                # Starting RPS
                while True:
                    if (hostWins == 0 and clientWins == 0):
                        print("=== WELCOME TO ROCK, PAPER, SCISSORS w/ PYTHON ===")
                        conn.send(WELCOMEMESSAGE.encode("utf-8"))
                    print(GAMEMESSAGE)
                    conn.send(f"{GAMEMESSAGE}   \n{HOSTNAME}@{addr[0]}~$\t".encode("utf-8"))
                        
                    # PORT and CLIENT make the DECISION
                    hostData = input(f"{HOSTNAME}@PORT~$\t").lower()
                    clientData = conn.recv(2048).decode("utf-8")[:-1]
                    # print(hostData) # DEBUG #
                    # print(clientData) # DEBUG #
                    print('\n')
                    
                    # compare data sent to determine winner
                    if hostData == "exit" or clientData == "exit":    
                        if hostData == "exit":
                            conn.send(f"Your opponent has quit the game, final score was {hostWins}:{clientWins}".encode("utf-8"))
                                
                        else:
                            print(f"Your opponent has quit the game, final score was {hostWins}:{clientWins}")
                        conn.close()
                        activeConections -= 1
                        break
                        
                    elif (hostData == "rock" and clientData == "scissors") or (hostData == "scissors" and clientData == "paper") or (hostData == "paper" and clientData == "rock"):    
                        hostWins +=1
                        conn.send(f"\nYour opponnent choosed: {hostData}\n".encode("utf8"))
                        print(f"{WINMESSAGE} {hostWins}:{clientWins}")
                        conn.send(f"\n{LOSEMESSAGE} {hostWins}:{clientWins}\nBetter luck next time! :)".encode("utf-8"))
                        
                    elif (hostData == "scissors" and clientData == "rock") or (hostData == "paper" and clientData == "scissors") or (hostData == "rock" and clientData == "paper"):
                        clientWins +=1
                        print(f"{LOSEMESSAGE} {hostWins}:{clientWins}\nBetter luck next time!")
                        conn.send(f"\n{WINMESSAGE} {hostWins}:{clientWins}".encode("utf-8"))
                        
                    elif hostData != "scissors" or hostData != "rock" or hostData != "paper":
                        print("Wrong option!\n(rock, paper, scissors, exit)")
                        
                    elif  clientData != "scissors" or clientData != "rock" or clientData != "paper":
                        conn.send("Wrong option!\n(rock, paper, scissors, exit)".encode("utf-8"))
                    
                    elif hostData == clientData:
                        print(f"{TIEMESSAGE} {hostWins}:{clientWins}")
                    else:
                        activeConections -= 1
                        break          
        except:
            print("\nConnection has been closed :(    \nBye...")
            activeConections -= 1
            if conn.__class__ == socket:
                conn.close()
        
    else:
        print(f"Someone has already connected, wait until game has ended...")
        break
