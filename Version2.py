from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random

app = Ursina()

# List of teams
teams = ['Barcelona', 'Liverpool', 'Bayern Munich', 'Paris Saint-Germain', 'Man city', 'Arsenal']

# Set initial team
selected_team = None
ai_team = None

# Basic Player Setup for Teams (for simplicity, they are represented by colored cubes)
team_players = {
    'Barcelona': [color.blue, color.red],  # Team colors
    'Liverpool': [color.green, color.white],
    'Bayern Munich': [color.yellow, color.white],
    'Paris Saint-Germain': [color.blue, color.green],
    'Man city': [color.cyan, color.yellow],
    'Arsenal': [color.red, color.white],
}

# Score and game state
score_left = 0
score_right = 0
game_over = False

# Simple Soccer Ball setup
soccer_ball = Entity(model='sphere', scale=1, color=color.white, position=(0, 0.5, 0), collider='sphere')

# Create basic stadium and field
field = Entity(model='plane', scale=(30, 1, 50), color=color.green, collider='box')
goal_left = Entity(model='cube', scale=(1, 2, 5), position=(-15, 1, 0), color=color.red)
goal_right = Entity(model='cube', scale=(1, 2, 5), position=(15, 1, 0), color=color.blue)

# UI Texts
score_text = Text(text=f"Score: {score_left} - {score_right}", position=(-0.9, 0.45), color=color.white, scale=2)
game_over_text = Text(text="", position=(0, 0.5), color=color.red, scale=3)

# Player and Robot Controllers
player = None
robots = []

# Team Selection Menu
def team_selection():
    global selected_team, ai_team
    menu = Entity(parent=camera.ui, model='quad', scale=(0.6, 0.8), color=color.black, opacity=0.8, position=(0, 0, 0))
    title = Text(parent=menu, text="Select Your Team", position=(0, 0.3), scale=2, color=color.white)

    def select_team(team_name):
        selected_team = team_name
        ai_team = random.choice([team for team in teams if team != selected_team])  # Randomly assign AI team
        print(f"Selected team: {team_name} | AI Team: {ai_team}")
        menu.disable()  # Hide menu
        start_game(team_name, ai_team)  # Proceed to the game

    buttons = []
    for i, team in enumerate(teams):
        button = Button(parent=menu, text=team, scale=(0.4, 0.1), position=(0, 0.15 - (i * 0.2), 0), color=color.gray, on_click=lambda team=team: select_team(team))
        buttons.append(button)

def start_game(player_team, ai_team):
    global selected_team, score_left, score_right, game_over, player, robots
    selected_team = player_team
    ai_team = ai_team
    score_left = 0
    score_right = 0
    game_over = False

    # Create the player character based on the team selection
    player = Entity(model='cube', color=team_players[player_team][0], scale=(1, 2, 1), position=(-5, 1, 0), collider='box', origin_y=0.5)

    # Create opposing robot team players (AI)
    robots = []
    for i in range(5):  # 5 robots for now
        robot = Entity(model='cube', color=team_players[ai_team][1], scale=(1, 2, 1), position=(5, 1, i * 3), collider='box', origin_y=0.5)
        robots.append(robot)

    # Soccer Ball Controls
    def update():
        global score_left, score_right, game_over

        # Ball movement
        if soccer_ball.position.y < 0:
            soccer_ball.position = Vec3(0, 0.5, 0)  # Reset ball position if it falls below the ground

        # Ball in goal check
        if soccer_ball.position.x < -15 and abs(soccer_ball.position.z) < 2:
            score_right += 1
            print(f"Goal! Score: {score_left} - {score_right}")
            soccer_ball.position = Vec3(0, 0.5, 0)  # Reset ball to center

        if soccer_ball.position.x > 15 and abs(soccer_ball.position.z) < 2:
            score_left += 1
            print(f"Goal! Score: {score_left} - {score_right}")
            soccer_ball.position = Vec3(0, 0.5, 0)  # Reset ball to center

        # Update the score text
        score_text.text = f"Score: {score_left} - {score_right}"

        # Ball control (kick action)
        if held_keys['space']:
            soccer_ball.position += player.forward * 0.5  # Kick the ball forward

        # Player movement
        if held_keys['w']:
            player.position += Vec3(0, 0, 1) * time.dt * 5
        if held_keys['s']:
            player.position += Vec3(0, 0, -1) * time.dt * 5
        if held_keys['a']:
            player.position += Vec3(-1, 0, 0) * time.dt * 5
        if held_keys['d']:
            player.position += Vec3(1, 0, 0) * time.dt * 5

        # Collision detection for ball and player
        if player.intersects(soccer_ball).hit:
            soccer_ball.position += player.forward * 0.5  # Push the ball forward

        # Simple AI for robots (move towards the ball)
        for robot in robots:
            direction_to_ball = soccer_ball.position - robot.position
            if direction_to_ball.length() < 10:  # If the robot is close to the ball
                robot.position += direction_to_ball.normalized() * time.dt * 2  # Move towards the ball

        # Game Over Check
        if score_left >= 5 or score_right >= 5:  # Arbitrary score limit to end game
            game_over = True
            game_over_text.text = "Game Over! Press 'R' to Restart"
            restart_button = Button(parent=camera.ui, text="Restart", scale=(0.3, 0.1), position=(0, -0.2), color=color.gray, on_click=restart_game)

    app.run()

def restart_game():
    global score_left, score_right, game_over, soccer_ball
    score_left = 0
    score_right = 0
    game_over = False
    soccer_ball.position = Vec3(0, 0.5, 0)  # Reset ball
    game_over_text.text = ""
    start_game(selected_team, ai_team)  # Restart game with selected team

# Start the team selection menu
team_selection()

app.run()

