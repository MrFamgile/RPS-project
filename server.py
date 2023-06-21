import socket
import threading
# from RSA import RSA

class Server:
    def __init__(self):
        self.clients = []
        self.player_choices = {}
        self.player_locks = [threading.Lock(), threading.Lock()]
        self.choices_event = threading.Event()
        self.server_socket = None

    def handle_client(self, client_socket, player_number):
        try:
            while True: 
                # Receive the player's choice from the client
                choice = client_socket.recv(1024).decode()
                print("Player", player_number, "choice:", choice)

                # Store the player's choice
                with self.player_locks[player_number - 1]:
                    self.player_choices[player_number] = choice

                # Check if both players have made their choices
                if len(self.player_choices) == 2:
                    # Set the event to signal that both players have made their choices
                    self.choices_event.set()

                    # Wait for both players to make their choices
                    self.choices_event.wait()

                    # Send each player's choice to the respective clients
                    client1_choice = self.player_choices[1]
                    client2_choice = self.player_choices[2]

                    # Send the other player's choice to the respective clients
                    self.clients[0].send(client2_choice.encode())
                    self.clients[1].send(client1_choice.encode())

                    # Reset the choices and event for the next round
                    self.player_choices.clear()
                    self.choices_event.clear()

        finally:
            # Close the client socket
            client_socket.close()

    def start_server(self):
        # Create a socket object
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Define the server address and port
        server_address = ('localhost', 8888)

        # Bind the socket to the server address
        self.server_socket.bind(server_address)

        # Listen for incoming connections
        self.server_socket.listen(2)
        print("Server is listening for connections...")

        try:
            while True:
                # Accept a client connection
                client_socket, client_address = self.server_socket.accept()
                print("Accepted connection from:", client_address)

                # Append the client connection to the list
                self.clients.append(client_socket)

                # Get the player number for this client
                player_number = len(self.clients)

                # Start a new thread to handle the client
                client_thread = threading.Thread(target=self.handle_client, args=(client_socket, player_number))
                client_thread.start()

                # Check if all players have connected
                if len(self.clients) == 2:
                    # Reset the choices and event for a new game
                    self.player_choices.clear()
                    self.choices_event.clear()

        finally:
            # Close the server socket
            self.server_socket.close()

if __name__ == '__main__':
    server = Server()
    server.start_server()