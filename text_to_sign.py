"""Text-to-Sign Language module.

This module provides functionality to convert text to sign language by displaying
images sequentially using pygame.
"""

import os
import time
from typing import Dict

import pygame

# Sign language mapping (A-Z). Images should be in sign_images/ folder named A.jpg, B.jpg, etc.
SIGN_MAPPING: Dict[str, str] = {
    "A": "A.jpg",
    "B": "B.jpg",
    "C": "C.jpg",
    "D": "D.jpg",
    "E": "E.jpg",
    "F": "F.jpg",
    "G": "G.jpg",
    "H": "H.jpg",
    "I": "I.jpg",
    "J": "J.jpg",
    "K": "K.jpg",
    "L": "L.jpg",
    "M": "M.jpg",
    "N": "N.jpg",
    "O": "O.jpg",
    "P": "P.jpg",
    "Q": "Q.jpg",
    "R": "R.jpg",
    "S": "S.jpg",
    "T": "T.jpg",
    "U": "U.jpg",
    "V": "V.jpg",
    "W": "W.jpg",
    "X": "X.jpg",
    "Y": "Y.jpg",
    "Z": "Z.jpg",
    " ": "space.jpg",  # Space gesture
}


def _load_available_images(image_dir: str) -> Dict[str, str]:
    """Auto-scan available images in the sign_images directory.

    Args:
        image_dir (str): Path to the directory containing sign images.

    Returns:
        Dict[str, str]: Mapping of letters to available image filenames.
    """
    available_letters = {}
    if os.path.exists(image_dir):
        try:
            for filename in os.listdir(image_dir):
                if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                    letter = filename[0].upper() if len(filename) > 1 else ""
                    available_letters[letter] = filename
        except OSError as e:
            print(f"Error reading sign_images directory: {e}")
    return available_letters


def text_to_sign(text: str, display_duration: float = 1.5) -> None:
    """Convert text to sign language by displaying images sequentially.

    Assumes uppercase letters. Images must exist in sign_images/.

    Args:
        text (str): The text to convert to sign language.
        display_duration (float): Duration to display each sign in seconds. Defaults to 1.5.

    Returns:
        None

    Example:
        >>> text_to_sign("HELLO")
    """
    image_dir = "sign_images"
    if not os.path.exists(image_dir):
        print("sign_images folder not found. Create it with A.jpg to Z.jpg files.")
        return

    # Load available images
    available_images = _load_available_images(image_dir)
    sign_mapping = {**SIGN_MAPPING, **available_images}

    pygame.init()
    screen = pygame.display.set_mode((400, 500))
    pygame.display.set_caption("Sign Language")
    clock = pygame.time.Clock()

    text = text.upper()
    running = True

    char_index = 0
    display_start_time = time.time()

    try:
        while running and char_index < len(text):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Clear screen
            screen.fill((255, 255, 255))

            char = text[char_index]
            if char in sign_mapping:
                img_path = os.path.join(image_dir, sign_mapping[char])
                if os.path.exists(img_path):
                    try:
                        img_surface = pygame.image.load(img_path)
                        img_surface = pygame.transform.scale(img_surface, (350, 400))
                        screen.blit(img_surface, (25, 50))
                    except pygame.error as e:
                        font = pygame.font.Font(None, 36)
                        text_surf = font.render(f"Error loading {char}: {str(e)[:20]}", True, (255, 0, 0))
                        screen.blit(text_surf, (25, 250))
                else:
                    font = pygame.font.Font(None, 36)
                    text_surf = font.render(f"Missing {img_path}", True, (0, 0, 0))
                    screen.blit(text_surf, (25, 250))
            else:
                font = pygame.font.Font(None, 36)
                text_surf = font.render(f"No mapping for {char}", True, (0, 0, 0))
                screen.blit(text_surf, (25, 250))

            # Show status
            font = pygame.font.Font(None, 24)
            status = font.render(f"Text: {text} | Current: {char} ({char_index + 1}/{len(text)})", True, (0, 0, 0))
            screen.blit(status, (10, 10))

            pygame.display.flip()
            clock.tick(30)

            # Check if display duration has elapsed
            if time.time() - display_start_time >= display_duration:
                char_index += 1
                display_start_time = time.time()
    finally:
        pygame.quit()
        print("Sign language display completed.")


if __name__ == "__main__":
    text_to_sign("HELLO")
