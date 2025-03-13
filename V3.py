from panda3d.core import Point3, CollisionNode, CollisionSphere
from panda3d.gui import DirectButton
from direct.showbase.ShowBase import ShowBase
from math import radians
import random

class UCLGame(ShowBase):
    def __init__(self):
        super().__init__()

        # List of teams
        self.teams = ['Barcelona', 'Liverpool', 'Bayern Munich', 'Paris Saint-Germain', 'Man city', 'Arsenal']

        # Set initial team
        self.selected_team = None
        self.ai_team = None

        # Basic Team Players (using colors for simplicity)
        self.team_players = {
            'Barcelona': (0, 0, 1),  # Blue
            'Liverpool': (0, 1, 0),  # Green
            'Bayern Munich': (1, 1, 0),  # Yellow
            'Paris Saint-Germain': (0, 0, 1),  # Blue
            'Man city': (0, 1, 1),  # Cyan
            'Arsenal': (1, 0, 0),  # Red
        }

        self.score_left = 0
        self.score_right = 0
        self.game_over = False

        # Set up 3D Environment
        self.setup_scene()
        self.setup_ui()

        # Team selection menu
        self.create_team_selection()

        # Set up movement keys
        self.accept('w', self.move_player, [0, 0, 1])  # Forward
        self.accept('s', self.move_player, [0, 0, -1])  # Backward
        self.accept('a', self.move_player, [-1, 0, 0])  # Left
        self.accept('d', self.move_player, [1, 0, 0])  # Right
        self.accept('space', self.kick_ball)  # Kick ball with space

    def setup_scene(self):
        # Basic soccer field
        self.field = self.loader.loadModel("models/plane")  # Use a plane as field
        self.field.set_scale(30, 1, 50)
        self.field.reparent_to(self.render)

        # Create goalposts
        self.goal_left = self.create_goal(-15, 0)
        self.goal_right = self.create_goal(15, 0)

        # Soccer ball
        self.soccer_ball = self.create_soccer_ball()

    def create_goal(self, x, z):
        goal = self.loader.loadModel("models/box")  # Use a box as goal
        goal.set_scale(1, 2, 5)
        goal.set_pos(x, 0, z)
        goal.reparent_to(self.render)
        return goal

    def create_soccer_ball(self):
        soccer_ball = self.loader.loadModel("models/sphere")
        soccer_ball.set_scale(1)
        soccer_ball.set_pos(0, 0.5, 0)
        soccer_ball.reparent_to(self.render)

        # Add collision
        ball_collision = CollisionNode('ball')
        ball_collision.add_solid(CollisionSphere(0, 0, 0, 1))
        soccer_ball.attach_collision_node(ball_collision)

        return soccer_ball

    def setup_ui(self):
        # UI for score and game over text
        self.score_text = self.aspect2d.attach_new_node(self.loader.load_model("models/text"))
        self.score_text.set_scale(0.1)
        self.score_text.set_pos(-0.9, 0, 0.45)

        self.game_over_text = self.aspect2d.attach_new_node(self.loader.load_model("models/text"))
        self.game_over_text.set_scale(0.1)
        self.game_over_text.set_pos(0, 0, 0.5)
        self.game_over_text.hide()

    def create_team_selection(self):
        # Create team selection buttons
        for i, team in enumerate(self.teams):
            button = DirectButton(text=team, scale=(0.4, 0.1), pos=(0, 0, 0.2 - (i * 0.2)), command=self.select_team, extraArgs=[team])

    def select_team(self, team_name):
        self.selected_team = team_name
        self.ai_team = random.choice([team for team in self.teams if team != self.selected_team])  # Randomly assign AI team
        print(f"Selected team: {self.selected_team} | AI Team: {self.ai_team}")
        self.start_game()

    def start_game(self):
        self.game_over = False
        self.score_left = 0
        self.score_right = 0
        self.update_score()

        # Reset soccer ball position
        self.soccer_ball.set_pos(0, 0.5, 0)

        # Create player character
        self.player = self.create_player(self.selected_team)

        # Create AI robots (opponents)
        self.robots = [self.create_robot(self.ai_team, i) for i in range(5)]

        # Disable the team selection screen
        self.accept('space', self.kick_ball)

        self.taskMgr.add(self.update_game, 'update_game')

    def update_game(self, task):
        if self.game_over:
            return task.done

        # Ball movement (check if it goes out of bounds)
        if self.soccer_ball.get_z() < 0:
            self.soccer_ball.set_pos(0, 0.5, 0)  # Reset ball position if it falls below the ground

        # Ball in goal check (goal scoring)
        if self.soccer_ball.get_x() < -15 and abs(self.soccer_ball.get_z()) < 2:
            self.score_right += 1
            print(f"Goal! Score: {self.score_left} - {self.score_right}")
            self.reset_ball()

        if self.soccer_ball.get_x() > 15 and abs(self.soccer_ball.get_z()) < 2:
            self.score_left += 1
            print(f"Goal! Score: {self.score_left} - {self.score_right}")
            self.reset_ball()

        # Update score
        self.update_score()

        # AI behavior: robots move towards the ball
        for robot in self.robots:
            direction_to_ball = self.soccer_ball.get_pos() - robot.get_pos()
            if direction_to_ball.length() < 10:
                robot.set_pos(robot.get_pos() + direction_to_ball.normalized() * 0.1)

        # Check game over condition
        if self.score_left >= 5 or self.score_right >= 5:
            self.game_over = True
            self.game_over_text.show()
            self.game_over_text.set_text("Game Over! Press 'R' to Restart")

        return task.cont

    def update_score(self):
        self.score_text.set_text(f"Score: {self.score_left} - {self.score_right}")

    def reset_ball(self):
        self.soccer_ball.set_pos(0, 0.5, 0)

    def create_player(self, team_name):
        player = self.loader.loadModel("models/box")
        player.set_scale(1, 2, 1)
        player.set_pos(-5, 1, 0)
        player.set_color(*self.team_players[team_name])
        player.reparent_to(self.render)

        self.player = player
        return player

    def create_robot(self, team_name, index):
        robot = self.loader.loadModel("models/box")
        robot.set_scale(1, 2, 1)
        robot.set_pos(5, 1, index * 3)
        robot.set_color(*self.team_players[team_name])
        robot.reparent_to(self.render)
        return robot

    def move_player(self, dx, dy, dz):
        """Move the player in a given direction"""
        self.player.set_pos(self.player.get_pos() + Point3(dx, dy, dz))

    def kick_ball(self):
        """Kick the ball in the direction the player is facing"""
        # Get direction the player is facing (along the X-Z plane)
        player_forward = self.player.get_hpr()[0]  # Getting the heading (rotation on the Y-axis)
        kick_direction = Point3(0, 0, 0)
        
        # Direction vector (move ball in the player's facing direction)
        kick_direction = self.player.getQuat().get_forward()
        self.soccer_ball.set_pos(self.soccer_ball.get_pos() + kick_direction * 3)  # Add movement to the ball

    def restart_game(self):
        self.game_over = False
        self.score_left = 0
        self.score_right = 0
        self.game_over_text.hide()
        self.start_game()

if __name__ == "__main__":
    game = UCLGame()
    game.run()
