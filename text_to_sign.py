import os
import time
from PIL import Image
import pygame

# Sign language mapping (A-Z). Images should be in sign_images/ folder named A.jpg, B.jpg, etc.
SIGN_MAPPING = {
    'A': 'A.jpg', 'B': 'B.jpg', 'C': 'C.jpg', 'D': 'D.jpg', 'E': 'E.jpg',
    'F': 'F.jpg', 'G': 'G.jpg', 'H': 'H.jpg', 'I': 'I.jpg', 'J': 'J.jpg',
    'K': 'K.jpg', 'L': 'L.jpg', 'M': 'M.jpg', 'N': 'N.jpg', 'O': 'O.jpg',
    'P': 'P.jpg', 'Q': 'Q.jpg', 'R': 'R.jpg', 'S': 'S.jpg', 'T': 'T.jpg',
    'U': 'U.jpg', 'V': 'V.jpg', 'W': 'W.jpg', 'X': 'X.jpg', 'Y': 'Y.jpg', 'Z': 'Z.jpg',
    ' ': 'space.jpg'  # Space gesture
}

# Auto-scan available images (silent)
import os
image_dir = 'sign_images'
available_letters = {}
for filename in os.listdir(image_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        letter = filename[0].upper() if len(filename) > 1 else ''
        available_letters[letter] = filename

# Override mapping with found files
for letter, filename in available_letters.items():
    SIGN_MAPPING[letter] = filename

def text_to_sign(text):
    """
    Convert text to sign language by displaying images sequentially.
    Assumes uppercase letters. Images must exist in sign_images/.
    """
    image_dir = 'sign_images'
    if not os.path.exists(image_dir):
        print("sign_images folder not found. Create it with A.jpg to Z.jpg files.")
        return
    
    pygame.init()
    screen = pygame.display.set_mode((400, 500))
    pygame.display.set_caption("Sign Language")
    clock = pygame.time.Clock()
    
    text = text.upper()
    running = True
    
    char_index = 0
    start_time = time.time()
    
    while running and char_index < len(text):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Clear screen
        screen.fill((255, 255, 255))
        
        char = text[char_index]
        if char in SIGN_MAPPING:
            img_path = os.path.join(image_dir, SIGN_MAPPING[char])
            if os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    img = img.resize((350, 400), Image.Resampling.LANCZOS)
                    img_surface = pygame.image.load(img_path)
                    img_surface = pygame.transform.scale(img_surface, (350, 400))
                    screen.blit(img_surface, (25, 50))
                except:
                    font = pygame.font.Font(None, 36)
                    text_surf = font.render(f"No image: {char}", True, (0, 0, 0))
                    screen.blit(text_surf, (25, 250))
            else:
                font = pygame.font.Font(None, 36)
                text_surf = font.render(f"Missing {img_path}", True, (0, 0, 0))
                screen.blit(text_surf, (25, 250))
        else:
            font = pygame.font.Font(None, 36)
            text_surf = font.render(f"Unsupported: {char}", True, (0, 0, 0))
            screen.blit(text_surf, (25, 250))
        
        # Show current text and progress
        font = pygame.font.Font(None, 24)
        status = font.render(f"Text: {text} | Current: {char} ({char_index+1}/{len(text)})", True, (0, 0, 0))
        screen.blit(status, (25, 25))
        
        pygame.display.flip()
        clock.tick(1)  # Display each sign for 1 second
        
        # Auto advance after 1 second
        if time.time() - start_time > 1:
            char_index += 1
            start_time = time.time()
    
    pygame.time.wait(2000)
    pygame.quit()
    print("Sign language display completed.")

if __name__ == "__main__":
    text_to_sign("HELLO")

