- [1. ScorchedEarth](#1-scorchedearth)
- [2. Controls](#2-controls)
- [3. Scores](#3-scores)
- [4. Usage](#4-usage)

# 1. ScorchedEarth

ScorchedEarth is a turn-based artillery game.
The game screen consists of a terrain, on which the players as tanks are
shown.
The players in turns try to shoot each other (the winner is the last remaining player).

# 2. Controls

The shooting is controlled by specifying the angle (left and right arrow keys) and power of the shot (up and down arrow keys). The
projectile trajectory is influenced by the gravity (i.e., the shot curve is parabol-
ic). The window edges are “rubber”, i.e., the projectiles bounce. To shoot the projectile, press space.

# 3. Scores

The game awards accuracy of the player. If the player managed to hit a tank within its 1st or 2nd shot 
they get 50 and 25 points respectively. Otherwise, just 10 points. The winner gets 10 points at the end of the game.

# 4. Usage

Make sure tkinter is installed and pip packages are fullfilled:
```
pip install -r requirements.txt
```

```
python main.py
```