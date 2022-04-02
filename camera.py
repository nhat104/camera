from cgitb import text
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import tkinter.messagebox

class MyVideoCapture:
    def __init__(self, video_source):
        self.vid = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source",video_source)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            frame = cv2.resize(frame, (640, 480))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if ret:
                return (ret, frame)
            else:
                return (ret, None)

class App:
    def __init__(self, window, window_title, video_source = 0, fpsLimit = 10):
        # Class parameters
        self.path = './Image/'
        self.window = window
        self.delay = 1
        self.iteration = 0
        self.card_code = ""
        self.vid = MyVideoCapture(video_source)
        self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.var = tkinter.StringVar()
        self.text = tkinter.Entry(self.window, width = 25, textvariable=self.var, font = ('Calibri', 18))
        self.old_value = ''
        self.video_source = video_source
        self.fpsLimit = fpsLimit
        self.time_limit = 10

        # Configure window
        self.text.pack()
        self.canvas.pack()
        self.window.title(window_title)
        self.text.configure(state='disabled')
        self.reset_binding()
        self.update()
        self.current_frame = None
        self.var.trace('w', self.check)

        self.window.mainloop()

    def get_input(self, event):
        # Neu khong phai number thi iterater ve 0
        if event.char == '\r':
            if self.iteration == 10:
                self.get_image()
                self.iteration = 0
                print(self.card_code)
                self.window.unbind('<Key>')
                self.text.configure(state='normal')
                self.text.focus()
        if event.char < '0' or event.char > '9':
            self.iteration = 0
        else:
            self.iteration += 1
            self.card_code += event.char
            

    def check(self, *args):
        if self.var.get() == '':
            self.var.set('')
        elif self.var.get().isdigit(): 
            # the current value is only digits; allow this
            self.old_value = self.var.get()
        else:
            # there's non-digit characters in the input; reject this 
            self.var.set(self.old_value)

    def get_image(self):
        ret, frame = self.vid.vid.read()
        self.current_frame = frame
        cv2.imwrite(self.path + self.card_code + '.jpg', frame)

    def image_text(self, student_code):
        cv2.putText(img = self.current_frame, text = student_code, org = (50, 50), fontFace = cv2.FONT_HERSHEY_SIMPLEX, 
                    color = (255, 0, 0), fontScale = 1, thickness = 2, lineType = cv2.LINE_AA)
        cv2.imwrite(self.path + self.card_code + '_' + student_code + '.jpg', self.current_frame)


    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
        self.window.after(self.delay, self.update)

    def get_text(self, e):
        self.iteration = 0
        user_input = self.text.get()
        self.image_text(user_input)
        self.var.set('')
        self.text.configure(state='disabled')
        self.reset_binding()
        self.card_code = ""

    def reset_binding(self):
        self.text.bind('<Return>', func = self.get_text)
        self.window.bind('<Key>', self.get_input)
        
        
App(tkinter.Tk(), "Thay Tien dep trai", 0, 10)
