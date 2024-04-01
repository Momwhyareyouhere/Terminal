import tkinter as tk
import subprocess
import string
import random
import os

class TerminalApp:
    def __init__(self, master):
        self.master = master
        master.title("GUI Terminal")

        self.output_text = tk.Text(master, wrap=tk.WORD, height=20, width=60)
        self.output_text.pack()

        self.input_entry = tk.Entry(master, width=60)
        self.input_entry.pack()
        self.input_entry.bind("<Return>", self.execute_command)

    def execute_command(self, event):
        command = self.input_entry.get()
        self.input_entry.delete(0, tk.END)

        # Check if the command is "password generator"
        if command.lower() == "password generator":
            self.generate_password()
            return
        
        # Check if the command is "snake_game"
        if command.lower() == "snake_game":
            self.install_and_run_snake_game()
            return

        # Execute other commands and capture output
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")

        # Display output and error in the GUI
        if output:
            self.output_text.insert(tk.END, output)
        if error:
            self.output_text.insert(tk.END, error)

        # Ensure the text widget scrolls to show the latest output
        self.output_text.see(tk.END)

    def generate_password(self):
        password_length = 12
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=password_length))
        
        # Save password to a file
        with open("passwords.txt", "a") as f:
            f.write(password + "\n")
        
        self.output_text.insert(tk.END, f"Generated password: {password}\n")
        self.output_text.insert(tk.END, "Password saved to passwords.txt\n")
        self.output_text.see(tk.END)

    def check_package_installed(self, package_name):
        process = subprocess.Popen(["dpkg", "-s", package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        output, error = process.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")

        if "Status: install ok installed" in output:
            return True
        else:
            return False

    def install_and_run_snake_game(self):
        required_packages = ["python3-tk", "libncurses5-dev", "libncursesw5-dev"]

        for package in required_packages:
            if not self.check_package_installed(package):
                self.output_text.insert(tk.END, f"Installing {package}...\n")
                process = subprocess.Popen(["sudo", "apt-get", "install", "-y", package], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
                output, error = process.communicate()
                error = error.decode("utf-8")
                if error:
                    self.output_text.insert(tk.END, error)
                    return
                else:
                    self.output_text.insert(tk.END, f"{package} installed successfully.\n")
            else:
                self.output_text.insert(tk.END, f"{package} is already installed.\n")

        self.output_text.insert(tk.END, "Cloning Snake Game repository...\n")
        process = subprocess.Popen(["git", "clone", "https://github.com/Momwhyareyouhere/Snake-Game-for-Console.git"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        output, error = process.communicate()
        error = error.decode("utf-8")
        if error:
            self.output_text.insert(tk.END, error)
            return
        else:
            self.output_text.insert(tk.END, "Snake Game repository cloned successfully.\n")

        self.output_text.insert(tk.END, "Running Snake Game...\n")
        os.chdir("Snake-Game-for-Console")
        process = subprocess.Popen(["python", "snake_game.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        output, error = process.communicate()
        if error:
            self.output_text.insert(tk.END, error.decode("utf-8"))
        else:
            self.output_text.insert(tk.END, output.decode("utf-8"))

def main():
    root = tk.Tk()
    app = TerminalApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
