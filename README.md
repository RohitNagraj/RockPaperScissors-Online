# RockPaperScissors-Online
An online version of Rock Paper Scissors game made with PyGame and Socket. <br />
This runs on a server that handles each game individually and each game instance has 2 clients attached to it. <br />
Can be played with anyone anywhere across the world. <br />

## Installation
* Clone the repo
* Navigate to the directory and run `pip install -r requirements.txt`
* Change the local IP addresses of the server in `network.py` and `server.py` to your local IP address
	* To deploy on a cloud server, add VM's internal IP in the `server.py` file and VM's external IP in `network.py`
* Run `server.py`
* Run as many `client.py` instances as you want!

## Screenshots
![Alt](/Screenshots/waiting.png "Waiting Screen")
![Alt](/Screenshots/playing.png "Game Screen")
![Alt](/Screenshots/complete.png "Win Screen")
