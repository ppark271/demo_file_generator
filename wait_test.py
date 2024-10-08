import tkinter as tk

root = tk.Tk()
root.geometry("400x300")  # Set window size

# Create frames
upper_left_frame = tk.Frame(root, bg="lightblue", width=200, height=150)
upper_right_frame = tk.Frame(root, bg="lightgreen", width=200, height=150)
bottom_frame = tk.Frame(root, bg="lightcoral", width=400, height=150)

# Use grid to position the frames
upper_left_frame.grid(row=0, column=0, sticky="nsew")
upper_right_frame.grid(row=0, column=1, sticky="nsew")
bottom_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

# Configure grid weights to expand
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)

root.mainloop()
