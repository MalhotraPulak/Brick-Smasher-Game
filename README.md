### Classic Brick Smasher Game
- [Inspiration](https://dx-ball.ru/)
- Playable in terminal 
- To run 
```shell
git clone https://github.com/PulakIIIT/Brick-Smasher-Game
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```
- Code written in modular way
- Bonus Implemented: None
- Functionality : As mentioned in assignment doc
- Controls: A to move left, D to move right
- Powerups (Symbol is the corresponding number): 
    0. Shrink
    1. Expand
    2. Multiply balls
    3. Fast balls
    4. Through balls
    5. Grab ball
	6. Shooting paddle
- All powerups (except Multiply ball) last 10 seconds
- Q to quit, R to Restart
- 3 Levels
- Last level with UFO boss
- UFO health 20 
- 5 seconds after level starts time attack mode begins
	- Bricks move 1 level down everytime ball hits paddle
- UFO drops bomb which reduces health by one
- Types of brick:
	Red - 1 strength
	Blue - 2 strenght
	Cyan - 3 strength
	Green- Unbreakable 
	Grey - UFO 
	Rainbow - Keeps changing strength until hit
- Customizable layout through CSV file, make your own levels easily
- Enjoy!
