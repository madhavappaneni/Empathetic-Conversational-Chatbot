# Topic based Empathetic Chatbot

## Instructions

Before you begin, ensure you have met the following requirements:

- Python 3.x installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).

- Node.js and npm installed on your machine. You can download them from [nodejs.org](https://nodejs.org/).


### Backend Installation

1. Clone the repository to your local machine using the following command:

   ```
   git clone https://github.com/madhavappaneni/Empathetic_Conversational_Chatbot
   ```
2. Naviage to the project directory
   ```
   cd ./application./backend
   ```
3. Create a virtual environment (optional but recommended)
   ```
   python -m venv venv
   ```
4. Activate the virtual environment:
   On Windows
    ``` 
    venv\Scripts\activate
    ```
    On macOS and Linux

    ```
    source venv/bin/activate
    ```
5. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
6. Running the Application
    ```
    flask run
    ```
   
### Frontend Installation
1. Naviage to the project directory
   ```
   cd ./application./frontend

2. Install project dependencies:
   ```
   npm install
   ```
4. Start the development server:
   ```
   npm start
   ```
3. By default, the application will be accessible at http://localhost:4200



Following this steps should open the application with a chatbot interface. Feel free to experiment with the it. 

The chatbot maintains a context about the previous conversations to provide better and human-like responses. 

To refresh/clear the context and start a new conversation, reload the page, by clicking on Re-load button in your browser.