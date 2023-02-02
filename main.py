# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "zapier-cobras",  # TODO: Your Battlesnake Username
        "color": "#ff6600",  # TODO: Choose color
        "head": "viper",  # TODO: Choose head
        "tail": "bolt",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    is_move_safe = {
      "up": True, 
      "down": True, 
      "left": True, 
      "right": True
    }
    next_move = None

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        print(f"Neck is left of head. Left is not safe.")
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        print(f"Neck is right of head. Lef is not safe.")
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        print(f"Neck is below of head. Down is not safe.")
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        print(f"Neck is above of head. Up is not safe.")
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    print(f"Board height: {board_height}")
    print(f"Board width: {board_width}")
    print(f"Head position: {my_head}")
    if my_head["y"] == board_height - 1:
      print(f"At top of board. Up is not safe.")
      is_move_safe["up"] = False
    elif my_head["y"] == 0:
      print(f"At bottom of board. Down is not safe.")
      is_move_safe["down"] = False

    if my_head["x"] == board_width - 1:
      print(f"At right of board. Right is not safe.")
      is_move_safe["right"] = False
    elif my_head["x"] == 0:
      print(f"At left of board. Left is not safe.")
      is_move_safe["left"] = False

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']
    above_head = {
      "x": my_head["x"],
      "y": my_head["y"] + 1
    }
    below_head = {
      "x": my_head["x"],
      "y": my_head["y"] - 1
    }
    left_head = {
      "x": my_head["x"] - 1,
      "y": my_head["y"]
    }
    right_head = {
      "x": my_head["x"] + 1,
      "y": my_head["y"]
    }
    for coordinate in my_body:
      if coordinate == above_head:
        print(f"Body is above head. Up is not safe.")
        is_move_safe["up"] = False
      elif coordinate == below_head:
        print(f"Body is below head. Up is not safe.")
        is_move_safe["down"] = False
      elif coordinate == left_head:
        print(f"Body is left of head. Left is not safe.")
        is_move_safe["left"] = False
      elif coordinate == right_head:
        print(f"Body is right of head. Right is not safe.")
        is_move_safe["right"] = False

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']
    for opponent in opponents:
      if opponent["name"] == "zapier-cobras":
        continue
      # find if they are next to our head
      for coord in opponent["body"]:
        if abs(my_head["x"] - coord["x"]) == 1:
          if coord["x"] < my_head["x"]:
            is_move_safe["left"] = False
            print("Left is not safe due to opponent")
          else:
            is_move_safe["right"] = False
            print("right is not safe due to opponent")
        elif abs(my_head["y"] - coord["y"]) == 1:
          if coord["y"] < my_head["y"]:
            is_move_safe['down'] = False
            print("down is not safe due to opponent")
          else:
            is_move_safe['up'] = False
            print("up is not safe due to opponent")
            
    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    food = game_state['board']['food']
    for coordinate in food:
      if coordinate == above_head and is_move_safe["up"]:
        print(f"Food is above head")
        next_move = "up"
      elif coordinate == below_head and is_move_safe["down"]:
        print(f"Food is below head")
        next_move = "down"
      elif coordinate == left_head and is_move_safe["left"]:
        print(f"Food is left of head.")
        next_move = "left"
      elif coordinate == right_head and is_move_safe["right"]:
        print(f"Food is right of head.")
        next_move = "right"

    # Choose a random move from the safe ones
    if not next_move:
      next_move = random.choice(safe_moves)

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info, 
        "start": start, 
         "move": move, 
        "end": end
    })
