from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os

# tkinter initialization
application = Tk()

# globals
file_path = os.path.abspath(os.getcwd())
image_on_canvas: Label
resized_tk_img: PhotoImage
text_input: Entry
image_canvas: Frame
info_label: Label
image_canvas_width: int
image_canvas_height: int


def initialize(app):
    global text_input, image_canvas, info_label, image_canvas_height, image_canvas_width
    app.title("Super Mega Hiding Text In Images And Reading It From Images Application")
    screen_width, screen_height = 580, 460
    app.geometry("{}x{}".format(screen_width, screen_height))
    app.resizable(False, False)

    # tkinter - input
    text_input = Entry(app, width=screen_width)
    text_input.pack(pady=15, padx=15)

    # tkinter - info label
    info_label = Label(app, text="Choose an image to get started", pady=15)
    info_label.pack()

    # tkinter - image canvas
    image_canvas = Frame(app, width=300, height=300, bg='#D3D3D3')
    image_canvas.pack()
    image_canvas_height, image_canvas_width = (300, 300)
    image_canvas.place(anchor='center', relx=0.5, y=250, height=image_canvas_height, width=image_canvas_width)

    # tkinter - select button
    select_button = Button(app, text="Select an image", padx=10, pady=10, width=10, command=select_image)
    select_button.place(x=15, y=100)

    # tkinter - save button
    save_button = Button(app, text="Save hidden text", padx=10, pady=10, width=10, command=save_image)
    save_button.place(x=15, y=150)

    # tkinter - exit button
    quit_button = Button(app, text="Exit Application", command=app.quit)
    quit_button.pack(side=BOTTOM, pady=20)


def resize_to_fit_canvas(image_height: int, image_width: int, canvas_height: int, canvas_width: int) -> (int, int):
    ratio_height = image_height / canvas_height
    ratio_width = image_width / canvas_width

    if ratio_width > ratio_height:
        new_height = round(image_height / ratio_width)
        new_width = canvas_width
    else:
        new_height = canvas_height
        new_width = round(image_width / ratio_height)
    return new_height, new_width


def center_on_canvas(canvas_size: int, image_size: int) -> int:
    return round((canvas_size - image_size) / 2)


def clear_previous_image_selection() -> None:
    text_input.delete(0, 'end')
    if 'image_on_canvas' in globals():
        image_on_canvas.destroy()


def open_file_selection() -> None:
    try:
        global file_path
        open_directory = file_path
        file_path = filedialog.askopenfilename(initialdir=open_directory, title="pick",
                                               filetypes=(("All files", "*.*"), ("JPG files", "*.jpg")))
        info_label.config(text=file_path, fg="#000")
    except Exception as exception:
        print("Something went wrong,", exception)


def read_hidden_text_from_image() -> str:
    with open(file_path, 'rb') as f:
        try:
            content = f.read()
            offset = content.index(bytes.fromhex('FFD9')) + 2
            f.seek(offset)
            return str(f.read())[2:-1]
        except Exception as exception:
            print("Something went wrong while reading hidden text from image,", exception)


def select_image():
    global resized_tk_img, image_on_canvas, info_label
    clear_previous_image_selection()

    open_file_selection()

    try:
        # Open image
        opened_image = Image.open(file_path)
        original_tk_image = ImageTk.PhotoImage(opened_image)

        # Resize image to canvas
        resized_image_height, resized_image_width = resize_to_fit_canvas(original_tk_image.height(),
                                                                         original_tk_image.width(),
                                                                         image_canvas_height,
                                                                         image_canvas_width)

        resized_tk_img = ImageTk.PhotoImage(
            Image.open(file_path).resize((resized_image_width, resized_image_height)))
        image_on_canvas = Label(image_canvas, image=resized_tk_img, bg='#D3D3D3')
        if resized_image_height == 300:
            image_on_canvas.place(x=center_on_canvas(300, resized_image_width), y=0)
        elif resized_image_width == 300:
            image_on_canvas.place(x=0, y=center_on_canvas(300, resized_image_height))
        else:
            image_on_canvas.pack()

        # Read hidden text from image
        text_input.insert(0, read_hidden_text_from_image())

    except Exception as exception:
        print("File selected is not an image,", exception)
        info_label.config(text="Please select a valid image", fg="#D2042D")


def save_image():
    try:
        with open(file_path, 'rb') as in_f:
            content = in_f.read()
            offset = content.index(bytes.fromhex('FFD9')) + 2
            with open(file_path, 'wb') as out_f:
                out_f.write(content[:offset])
        with open(file_path, 'ab') as f:
            f.write(b"%b" % text_input.get().encode())
        info_label.config(text="Image hidden message updated successfully", fg="#228B22")
    except Exception as error:
        print("No file selected,", error)
        # no file selected
        info_label.config(text="Please select an image first", fg='#D2042D')


initialize(application)
# start application
application.mainloop()
