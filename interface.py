from tkinter import *
import customtkinter

root = customtkinter.CTk()
root.geometry('300x400')

def update_value(value):
    value_label.configure(text=f"Tempo: {int(value)}")

slider = customtkinter.CTkSlider(root, from_=0, to=100, number_of_steps=100, command=update_value)
slider.place(relx=0.5, rely=0.2, anchor=CENTER)

value_label = customtkinter.CTkLabel(root, text="Tempo: 50", fg_color="transparent")
value_label.place(relx=0.5, rely=0.3, anchor=CENTER)

frame = customtkinter.CTkFrame(master=root, width=10, height=100)
frame.place(relx=0.5, rely=0.6, anchor=CENTER)

myButton = customtkinter.CTkButton(root, text='Play', font=("Inter", 14))
myButton.place(relx=0.5, rely=0.9, anchor=CENTER)

root.mainloop()