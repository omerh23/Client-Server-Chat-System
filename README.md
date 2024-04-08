
## Client-Server Chat System

## Overview

This project implements a client-server chat system in Python using TCP sockets. The system allows multiple clients to connect to a central server, exchange messages, and engage in real-time communication. The server facilitates the routing of messages between clients and manages the connection state.

## Features

- **Client-Server Architecture**: Utilizes a client-server model where clients connect to a central server to exchange messages.
- **Real-Time Communication**: Enables real-time messaging between connected clients, facilitating instant communication.
- **Connection Management**: Manages client connections, assigns unique usernames, and maintains a list of connected clients and servers.
- **Round-Trip Time (RTT) Measurement**: Measures the Round-Trip Time (RTT) between clients and servers to optimize communication latency.
- **Chat Interface**: Provides a simple command-line interface for clients to initiate chats, send messages, and close conversations.
- **Scalability**: Designed with scalability in mind to handle a large number of concurrent connections efficiently.
- **Error Handling**: Implements robust error handling to ensure graceful recovery from network errors and exceptions.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/client-server-chat.git
   ```

2. Navigate to the project directory:

   ```bash
   cd client-server-chat
   ```

3. Run the server:

   ```bash
   python server.py
   ```

4. Run the client:

   ```bash
   python client.py
   ```

## Usage

1. Start the server by running `server.py`.
2. Connect clients to the server by running `client.py`.
3. Follow the prompts to initiate chats, send messages, and close conversations.
4. Enjoy real-time communication with other connected clients!

## Configuration

- **Server Port**: Specify the port number on which the server listens for incoming connections.
- **Client Port**: Set the port number used by clients to connect to the server.
- **Server IP Address**: Configure the IP address of the server for client connections.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository, make your changes, and submit a pull request. For major changes, please open an issue first to discuss the proposed changes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This project was inspired by [insert inspiration here].
- Special thanks to [insert names] for their contributions and feedback.

## Contact

For any inquiries or feedback, please contact omerhalfon1234@gmail.com

---

Feel free to customize the README according to your project's specific details, such as additional features, dependencies, usage instructions, and acknowledgments.
