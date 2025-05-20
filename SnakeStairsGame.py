import random

# Class representing a player in the game
class Player:
    def __init__(self, start_position=1, imunity=0):
        # Initialize the player's position, immunity, and snake counter
        self.position = start_position
        self.imunity = imunity
        self.snakes = 0

    # Simulates a dice roll and moves the player
    def walk_dice(self, stairs_prob):
        self.position += random.randint(1, 6)  # Roll a 6-sided dice
        self.test_stairs(stairs_prob)  # Check if the player lands on a stair
        self.test_snakes()  # Check if the player lands on a snake

    # Checks if the player lands on a stair and moves them up if applicable
    def test_stairs(self, probability):
        if random.randint(1, 100) <= probability:  # Probability to climb the stair
            match self.position:
                case 3:
                    self.position = 16
                case 5:
                    self.position = 7
                case 15:
                    self.position = 25
                case 18:
                    self.position = 20
                case 21:
                    self.position = 32

    # Checks if the player lands on a snake and moves them down if applicable
    def test_snakes(self):
        last_position = self.position  # Store the current position
        match self.position:
            case 12:
                self.position = 2
            case 14:
                self.position = 11
            case 17:
                self.position = 4
            case 31:
                self.position = 19
            case 35:
                self.position = 22

        # If the position changed, increment the snake counter
        if last_position != self.position:
            self.snakes += 1

        # If the player has immunity, restore their position and remove immunity
        if self.imunity == 1:
            self.imunity = 0
            self.position = last_position

# Class representing the game logic
class Game:
    def __init__(self):
        # Initialize game parameters
        self.Games_Number = 10000  # Number of games to simulate
        self.player1 = Player()  # Player 1
        self.player2 = Player()  # Player 2
        self.final_position = 36  # Winning position
        self.start_position_player2 = 1  # Starting position for Player 2
        self.stairs_probability = 100  # Probability of climbing stairs (in percentage)
        self.imunity = 0  # Immunity status for Player 2 (0 = no immunity, 1 = immunity)
        self.run()  # Start the simulation

    # Simulates the games and calculates results
    def simulation(self):
        snakes = 0  # Total number of snakes encountered
        throws = 0  # Total number of dice throws
        winner = []  # List to store the winners of each game

        # Simulate the specified number of games
        for i in range(1, self.Games_Number):
            # Reset players for each game
            self.player1.__init__()
            self.player2.__init__(self.start_position_player2, self.imunity)

            # Simulate a single game
            while True:
                self.player1.walk_dice(self.stairs_probability)  # Player 1's turn
                throws += 1
                if self.player1.position >= self.final_position:  # Check if Player 1 wins
                    winner.append(1)
                    break
                self.player2.walk_dice(self.stairs_probability)  # Player 2's turn
                throws += 1
                if self.player2.position >= self.final_position:  # Check if Player 2 wins
                    winner.append(2)
                    break

            # Count the total number of snakes encountered
            snakes += self.player1.snakes + self.player2.snakes

        # Calculate and return the results
        return [winner.count(1) / self.Games_Number,  # Probability of Player 1 winning
                snakes / self.Games_Number,  # Average number of snakes encountered
                throws / self.Games_Number]  # Average number of dice throws

    # Runs the simulation and answers the questions
    def run(self):
        # Question 1: Probability of Player 1 winning
        [win_prob, snakes, throws] = self.simulation()
        print(f"Question 1:")
        print(f"Player 1 win probability: {win_prob}")

        # Question 2: Average number of snakes encountered
        print(f"Question 2:")
        print(f"Average snakes: {snakes}")

        # Question 3: Average number of dice throws with 50% stair probability
        self.stairs_probability = 50
        [win_prob, snakes, throws] = self.simulation()
        print(f"Question 3:")
        print(f"Average throws with 50% stairs probability: {throws}")

        # Question 4: Best starting position for Player 2 to balance win probabilities
        self.stairs_probability = 100
        best_prob = 1
        for i in range(1, 10):  # Test starting positions from 1 to 10
            self.start_position_player2 = i
            [win_prob, snakes, throws] = self.simulation()
            if abs(win_prob - 0.5) <= abs(best_prob - 0.5):  # Find the closest to 50% win probability
                best_prob = win_prob
                best_start_position_player2 = i
        print(f"Question 4:")
        print(f"Best start position: {best_start_position_player2}")
        print(f"Player 1 win probability in this case: {best_prob}")

        # Question 5: Probability of Player 1 winning when Player 2 has immunity
        self.imunity = 1  # Grant immunity to Player 2
        self.start_position_player2 = 1
        [win_prob, snakes, throws] = self.simulation()
        print(f"Question 5:")
        print(f"Player 1 win probability: {win_prob}")


# Entry point of the program
if __name__ == "__main__":
    game = Game()