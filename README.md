# dnd-sheduling
Bot to do dnd sheduling in python
# Installation
Install python and the requirements via following command
```bash
pip install ./requirements.txt
```
# Usage
Create an env file from the .env_template and add the API Token for your own bot and start the bot using following command
```bash
python3 main.py
```
It works by reading all messages in a discord channel and extracting all lines with following format: 
```txt
[mention_user1] [character1] [level1]
[mention_user2] [character2] [level2]
[mention_user3] [character3] [level3]

Date: mm/dd/YYYY

DM: [mention_user4]
```
According to the 'player_ranks' list in the main.py it will then send or update a schedule message with all games grouped by the month of the game in descending order. 
Those games without a valid date format it will append at the end in order of 'newest message first'