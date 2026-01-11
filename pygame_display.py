import pygame
import random
import csv

def find_dimensions(dataset_name, sample_name):
    print("Récupération des dimensions de la vidéo")
    with open("data/train.csv", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if row["lab_id"]==dataset_name and row["video_id"]==sample_name :
                return row["video_width_pix"], row["video_height_pix"]

    print ("Les dimensions n'ont pas été trouvées, 1280 x 720 appliqué")
    return 1280, 720  

def display(data, dataset_name, sample_name) :
    action_colors = {
    "None":(0,0,0),
    "rear": (128, 0, 128),        # violet
    "avoid": (0, 128, 255),       # bleu clair
    "attack": (255, 0, 0),        # rouge
    "approach": (0, 200, 0),      # vert
    "chase": (255, 165, 0),       # orange
    "submit": (100, 100, 100),    # gris
    "chaseattack": (0, 0, 0)      # noir
    }
    
    pygame.init()
    width, height = find_dimensions(dataset_name, sample_name)

    screen = pygame.display.set_mode((720, 480), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    surface = pygame.Surface((int(width), int(height)))

    running = True
    for key in sorted(data.keys()) :
        frame = data[key]
        if not running :
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        surface.fill((255, 255, 255))  # fond blanc
        clock.tick(25)
        for agent_id in frame.values() :
            color = (0, 0, 0)
            if agent_id["action"] is not None :
                color = action_colors[agent_id["action"]]
            pygame.draw.circle(surface, color, (int(agent_id['x']), int(agent_id['y'])), 20)

        font = pygame.font.SysFont(None, 60)
        y = 0
        for ckey,cvalue in action_colors.items():
            text = font.render(ckey, True, cvalue)
            surface.blit(text, (10, 10 + y))
            y += 35
        text = font.render(str(key), True, (0,0,0))
        surface.blit(text, (10, 10 + y))


        # adaptation écran
        scaled = pygame.transform.smoothscale(surface, screen.get_size())
        screen.blit(scaled, (0, 0))

        pygame.display.flip()
        clock.tick(25)  # fps

    pygame.quit()
    
