import socket
from tkinter import ttk
from tkinter import *
import threading
import time
import RSA
import json

class Client:
    def __init__(self):
        self.scoreP1 = 0
        self.scoreP2 = 0
        self.player_choice = None
        self.other_player_choice = None

        self.primes = RSA.get_primes(15, 300)
        self.public_key, self.private_key = RSA.keys(self.primes[0], self.primes[1])
        self.other_public_key = None

        # Create a socket object
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define the server address and port
        self.server_address = ('localhost', 8888)

        # Connect to the server
        self.client_socket.connect(self.server_address)
        print("Connected to the server.")

        self.client_socket.send(str(self.public_key).encode())
        print("Sent public key to the server.", self.public_key)

        # Create an instance of tkinter frame
        self.win = Tk()

        # Set the geometry of the window
        self.win.geometry("750x450")

        # Set the title of the window
        self.win.title("Rock Paper Scissors")

        # Create an instance of the GUI class
        self.gui = Gui(self.win, self.isrock, self.ispaper, self.isscissor)

        # Receives the other client's public key
        other_public_key_str = self.client_socket.recv(1024).decode()
        self.other_public_key = eval(other_public_key_str)
        print(self.other_public_key)

        # Start a separate thread to receive the other player's choice
        choice_thread = threading.Thread(target=self.receive_choice)
        choice_thread.start()

    def make_choice(self, choice):
        self.player_choice = choice

    def receive_choice(self):
        while True:
            # Receive the choices from the server
            self.other_player_choice = RSA.decrypt(self.private_key, json.loads(self.client_socket.recv(1024).decode()))
            # Call handle_match_result after receiving the other player's choice
            self.handle_match_result()

    def update_ui(self):
        self.gui.update_other_player_choice(self.other_player_choice)

    def handle_match_result(self):
        # Disable the buttons
        self.gui.disable_buttons()

        # Countdown before displaying the result
        for i in range(3, 0, -1):
            self.gui.update_label(str(i), "black")
            time.sleep(1)
            self.win.update()

        if self.player_choice == self.other_player_choice:
            self.gui.update_label("Draw", "gray25")
        elif (self.player_choice == "Rock" and self.other_player_choice == "Scissors") or \
                (self.player_choice == "Paper" and self.other_player_choice == "Rock") or \
                (self.player_choice == "Scissors" and self.other_player_choice == "Paper"):
            self.gui.update_label("You win", "green")
            self.scoreP1 += 1
        else:
            self.gui.update_label("You lose", "red")
            self.scoreP2 += 1
        self.gui.update_scores(self.scoreP1, self.scoreP2)
        self.update_ui()
        # Enable the buttons
        self.gui.enable_buttons()

    def isrock(self):
        self.make_choice("Rock")
        enc_message = RSA.encrypt(self.other_public_key, self.player_choice)
        self.client_socket.send(json.dumps(enc_message).encode('utf-8'))
        self.gui.update_player_choice(self.player_choice)
        self.gui.reset_other_player_img()

    def ispaper(self):
        self.make_choice("Paper")
        enc_message = RSA.encrypt(self.other_public_key, self.player_choice)
        self.client_socket.send(json.dumps(enc_message).encode('utf-8'))
        self.gui.update_player_choice(self.player_choice)
        self.gui.reset_other_player_img()

    def isscissor(self):
        self.make_choice("Scissors")
        enc_message = RSA.encrypt(self.other_public_key, self.player_choice)
        self.client_socket.send(json.dumps(enc_message).encode('utf-8'))
        self.gui.update_player_choice(self.player_choice)
        self.gui.reset_other_player_img()

    def start(self):
        self.win.mainloop()

    def close(self):
        # Close the client socket
        self.client_socket.close()

class Gui:
    def __init__(self, win, rock_callback, paper_callback, scissor_callback):
        self.win = win
        self.rock_callback = rock_callback
        self.paper_callback = paper_callback
        self.scissor_callback = scissor_callback
        self.scoreP1 = 0
        self.scoreP2 = 0
        self.player_choice = None
        self.other_player_choice = None

        self.choose1Image = PhotoImage(file='Images/choose1.png')
        self.choose2Image = PhotoImage(file='Images/choose2.png')
        self.rockImage = PhotoImage(file='Images/rock.png')
        self.paperImage = PhotoImage(file='Images/paper.png')
        self.scissorsImage = PhotoImage(file='Images/scissors.png')
        self.rock1Image = PhotoImage(file='Images/rock1.png')
        self.paper1Image = PhotoImage(file='Images/paper1.png')
        self.scissors1Image = PhotoImage(file='Images/scissors1.png')
        self.rock2Image = PhotoImage(file='Images/rock2.png')
        self.paper2Image = PhotoImage(file='Images/paper2.png')
        self.scissors2Image = PhotoImage(file='Images/scissors2.png')

        labelframe = LabelFrame(self.win, text=" Rock Paper Scissor ", font=('Century 20 bold'), labelanchor="n", bd=5, bg="slategray2", width=600, height=450, cursor="x_cursor")
        labelframe.pack(expand=True, fill=BOTH)

        l1 = Label(labelframe, text="You", font=('Helvetica 18 bold'), bg="slategray2")
        l1.place(relx=.18, rely=.1)

        l2 = Label(labelframe, text="VS", font=('Helvetica 18 bold'), bg="slategray2")
        l2.place(relx=.45, rely=.1)

        l3 = Label(labelframe, text="Opponent", font=('Helvetica 18 bold'), bg="slategray2")
        l3.place(relx=.65, rely=.1)

        self.label = Label(labelframe, text="", font=('Coveat', 25, 'bold'), bg="slategray2")
        self.label.pack(pady=150)

        self.b1 = Button(labelframe, image=self.rockImage, command=self.rock_callback, bg="slategray3", activebackground="slategray3", cursor="hand2")
        self.b1.place(relx=.25, rely=.62)
        self.b2 = Button(labelframe, image=self.paperImage, command=self.paper_callback, bg="slategray3", activebackground="slategray3", cursor="hand2")
        self.b2.place(relx=.41, rely=.62)
        self.b3 = Button(labelframe, image=self.scissorsImage, command=self.scissor_callback, bg="slategray3", activebackground="slategray3", cursor="hand2")
        self.b3.place(relx=.57, rely=.62)

        self.score1 = Label(labelframe, text=self.scoreP1, font=('Helvetica 18 bold'), bg="slategray2")
        self.score1.place(relx=.10, rely=.1)
        self.score2 = Label(labelframe, text=self.scoreP2, font=('Helvetica 18 bold'), bg="slategray2")
        self.score2.place(relx=.88, rely=.1)

        self.img1 = Label(labelframe, image=self.choose1Image, bg="slategray2")
        self.img1.place(relx=.10, rely=.30)
        self.img2 = Label(labelframe, image=self.choose2Image, bg="slategray2")
        self.img2.place(relx=.77, rely=.30)
    
    def reset_other_player_img(self):
        self.img2.config(image=self.choose2Image)

    def update_player_choice(self, choice):
        if choice == "Rock":
            self.img1.config(image=self.rock1Image)
        elif choice == "Paper":
            self.img1.config(image=self.paper1Image)
        else:
            self.img1.config(image=self.scissors1Image)

    def update_other_player_choice(self, choice):
        if choice == "Rock":
            self.img2.config(image=self.rock2Image)
        elif choice == "Paper":
            self.img2.config(image=self.paper2Image)
        else:
            self.img2.config(image=self.scissors2Image)

    def update_label(self, text, color):
        self.label.config(text=text, fg=color)

    def update_scores(self, scoreP1, scoreP2):
        self.score1.config(text=scoreP1)
        self.score2.config(text=scoreP2)

    def disable_buttons(self):
        self.b1.config(state=DISABLED)
        self.b2.config(state=DISABLED)
        self.b3.config(state=DISABLED)

    def enable_buttons(self):
        self.b1.config(state=NORMAL)
        self.b2.config(state=NORMAL)
        self.b3.config(state=NORMAL)

# Create an instance of the Client class
client = Client()
client.start()
client.close()
