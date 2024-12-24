import pygame
import random
import math

WHITE_COLOR = (255, 255, 255)
BLACK_COLOR = (0, 0, 0)


class GameController:
    def __init__(self) -> None:
        # option initialize
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen_width = 800
        self.screen_height = 600
        self.screen_option = (self.screen_width, self.screen_height)
        self.background_color = BLACK_COLOR
        self.background_thickness = int(round((self.screen_width / self.screen_height) * 10, 0)) # out boundary 13..
        
        # screen initialize
        self.screen = self.init_screen()
        
        
        # bee initialize
        self.count = 20
        self.bees = []
        
        self.init_bee()

    # init screen
    def init_screen(self) -> pygame.Surface:
        return pygame.display.set_mode(self.screen_option)
    
    # init object
    def init_bee(self) -> None:
        for _ in range(self.count):
            x = self.screen_width / 2
            y = self.screen_height / 2
            bee = Bee([x, y])
            self.bees.append(bee)
            
    
    # draw boundary
    def draw_boundary(self) -> None:
        return pygame.draw.rect(self.screen, WHITE_COLOR, 
                                self.screen.get_rect(), 
                                int(round((self.screen_width / self.screen_height) * 10, 0)))
        
    
    # draw bee object
    def draw_bee(self) -> None:
        for bee in self.bees:
            bee.update(self.bees, self.screen)
                    
    def run(self) -> None:
        start = True
        
        while start:
            self.clock.tick(15) # 30 fps
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    start = False
            
            # fill black color to background
            self.screen.fill(self.background_color)
            
            # boundary
            self.draw_boundary()
            
            # draw bee
            self.draw_bee()
            # pygame.draw.circle(self.screen, (255, 255, 255), (int(self.screen_width / 2), int(self.screen_height / 2)), int(round((self.screen_width / self.screen_height) * 50, 0)))
            
            # update frame
            pygame.display.flip()
        
        # exist
        pygame.quit()
        
        
# bee
class Bee:
    def __init__(self, position: list) -> None:
        # object position
        self.position = position
        
        # object velocity
        self.speedX = random.uniform(-1, 1) * 0.5
        self.speedY = random.uniform(-1, 1) * 0.5
        
        # object image
        self.background_image = pygame.image.load("bee.png")
        
        # object perception radius
        self.perception_radius = 100
        
        # object separation distance
        self.separation_distance = int(self.perception_radius / 2)
        
        self.max_speed = 3
        
    # draw 'bee'
    def draw(self, screen: pygame.Surface) -> None:
    
        screen.blit(self.background_image, self.position)
        
        

    def update(self, bees: list, screen: pygame.Surface):
        # Updates based on flocking rules
        avg_speedX, avg_speedY = 0, 0
        avg_positionX, avg_positionY = 0, 0
        avg_separationX, avg_separationY = 0, 0
        neighbors = 0
        
        
        # 먼저, update 할때, 자기 자신이, 범위를 벗어났는지 확인하자.
        # self.boundary()

        # Loop through other bees
        for bee in bees:
            if bee == self:
                continue

            bee_posX, bee_posY = bee.get_position()
            bee_speedX, bee_speedY = bee.get_speed()
            distance = self.euclidean_distance(bee)

            # Perception rule (check if within the perception radius)
            if distance < self.perception_radius:
                avg_speedX += bee_speedX
                avg_speedY += bee_speedY
                avg_positionX += bee_posX
                avg_positionY += bee_posY

                # Separation rule (check if within the separation distance)
                if distance < self.separation_distance:
                    diffX = self.position[0] - bee_posX
                    diffY = self.position[1] - bee_posY
                    mag = math.sqrt(diffX**2 + diffY**2)

                    # Avoid division by zero and normalize the vector
                    if mag != 0:
                        diffX /= mag
                        diffY /= mag
                    
                    avg_separationX += diffX
                    avg_separationY += diffY

                neighbors += 1

        # Calculate averages if there are neighbors
        if neighbors > 0:
            avg_positionX /= neighbors
            avg_positionY /= neighbors
            avg_speedX /= neighbors
            avg_speedY /= neighbors
            avg_separationX /= neighbors
            avg_separationY /= neighbors

        # Update the velocity and position based on flocking behavior
        self.speedX += avg_speedX * 0.01 + avg_separationX * 0.05
        self.speedY += avg_speedY * 0.01 + avg_separationY * 0.05

        # Limit the speed to the max speed
        speed_magnitude = math.sqrt(self.speedX**2 + self.speedY**2)
        if speed_magnitude > self.max_speed:
            self.speedX = (self.speedX / speed_magnitude) * self.max_speed
            self.speedY = (self.speedX / speed_magnitude) * self.max_speed

        # Update the position
        self.position[0] += self.speedX / 5
        self.position[1] += self.speedY / 5
        
        self.draw(screen)
        
            
            
    # Get position
    def get_position(self) -> tuple:
        return self.position
    
    # Get Speed
    def get_speed(self) -> tuple:
        return (self.speedX, self.speedY)
    
    # Calculate distance between self bee and other bee using by euclidean distance
    def euclidean_distance(self, other_bee) -> float:
        self_posX, self_posY = self.get_position()
        posX, posY = other_bee.get_position()
        return math.sqrt((posX - self_posX) ** 2 + (posY - self_posY)** 2)

    
if __name__ == '__main__':
    controller = GameController()
    controller.run()
    
