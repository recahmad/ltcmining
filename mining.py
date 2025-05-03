import tkinter as tk
from tkinter import messagebox
import subprocess
import threading

class MiningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Litecoin Mining App")
        
        # Create labels and input fields
        self.wallet_label = tk.Label(root, text="Enter Litecoin Wallet Address:")
        self.wallet_label.pack(pady=10)
        
        self.wallet_entry = tk.Entry(root, width=30)
        self.wallet_entry.pack(pady=10)
        
        # Mining status label
        self.status_label = tk.Label(root, text="Mining Status: Not Started", fg="red")
        self.status_label.pack(pady=10)
        
        # Buttons to start/stop mining
        self.start_button = tk.Button(root, text="Start Mining", command=self.start_mining)
        self.start_button.pack(pady=5)
        
        self.stop_button = tk.Button(root, text="Stop Mining", command=self.stop_mining, state=tk.DISABLED)
        self.stop_button.pack(pady=5)
        
        # Initialize mining process variable
        self.mining_process = None

    def start_mining(self):
        wallet_address = self.wallet_entry.get()
        
        if not wallet_address:
            messagebox.showerror("Error", "Please enter a wallet address.")
            return
        
        # Update UI and start mining
        self.status_label.config(text="Mining Status: Running", fg="green")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # Run mining in a separate thread
        threading.Thread(target=self.run_mining, args=(wallet_address,), daemon=True).start()

    def run_mining(self, wallet_address):
        # Command to start mining with CGMiner (assuming it's in the system PATH)
        cmd = f"cgminer -o stratum+tcp://your-mining-pool-url -u {wallet_address} -p x -S scrypt"
        
        # Start the mining process
        self.mining_process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for process to finish (if ever) or handle live output
        for line in self.mining_process.stdout:
            print(line.decode("utf-8").strip())

    def stop_mining(self):
        if self.mining_process:
            self.mining_process.terminate()
            self.status_label.config(text="Mining Status: Stopped", fg="red")
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

# Create the root window and start the app
if __name__ == "__main__":
    root = tk.Tk()
    app = MiningApp(root)
    root.mainloop()
