import subprocess
import os
import shutil
import time
import threading
from app.config import config


def is_bun_installed():
    try:
        subprocess.run(["bun", "--version"], check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False


# Código ANSI para colores
BLUE = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
RESET = "\033[0m"

# Imprimir el logotipo con la cor verde


def print_logo():
    print(f"{BLUE}{config['cli']['logo']}{RESET}\n \n")


def print_step(message):
    print("    ╭────")
    print(f"{YELLOW}    ⚠ {message}{RESET}")
    print("    ╰────")


def print_success(message):
    print("    ╭────")
    print(f"{GREEN}    ✓ {message}{RESET}")
    print("    ╰────")


def print_error(message):
    print("    ╭────")
    print(f"{RED}    ❌ {message}{RESET}")
    print("    ╰────")


def loading_animation():
    chars = "/—\|"
    for char in chars:
        print(f"\r    Loading {char}", end="", flush=True)
        time.sleep(0.1)


def create_template(project_name: str, repo_url: str):
    try:

        print_logo()

        steps = [
            "🛠️ - Creating React Native project...",
            "📦 - Cloning the repository...",
            "📂 - Copying necessary files...",
            "🗑️ - Cleaning temporary files... ",
            "📦 - Installing dependencies... ",
        ]

        # Step 1: Create a new React Native project
        print_step(steps[0])
        loading_thread = threading.Thread(target=loading_animation)
        loading_thread.start()
        process = subprocess.Popen(
            ["npx", "--yes", "@react-native-community/cli", "init",
                project_name, "--skip-install", "--install-pods", "false"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate()
        loading_thread.join()
        print("\r    ", end="", flush=True)  # Clear the loading animation

        if process.returncode != 0:
            print_error(f"Error creating project: {stderr.decode()}")
            return

        os.chdir(project_name)
        print_success("Project created")

        # Step 2: Clone the repository into a temporary folder
        print_step(steps[1])
        loading_thread = threading.Thread(target=loading_animation)
        loading_thread.start()
        subprocess.run(["git", "clone", repo_url, "temp_repo"], check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        loading_thread.join()
        print("\r    ", end="", flush=True)  # Clear the loading animation
        if not os.path.exists("temp_repo"):
            raise FileNotFoundError("The repository was not cloned correctly.")
        print_success("Repository cloned")

        # Step 3: Copy files and folders from the repository, except 'android' and 'ios'
        print_step(steps[2])
        loading_thread = threading.Thread(target=loading_animation)
        loading_thread.start()
        for item in os.listdir("temp_repo"):
            if item not in ["android", "ios"]:
                source_path = os.path.join("temp_repo", item)
                destination_path = os.path.join(".", item)

                if os.path.exists(destination_path):
                    if os.path.isdir(destination_path):
                        shutil.rmtree(destination_path)
                    else:
                        os.remove(destination_path)

                if os.path.isdir(source_path):
                    shutil.copytree(source_path, destination_path)
                else:
                    shutil.copy(source_path, destination_path)
        loading_thread.join()
        print("\r    ", end="", flush=True)  # Clear the loading animation
        print_success("Files copied")

        # Step 4: Clean temporary files
        print_step(steps[3])
        loading_thread = threading.Thread(target=loading_animation)
        loading_thread.start()
        shutil.rmtree("temp_repo")
        git_folder = os.path.join(".", ".git")
        if os.path.exists(git_folder):
            shutil.rmtree(git_folder)
        loading_thread.join()
        print("\r    ", end="", flush=True)  # Clear the loading animation
        print_success("Temporary files cleaned")

        # Step 5: Install dependencies
        print_step(steps[4])
        loading_thread = threading.Thread(target=loading_animation)
        loading_thread.start()
        if is_bun_installed():
            subprocess.run(["bun", "install"], check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:
            subprocess.run(["npm", "install"], check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        loading_thread.join()
        print("\r    ", end="", flush=True)  # Clear the loading animation
        print_success("Dependencies installed")

        print_step("To start the project, run:")
        print(f"{GREEN}    cd {project_name} && npm start{RESET}")
        print("    ╰────")

    except Exception as e:
        print_error(f"An error occurred: {e}")
