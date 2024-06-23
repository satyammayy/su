import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MemoryAllocationSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Allocation Simulator")

        # Set up the main frame
        mainframe = ttk.Frame(self.root, padding="10")
        mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Initialize memory parameters
        self.memory_size = 100  # Total memory size
        self.memory_blocks = [("Free", self.memory_size)]  # List of tuples (Status, Size)

        # Set up the control panel
        self.control_panel = ttk.Frame(mainframe, padding="5")
        self.control_panel.grid(row=0, column=0, sticky=(tk.W, tk.E))

        self.setup_controls()

        # Set up the canvas for memory visualization
        self.canvas_frame = ttk.Frame(mainframe, padding="5")
        self.canvas_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.setup_canvas()

        # Set up status bar
        self.status = tk.StringVar()
        self.status_bar = ttk.Label(mainframe, textvariable=self.status, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=2, column=0, sticky=(tk.W, tk.E))
        self.update_status()

    def setup_controls(self):
        # Control elements for memory allocation
        self.size_label = ttk.Label(self.control_panel, text="Block Size:")
        self.size_label.grid(row=0, column=0, padx=5, pady=5)

        self.size_entry = ttk.Entry(self.control_panel)
        self.size_entry.grid(row=0, column=1, padx=5, pady=5)

        self.allocate_button = ttk.Button(self.control_panel, text="Allocate", command=self.allocate_memory)
        self.allocate_button.grid(row=0, column=2, padx=5, pady=5)

        self.deallocate_button = ttk.Button(self.control_panel, text="Deallocate", command=self.deallocate_memory)
        self.deallocate_button.grid(row=0, column=3, padx=5, pady=5)

        self.algorithm_label = ttk.Label(self.control_panel, text="Algorithm:")
        self.algorithm_label.grid(row=1, column=0, padx=5, pady=5)

        self.algorithm_var = tk.StringVar()
        self.algorithm_combobox = ttk.Combobox(self.control_panel, textvariable=self.algorithm_var)
        self.algorithm_combobox['values'] = ('First Fit', 'Best Fit', 'Worst Fit')
        self.algorithm_combobox.current(0)
        self.algorithm_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.reset_button = ttk.Button(self.control_panel, text="Reset", command=self.reset_memory)
        self.reset_button.grid(row=1, column=2, padx=5, pady=5)

    def setup_canvas(self):
        # Set up the Matplotlib figure and canvas
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.update_canvas()

    def allocate_memory(self):
        try:
            size = int(self.size_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Block size must be an integer.")
            return

        if size <= 0:
            messagebox.showerror("Invalid input", "Block size must be a positive integer.")
            return

        algorithm = self.algorithm_var.get()
        if algorithm == 'First Fit':
            self.first_fit_allocate(size)
        elif algorithm == 'Best Fit':
            self.best_fit_allocate(size)
        elif algorithm == 'Worst Fit':
            self.worst_fit_allocate(size)
        self.update_canvas()
        self.update_status()

    def first_fit_allocate(self, size):
        for index, (status, block_size) in enumerate(self.memory_blocks):
            if status == "Free" and block_size >= size:
                if block_size > size:
                    self.memory_blocks[index] = ("Allocated", size)
                    self.memory_blocks.insert(index + 1, ("Free", block_size - size))
                else:
                    self.memory_blocks[index] = ("Allocated", block_size)
                return
        messagebox.showerror("Allocation Failed", "No suitable block found for allocation.")

    def best_fit_allocate(self, size):
        best_index = -1
        best_size = float('inf')
        for index, (status, block_size) in enumerate(self.memory_blocks):
            if status == "Free" and block_size >= size and block_size < best_size:
                best_index = index
                best_size = block_size
        if best_index != -1:
            if best_size > size:
                self.memory_blocks[best_index] = ("Allocated", size)
                self.memory_blocks.insert(best_index + 1, ("Free", best_size - size))
            else:
                self.memory_blocks[best_index] = ("Allocated", best_size)
        else:
            messagebox.showerror("Allocation Failed", "No suitable block found for allocation.")

    def worst_fit_allocate(self, size):
        worst_index = -1
        worst_size = 0
        for index, (status, block_size) in enumerate(self.memory_blocks):
            if status == "Free" and block_size >= size and block_size > worst_size:
                worst_index = index
                worst_size = block_size
        if worst_index != -1:
            if worst_size > size:
                self.memory_blocks[worst_index] = ("Allocated", size)
                self.memory_blocks.insert(worst_index + 1, ("Free", worst_size - size))
            else:
                self.memory_blocks[worst_index] = ("Allocated", worst_size)
        else:
            messagebox.showerror("Allocation Failed", "No suitable block found for allocation.")

    def deallocate_memory(self):
        try:
            size = int(self.size_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Block size must be an integer.")
            return

        if size <= 0:
            messagebox.showerror("Invalid input", "Block size must be a positive integer.")
            return

        for index, (status, block_size) in enumerate(self.memory_blocks):
            if status == "Allocated" and block_size == size:
                self.memory_blocks[index] = ("Free", block_size)
                self.merge_free_blocks()
                self.update_canvas()
                self.update_status()
                return
        messagebox.showerror("Deallocation Failed", "No allocated block of the specified size found.")

    def merge_free_blocks(self):
        merged_blocks = []
        prev_status, prev_size = self.memory_blocks[0]
        for status, size in self.memory_blocks[1:]:
            if prev_status == "Free" and status == "Free":
                prev_size += size
            else:
                merged_blocks.append((prev_status, prev_size))
                prev_status, prev_size = status, size
        merged_blocks.append((prev_status, prev_size))
        self.memory_blocks = merged_blocks

    def reset_memory(self):
        self.memory_blocks = [("Free", self.memory_size)]
        self.update_canvas()
        self.update_status()

    def update_canvas(self):
        self.ax.clear()
        y_pos = 0
        for status, size in self.memory_blocks:
            color = 'green' if status == "Free" else 'red'
            self.ax.barh(y_pos, size, color=color, edgecolor='black')
            self.ax.text(size / 2, y_pos, f'{status} ({size})', va='center', ha='center', color='white')
            y_pos += 1
        self.ax.set_xlim(0, self.memory_size)
        self.ax.set_yticks([])
        self.ax.set_xticks(range(0, self.memory_size + 1, 10))
        self.ax.set_xlabel('Memory Size')
        self.ax.set_ylabel('Memory Blocks')
        self.canvas.draw()

    def update_status(self):
        total_allocated = sum(size for status, size in self.memory_blocks if status == "Allocated")
        total_free = self.memory_size - total_allocated
        self.status.set(f'Total Memory: {self.memory_size}, Allocated: {total_allocated}, Free: {total_free}')

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryAllocationSimulator(root)
    root.mainloop()
