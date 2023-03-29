from tkinter import *

# Create the main window
root = Tk()
root.title("Matrix Example")

# Create a frame to hold the matrix
frame = Frame(root, borderwidth=2, relief="ridge")
frame.pack(padx=10, pady=10)

# Create a 10x10 matrix of labels and pack them into the frame
for row in range(10):
    for col in range(10):
        label = Label(frame, text=f"{row},{col}", width=5, height=2, borderwidth=1, relief="solid")
        label.grid(row=row, column=col)

# Start the main event loop
root.mainloop()