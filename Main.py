from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# List of teams
teams = ['Barcelona', 'Liverpool', 'Bayern Munich', 'Paris Saint-Germain', 'Man city', 'Arsenal','PSV',]

# Set initial team
selected_team = None

# Basic Player Setup for Teams (for simplicity, they are represented by colored cubes)
team_players = {
    'Barcelona': [color.blue, color.red],  # Team colors
    'Liverpool': [color.red, color.green],
    'Bayern Munich': [color.yellow, color.white],
    'Paris Saint-Germain': [color.blue, color.green],
}

# Simple Soccer Ball setup
soccer_ball = Entity(model='sphere', scale=1, color=color.white, position=(0, 0.5, 0))

# Create basic stadium and field
field = Entity(model='plane', scale=(30, 1, 50), color=color.green, collider='box')
goal_left = Entity(model='cube', scale=(1, 2, 5), position=(-15, 1, 0), color=color.red)
goal_right = Entity(model='cube', scale=(1, 2, 5), position=(15, 1, 0), color=color.blue)

# Team Selection Menu
def team_selection():
    global selected_team
    menu = Entity(parent=camera.ui, model='quad', scale=(0.6, 0.8), color=color.black, opacity=0.8, position=(0, 0, 0))
    title = Text(parent=menu, text="Select Your Team", position=(0, 0.3), scale=2, color=color.white)

    def select_team(team_name):
        selected_team = team_name
        print(f"Selected team: {team_name}")
        menu.disable()  # Hide menu
        start_game(team_name)  # Proceed to the game

    buttons = []
    for i, team in enumerate(teams):
        button = Button(parent=menu, text=team, scale=(0.4, 0.1), position=(0, 0.15 - (i * 0.2), 0), color=color.gray, on_click=lambda team=team: select_team(team))
        buttons.append(button)

def start_game(team_name):
    global selected_team
    selected_team = team_name
    print(f"Starting game with team {team_name}.")

    # Create the player character based on the team selection
    player = Entity(model='cube', color=team_players[team_name][0], scale=(1, 2, 1), position=(-5, 1, 0))

    # Create opposing robot team players (AI)
    robots = []
    for i in range(5):  # 5 robots for now
        robot = Entity(model='cube', color=team_players['Barcelona'][1], scale=(1, 2, 1), position=(5, 1, i * 3))
        robots.append(robot)

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

        # Simple AI for robots (move towards the ball)
        for robot in robots:
            direction_to_ball = soccer_ball.position - robot.position
            if direction_to_ball.length() < 10:  # If the robot is close to the ball
                robot.position += direction_to_ball.normalized() * time.dt * 2  # Move towards the ball

    app.run()

# Start the team selection menu
team_selection()

app.run()
