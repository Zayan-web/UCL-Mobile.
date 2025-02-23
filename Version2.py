from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# Liverpool Starting 11 Setup (4-3-3 Formation)
liverpool_players = [
    {"name": "Alisson", "position": Vec3(-12, 1, 0), "color": color.green},  # Goalkeeper
    {"name": "Trent", "position": Vec3(-9, 1, 2), "color": color.red},  # Right-back
    {"name": "Van Dijk", "position": Vec3(-9, 1, -2), "color": color.red},  # Center-back
    {"name": "Matip", "position": Vec3(-6, 1, -2), "color": color.red},  # Center-back
    {"name": "Robertson", "position": Vec3(-6, 1, 2), "color": color.red},  # Left-back
    {"name": "Henderson", "position": Vec3(-3, 1, 3), "color": color.red},  # Midfielder
    {"name": "Fabinho", "position": Vec3(-3, 1, 0), "color": color.red},  # Defensive Midfielder
    {"name": "Thiago", "position": Vec3(-3, 1, -3), "color": color.red},  # Midfielder
    {"name": "Salah", "position": Vec3(0, 1, 3), "color": color.red},  # Right-winger
    {"name": "Jota", "position": Vec3(0, 1, 0), "color": color.red},  # Forward
    {"name": "Diaz", "position": Vec3(0, 1, -3), "color": color.red},  # Left-winger
    {"name": "Nunez", "position": Vec3(3, 1, 0), "color": color.red},  # Striker
]

# New AI Team (5 programmed set of moves)
ai_players = [
    {"name": f"AI Player {i+1}", "position": Vec3(10, 1, i*3), "color": color.blue} for i in range(5)
]

# Simple Soccer Ball setup
soccer_ball = Entity(model='sphere', scale=1, color=color.white, position=(0, 0.5, 0))

# Create basic stadium and field
field = Entity(model='plane', scale=(30, 1, 50), color=color.green, collider='box')
goal_left = Entity(model='cube', scale=(1, 2, 5), position=(-15, 1, 0), color=color.red)  # Left goal
goal_right = Entity(model='cube', scale=(1, 2, 5), position=(15, 1, 0), color=color.blue)  # Right goal

# 3D Soccer Nets (Expanded version for goals)
net_left = Entity(model='cube', scale=(2, 3, 1), position=(-15, 2, 0), color=color.white)
net_right = Entity(model='cube', scale=(2, 3, 1), position=(15, 2, 0), color=color.white)

# AI set of moves
def ai_move(ai_player):
    move = random.choice(['attack', 'defend', 'pass', 'shoot', 'block'])
    if move == 'attack':
        ai_player.position += Vec3(1, 0, 0) * time.dt * 2  # Move forward
    elif move == 'defend':
        ai_player.position += Vec3(-1, 0, 0) * time.dt * 2  # Move backward
    elif move == 'pass':
        ai_player.position += Vec3(0, 0, random.choice([1, -1])) * time.dt  # Move laterally
    elif move == 'shoot':
        if soccer_ball.position.x > 10:
            soccer_ball.position = Vec3(15, 0.5, 0)  # "Shoot" ball towards the goal
    elif move == 'block':
        ai_player.position += Vec3(0, 0, random.choice([1, -1])) * time.dt  # Move randomly

# Display Game Rules
def display_rules():
    rules = """
    Football (Soccer) Rules:
    1. Objective: Score more goals than the opponent.
    2. Match Duration: Standard game has two 45-minute halves.
    3. Scoring: A goal is scored when the ball crosses the goal line.
    4. Offside: A player is offside if they are closer to the opponent's goal than the ball.
    5. Fouls: Includes tripping, kicking, or pushing an opponent unfairly.
    6. Goalkeeper: Only allowed to handle the ball within the penalty area.
    """
    rules_text = Text(parent=camera.ui, text=rules, scale=1, position=(-0.5, 0.4), color=color.white, background=True)

# Team Selection Menu
def team_selection():
    menu = Entity(parent=camera.ui, model='quad', scale=(0.6, 0.8), color=color.black, opacity=0.8, position=(0, 0, 0))
    title = Text(parent=menu, text="Select Your Team", position=(0, 0.3), scale=2, color=color.white)
    
    def select_team():
        menu.disable()  # Hide menu
        display_rules()  # Show rules before starting the game
        invoke(start_game, delay=5)  # Start game after 5 seconds for players to read the rules

    button = Button(parent=menu, text='Liverpool', scale=(0.4, 0.1), position=(0, 0, 0), color=color.gray, on_click=select_team)

def start_game():
    # Setup the player (Liverpool)
    player = Entity(model='cube', color=color.red, scale=(1, 2, 1), position=liverpool_players[10]["position"])

    # Create Liverpool players
    for player_data in liverpool_players:
        Entity(model='cube', color=player_data["color"], scale=(1, 2, 1), position=player_data["position"])

    # Create opposing AI team players
    for ai_data in ai_players:
        Entity(model='cube', color=ai_data["color"], scale=(1, 2, 1), position=ai_data["position"])

    # Soccer Ball Controls
    def update():
        # Ball movement
        if soccer_ball.position.y < 0:
            soccer_ball.position = Vec3(0, 0.5, 0)  # Reset ball position if it falls below the ground

        # Basic player movement
        if held_keys['w']:
            player.position += Vec3(0, 0, 1) * time.dt
        if held_keys['s']:
            player.position += Vec3(0, 0, -1) * time.dt
        if held_keys['a']:
            player.position += Vec3(-1, 0, 0) * time.dt
        if held_keys['d']:
            player.position += Vec3(1, 0, 0) * time.dt

        # Collision detection for ball and player
        if player.intersects(soccer_ball).hit:
            soccer_ball.position += player.forward * 0.5  # Push the ball forward

        # Simple AI behavior (random moves)
        for ai_data in ai_players:
            ai_move(ai_data)

    app.run()

# Start the team selection menu
team_selection()

app.run()
