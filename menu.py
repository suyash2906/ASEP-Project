def show_menu():
    """
    Display menu and get user choice.
    """
    print("\n" + "="*50)
    print("AI Multimodal Communication System")
    print("="*50)
    print("1. Text-to-Speech (TTS)")
    print("2. Speech-to-Text (STT)")
    print("3. Text-to-Sign Language")
    print("4. Speech-to-Sign")
    print("5. Camera Hand Detection")
    print("0. Exit")
    print("-"*50)
    
    choice = input("Select option (0-5): ").strip()
    return choice

if __name__ == "__main__":
    choice = show_menu()
    print(f"You selected: {choice}")

