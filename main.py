# main.py

import os
import logging
from scripts.unfollower_manager import unfollow_script
from scripts.follower_manager import follow_specific_user, search_most_followed_in_following
from scripts.github_utils import unstar_all_repositories

def setup_logging():
    """
    Sets up logging for main.py.
    Logs are stored in the 'logs' directory with the filename 'main.log'.
    """
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logger = logging.getLogger('main')
    logger.setLevel(logging.INFO)

    # Prevent adding multiple handlers if already set
    if not logger.handlers:
        fh = logging.FileHandler(os.path.join(log_directory, 'main.log'), mode='w')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        logger.propagate = False

    return logger

def clear_screen():
    """
    Clears the terminal screen for a cleaner interface.
    Works for both Windows (cls) and Unix-based systems (clear).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_main_menu():
    """
    Prints the main menu with better formatting and appeal.
    """
    print("\n" + "=" * 50)
    print(" " * 15 + "GITHUB BOT MENU")
    print("=" * 50)
    print("Welcome to your GitHub automation tool!")
    print("Please select one of the options below:")
    print("=" * 50)
    print("1. 🧹 Run Unfollow Script (Unfollow users who don't follow you back)")
    print("2. 👥 Run Follow Script")
    print("3. ⭐ Delete All Starred Repositories")
    print("4. 🔍 Search Most Followed Users in Your Following")
    print("5. ❌ Exit")
    print("=" * 50)

def print_follow_menu():
    """
    Prints the follow sub-menu with better formatting and appeal.
    """
    print("\n" + "=" * 50)
    print(" " * 18 + "FOLLOW MENU")
    print("=" * 50)
    print("Please choose an option:")
    print("1. 👤 Follow users from a specific GitHub account (with starring)")
    print("2. 🔄 Follow users from a specific GitHub account (without starring)")
    print("3. ❌ Return to the main menu")
    print("=" * 50)

def follow_menu(logger):
    """
    Sub-menu for the follow script with a cleaner layout.
    """
    while True:
        clear_screen()  # Clear the screen before displaying the follow menu
        print_follow_menu()
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == '1':
            clear_screen()  # Clear screen before starting specific user follow with starring
            logger.info("User selected to follow users from a specific GitHub account with starring.")
            follow_specific_user(should_star=True)
            logger.info("Completed following users from a specific GitHub account with starring.")
            input("Press Enter to return to the Follow Menu...")
        elif choice == '2':
            clear_screen()  # Clear screen before starting specific user follow without starring
            logger.info("User selected to follow users from a specific GitHub account without starring.")
            follow_specific_user(should_star=False)
            logger.info("Completed following users from a specific GitHub account without starring.")
            input("Press Enter to return to the Follow Menu...")
        elif choice == '3':
            logger.info("User chose to return to the main menu from the follow menu.")
            break
        else:
            print("❌ Invalid choice. Please select a valid option (1/2/3).")
            logger.warning(f"User entered invalid choice in follow menu: {choice}")
            input("Press Enter to continue...")  # Wait for user input before refreshing the screen

def main_menu(logger):
    """
    Main menu to select between unfollowing, following, deleting stars, searching, or exiting.
    """
    while True:
        clear_screen()  # Clear the screen before displaying the main menu
        print_main_menu()
        choice = input("Enter your choice (1/2/3/4/5): ").strip()
        logger.info(f"User selected main menu option: {choice}")

        if choice == '1':
            clear_screen()  # Clear screen before starting the unfollow script
            logger.info("User selected to run the Unfollow Script.")
            unfollow_script()
            logger.info("Completed running the Unfollow Script.")
            input("Press Enter to return to the main menu...")
        elif choice == '2':
            logger.info("User selected to run the Follow Script.")
            follow_menu(logger)
        elif choice == '3':
            clear_screen()  # Clear screen before deleting all starred repositories
            logger.info("User selected to delete all starred repositories.")
            confirm = input("Are you sure you want to delete (unstar) all your starred repositories? (y/n): ").strip().lower()
            logger.info(f"User confirmation for deleting starred repositories: {confirm}")
            if confirm == 'y':
                unstar_count = unstar_all_repositories()
                logger.info(f"Total repositories unstarred: {unstar_count}")
                print(f"Total repositories unstarred: {unstar_count}")
                input("Press Enter to return to the main menu...")
            else:
                print("Operation canceled.")
                logger.info("User canceled the deletion of starred repositories.")
                input("Press Enter to return to the main menu...")
        elif choice == '4':
            clear_screen()  # Clear screen before searching for most followed users
            logger.info("User selected to search for the most followed users in their following.")
            search_most_followed_in_following()
            logger.info("Completed searching for the most followed users in following.")
            input("Press Enter to return to the main menu...")
        elif choice == '5':
            clear_screen()  # Clear screen before exiting
            logger.info("User selected to exit the program.")
            print("Exiting the program. Goodbye! 👋")
            break
        else:
            print("❌ Invalid choice. Please select a valid option (1/2/3/4/5).")
            logger.warning(f"User entered invalid choice in main menu: {choice}")
            input("Press Enter to continue...")  # Wait for user input before refreshing the screen

if __name__ == "__main__":
    logger = setup_logging()
    logger.info("GitHub Bot started.")
    try:
        main_menu(logger)
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")
    finally:
        logger.info("GitHub Bot terminated.")
