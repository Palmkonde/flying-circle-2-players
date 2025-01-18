# JSON structure
"""
{
  "state": 0,                                    0: waiting  1: playing
  "coin_position": [
    {
      "id": 0,
      "position": [x, y],                        Coin position (x, y)
      "is_collected": false                      True, False
    },
    {
      "id": 1,
      "position": [x, y],
      "is_collected": false
    }
                                                  In Engine set coin id, 0-9
  ],
  "players": [
    {
      "id": 1,                                    Player id (1)
      "player": {
        "center": [x, y],
        "direction": [dx, dy],                    Use this as direction marker, it's on player cirle edge, pointing toward.
        "score": 10                               Integer
      }
    },
    {
      "id": 2,
      "player": {
        "center": [x, y],
        "direction": [dx, dy],                              
        "score": 8
      }
    }
  ]
}
"""




from game_engine import *
from pprint import pprint


# client inputs
client1_input = "w"
client2_input = "a"

# run engine
if __name__ == "__main__":

    SCREEN = (500, 600)

    player1 = PlayerCircle(center=(200, 400), radius=50, id=1, direction=0)
    player2 = PlayerCircle(center=(300, 400), radius=50, id=2, direction=math.pi / 2)

    engine = GameEngine(player1=player1, player2=player2, screen=SCREEN)

    while True:
        game_state = engine.run(player1key=key_apply(client1_input), player2key=key_apply(client2_input))

        pprint(game_state)  # Output game data JSON format



