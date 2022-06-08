# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
from tkinter import ttk
from tkinter import *
import tkinter.filedialog as fc
import fitz as ft
import os
from checkBoxDetection import run_analysis


def select_file():
    filetypes = (
        ("PDF files", ".pdf"),
        ("All files", ".*")
    )
    filename = fc.askopenfilename(filetypes=filetypes)
    # pdf2png(filename)
    get_text(filename)
    file_name.set(filename)


def get_text(filename):
    return filename


def pdf_png(filename):
    print(filename)
    doc = ft.open(filename)  # array of png
    if not os.path.exists("F:/Text Images"):
        os.mkdir("F:/Text Images")
    for page in doc:
        pix = page.get_pixmap()
        pix.save(f"F:/Text Images/page-{page.number}.png")
        run_analysis(f"F:/Text Images/page-{page.number}.png")
        # row_counter=row_counter+2
        print('saved')
        # cv2.imread('image',doc)


if __name__ == '__main__':
    root = Tk()

    # Gets the requested values of the height and width.
    windowWidth = root.winfo_reqwidth()
    windowHeight = root.winfo_reqheight()
    # print("Width",windowWidth,"Height",windowHeight)

    # Gets both half the screen width/height and window width/height
    positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)
    positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)

    # Positions the window in the center of the page.
    root.geometry("+{}+{}".format(positionRight, positionDown))
    # start_row=0
    root.title("Check Box Analysis")
    file_name = StringVar()

    frm = ttk.Frame(root, padding=10)
    frm.pack()

    left_screen = ttk.Label(frm)
    left_screen.pack(side=LEFT)

    right_screen = ttk.Label(frm)
    right_screen.pack(side=RIGHT, anchor=N)

    right_top_screen = ttk.Label(right_screen)
    right_top_screen.pack(side=TOP)

    right_bottom_screen = ttk.Label(right_screen)
    right_bottom_screen.pack(side=TOP)

    bone_img = PhotoImage(file='F:/FYP/Paitient Form Analysis/bone.png')
    bone_img_lable = ttk.Label(left_screen, image=bone_img)
    bone_img_lable.pack(anchor=CENTER)

    Bahria_Uni_img = PhotoImage(file='F:/FYP/Paitient Form Analysis/Bahria_Uni.png')
    Bahria_Uni_img_lable = ttk.Label(right_top_screen, image=Bahria_Uni_img, anchor=N)
    Bahria_Uni_img_lable.pack(side=LEFT, anchor=N)

    chirologo_img = PhotoImage(file='F:/FYP/Paitient Form Analysis/chirologo.png')
    chirologo_img_lable = ttk.Label(right_top_screen, image=chirologo_img, anchor=N)
    chirologo_img_lable.pack(side=RIGHT, anchor=N)

    file_name_lable = ttk.Label(right_bottom_screen, text="File Name")
    file_name_lable.pack(side=TOP, anchor=CENTER)

    file_name_entry = ttk.Entry(right_bottom_screen, textvariable=file_name)
    file_name_entry.pack(side=TOP, anchor=CENTER)

    select_button = ttk.Button(right_bottom_screen, text="select", command=lambda: select_file())
    select_button.pack(side=TOP, anchor=W)

    convert_button = ttk.Button(right_bottom_screen, text="Convert", command=lambda: pdf_png(file_name.get()))
    convert_button.pack(side=TOP, anchor=E)

    # png_button = ttk.Buuton(right_bottom_screen, text = "PNG")
    # png_button.pack(side = LEFT,anchor = )
    root.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
