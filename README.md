# Django Chat Application

Welcome to our Django-based chat application! This application allows users to register, log in, add friends, send and remove messages, all in real-time using WebSockets. It also provides a clean and user-friendly interface for seamless communication.

## Features

- **User Authentication:** Users can register and log in securely using JWT token authentication.
- **Real-Time Messaging:** Utilizing WebSockets for real-time communication, ensuring instant message delivery.
- **Add Friend Functionality:** Users can add friends to their contact list for easy communication.
- **Send and Remove Messages:** Sending messages to friends and removing messages from the chat history.
- **DRF Integration:** The backend utilizes Django Rest Framework (DRF) for handling user updates and authentication.

## Technologies Used

- **Django:** The web framework used for backend development.
- **WebSocket:** For real-time bidirectional communication between clients and server.
- **JavaScript & jQuery Ajax:** Handling asynchronous requests for dynamic updates without page reloads.
- **HTML & CSS:** For building the frontend user interface and styling.
- **Django Rest Framework (DRF):** Used for API development and integrating with the frontend.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your_username/ChatApp.git
```

2. Navigate to the project directory:

```bash
cd django-chat-app
```

3. Create a virtual environment:

```bash
python3 -m venv venv
```

4. Activate the virtual environment:

- On macOS and Linux:

```bash
source venv/bin/activate
```

- On Windows:

```bash
venv\Scripts\activate
```

5. Install the dependencies:

```bash
pip install -r requirements.txt
```

6. Run migrations:

```bash
python manage.py migrate
```

7. Start the development server:

```bash
python manage.py runserver
```

8. Access the application at `http://localhost:8000` in your web browser.

## Usage

1. Register a new account or log in with existing credentials.
2. Add friends using their usernames.
3. Start sending and receiving real-time messages with added friends.
4. Remove messages or contacts as needed.
5. See user profile with friend list.

## Contributing

We welcome contributions to improve this chat application. Feel free to fork the repository, make changes, and submit pull requests.
