import pygame
import random
import math

pygame.init()
pygame.mixer.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Bubble Pop Fun!")
clock = pygame.time.Clock()

# Load sounds
try:
    pop_sound = pygame.mixer.Sound("pop.wav")
    laugh_sound = pygame.mixer.Sound("laugh.wav")
except:
    # Create dummy sound objects if files aren't found
    class DummySound:
        def play(self): pass
    pop_sound = DummySound()
    laugh_sound = DummySound()

# Define bright, child-friendly colors
COLORS = [
    (255, 0, 0),     # Red
    (0, 255, 0),     # Green
    (0, 0, 255),     # Blue
    (255, 255, 0),   # Yellow
    (255, 0, 255),   # Pink
    (0, 255, 255),   # Cyan
    (255, 165, 0)    # Orange
]

# Background with gradient
def draw_background():
    for y in range(600):
        # Create a soft gradient from light blue to light purple
        color = (200 - y//3, 200 - y//6, 255)
        pygame.draw.line(screen, color, (0, y), (800, y))
    
    # Add some clouds
    for x in [100, 300, 500, 700]:
        pygame.draw.ellipse(screen, (255, 255, 255), (x-40, 50, 80, 40))
        pygame.draw.ellipse(screen, (255, 255, 255), (x-20, 30, 80, 40))
        pygame.draw.ellipse(screen, (255, 255, 255), (x, 50, 80, 40))

# Character faces on shapes
def draw_face(surface, x, y, size, happy=True):
    # Convert size to integer to avoid float issues
    size = int(size)
    
    # Eyes
    eye_size = max(4, size // 5)
    pygame.draw.circle(surface, (255, 255, 255), (int(x - size//3), int(y - size//5)), eye_size)
    pygame.draw.circle(surface, (255, 255, 255), (int(x + size//3), int(y - size//5)), eye_size)
    
    # Pupils
    pupil_size = max(2, eye_size // 2)
    pygame.draw.circle(surface, (0, 0, 0), (int(x - size//3), int(y - size//5)), pupil_size)
    pygame.draw.circle(surface, (0, 0, 0), (int(x + size//3), int(y - size//5)), pupil_size)
    
    # Mouth
    if happy:
        # Smiling mouth (arc)
        pygame.draw.arc(surface, (0, 0, 0), (int(x - size//2), int(y - size//6), size, size//2), 
                        math.pi * 0.1, math.pi * 0.9, max(2, size//10))
    else:
        # Surprised mouth (circle)
        pygame.draw.circle(surface, (0, 0, 0), (int(x), int(y + size//4)), max(3, size//6))

# Different shape types
class Shape:
    def __init__(self):
        self.x = random.randint(100, 700)
        self.y = random.randint(100, 500)
        self.size = random.randint(30, 60)  # Larger for easier clicking
        self.color = random.choice(COLORS)
        
        # Slower, gentler movement for younger children
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.uniform(-1, 1)
        
        self.popping = False
        self.pop_frames = 15  # Longer animation
        self.shape_type = random.choice(["circle", "star", "heart", "square"])
        self.happy = True
        self.rotation = 0
        self.wobble = random.uniform(0, math.pi * 2)
        self.wobble_speed = random.uniform(0.05, 0.1)

    def draw(self):
        if self.shape_type == "circle":
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
            draw_face(screen, self.x, self.y, self.size, self.happy)
            
        elif self.shape_type == "square":
            rect = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
            pygame.draw.rect(screen, self.color, rect, border_radius=self.size//4)
            draw_face(screen, self.x, self.y, self.size, self.happy)
            
        elif self.shape_type == "heart":
            # Simple heart shape
            points = []
            for i in range(20):
                angle = (i / 20) * 2 * math.pi
                heart_x = self.size * math.sin(angle) * math.sin(angle) * math.sin(angle)
                heart_y = self.size * (13 * math.cos(angle) - 5 * math.cos(2*angle) - 2 * math.cos(3*angle) - math.cos(4*angle)) / 16
                points.append((int(self.x + heart_x), int(self.y - heart_y)))
            
            pygame.draw.polygon(screen, self.color, points)
            draw_face(screen, self.x, self.y - self.size//4, self.size, self.happy)
            
        elif self.shape_type == "star":
            points = []
            for i in range(10):
                angle = math.pi/2 + i * math.pi/5
                r = self.size if i % 2 == 0 else self.size/2
                points.append((
                    int(self.x + r * math.cos(angle + self.rotation)),
                    int(self.y + r * math.sin(angle + self.rotation))
                ))
            pygame.draw.polygon(screen, self.color, points)
            # Convert float to int by using int() instead of division
            face_size = int(self.size / 1.5)
            draw_face(screen, self.x, self.y, face_size, self.happy)
            
        # Add a gentle shimmer/glow around the shape
        for radius in range(3):
            alpha = 100 - radius * 30  # Decreasing opacity
            s = pygame.Surface((int(self.size*2 + 10 + radius*5), int(self.size*2 + 10 + radius*5)), pygame.SRCALPHA)
            # Fix alpha value in tuple
            pygame.draw.circle(s, self.color + (alpha,), 
                              (int(self.size + 5 + radius*2.5), int(self.size + 5 + radius*2.5)), 
                              int(self.size + 2 + radius*2))
            screen.blit(s, (int(self.x - self.size - 5 - radius*2.5), int(self.y - self.size - 5 - radius*2.5)))

    def update(self):
        if self.popping:
            # Playful pop animation
            self.size += 3
            self.pop_frames -= 1
            return self.pop_frames <= 0
        else:
            # Add a gentle wobble for more playfulness
            self.wobble += self.wobble_speed
            wobble_offset = math.sin(self.wobble) * 0.5
            
            # Update position
            self.x += self.speed_x + wobble_offset
            self.y += self.speed_y
            
            # Bounce with a slight randomization for unpredictability
            if self.x < self.size or self.x > 800 - self.size:
                self.speed_x *= -1
                self.speed_x += random.uniform(-0.2, 0.2)  # Add slight randomness
                self.happy = not self.happy  # Change expression when bouncing
                
            if self.y < self.size or self.y > 600 - self.size:
                self.speed_y *= -1
                self.speed_y += random.uniform(-0.2, 0.2)  # Add slight randomness
                self.happy = not self.happy  # Change expression when bouncing
                
            # Keep speed in reasonable bounds
            self.speed_x = max(-2, min(2, self.speed_x))
            self.speed_y = max(-2, min(2, self.speed_y))
            
            # Update rotation for star
            if self.shape_type == "star":
                self.rotation += 0.01
                
            return False

# Floating stars effect
class Star:
    def __init__(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(0, 600)
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.2, 1)
        self.alpha = random.randint(100, 255)
        self.alpha_change = random.choice([-1, 1]) * random.uniform(0.5, 2)

    def update(self):
        self.y -= self.speed
        self.alpha += self.alpha_change
        
        if self.alpha > 255 or self.alpha < 100:
            self.alpha_change *= -1
            
        if self.y < 0:
            self.y = 600
            self.x = random.randint(0, 800)
    
    def draw(self):
        # Fixed: Create a surface with correct alpha
        s = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        # Fixed: Ensure alpha value is within valid range (0-255)
        alpha = max(0, min(255, int(self.alpha)))
        pygame.draw.circle(s, (255, 255, 255, alpha), 
                         (self.size, self.size), self.size)
        screen.blit(s, (int(self.x - self.size), int(self.y - self.size)))

# Particle effects for popping
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 8)
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 5)
        self.speed_x = math.cos(angle) * speed
        self.speed_y = math.sin(angle) * speed
        self.life = random.randint(20, 40)
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += 0.1  # Gravity
        self.life -= 1
        self.size = max(0, self.size - 0.1)
        return self.life <= 0
    
    def draw(self):
        alpha = min(255, self.life * 10)
        s = pygame.Surface((int(self.size*2), int(self.size*2)), pygame.SRCALPHA)
        # Fixed: Use (r,g,b,a) format for color with alpha
        color = self.color + (int(alpha),)
        pygame.draw.circle(s, color, (int(self.size), int(self.size)), int(self.size))
        screen.blit(s, (int(self.x - self.size), int(self.y - self.size)))

# Setup game objects
shapes = [Shape() for _ in range(8)]  # Fewer shapes for less overwhelming
stars = [Star() for _ in range(50)]
particles = []
score = 0
font = pygame.font.Font(None, 48)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            for shape in shapes[:]:
                # Make hit detection more forgiving for young children
                distance = ((mx - shape.x) ** 2 + (my - shape.y) ** 2) ** 0.5
                if not shape.popping and distance < shape.size + 10:  # More forgiving hit detection
                    shape.popping = True
                    try:
                        pop_sound.play()  # Play pop sound
                    except:
                        pass  # Skip if sound cannot be played
                    
                    # Add particles for visual feedback
                    for _ in range(20):
                        particles.append(Particle(shape.x, shape.y, shape.color))
                    
                    score += 1
                    
                    # Play occasional laugh sound for positive reinforcement
                    if score % 5 == 0:
                        try:
                            laugh_sound.play()
                        except:
                            pass

    # Draw background
    draw_background()
    
    # Update and draw stars
    for star in stars:
        star.update()
        star.draw()
    
    # Update and draw shapes
    for shape in shapes[:]:
        if shape.update():  # If True, shape has finished popping
            shapes.remove(shape)
            shapes.append(Shape())  # Add a new shape
        shape.draw()
    
    # Update and draw particles
    for particle in particles[:]:
        if particle.update():
            particles.remove(particle)
        else:
            particle.draw()
    
    # Display score in a child-friendly way
    score_text = font.render("Pop: " + str(score), True, (50, 50, 200))
    screen.blit(score_text, (20, 20))
    
    # Add visual counter (stars) for young children who can't read numbers yet
    for i in range(min(10, score % 10)):
        pygame.draw.polygon(screen, (255, 255, 0), [
            (30 + i*25, 80),  # Top
            (35 + i*25, 90),  # Right
            (30 + i*25, 100), # Bottom
            (25 + i*25, 90)   # Left
        ])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()