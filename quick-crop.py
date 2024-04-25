import PIL
from PIL import Image, ImageTk
import tkinter as tk
import numpy as np




class QuickCropper(tk.Frame):
    def motion(self,event):
        x,y=event.x,event.y
        print("{}, {}".format(x,y))
        return

    @staticmethod
    def resize_image(final_width,image):
        width,height=image.size
        ratio=width/height

        window_width=1000
        return image.resize((window_width,int(window_width/ratio)), Image.LANCZOS)

    def _start_canvas(self):
        self.canvas=tk.Canvas(width=1000,height=1000)
        self.canvas.pack()

        img=ImageTk.PhotoImage(self.resize_image(1000,self.pil_image))
        self.canvas.create_image((0,0),image=img,anchor=tk.NW)

    def __init__(self, parent, path, *args, **kwargs):
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.parent=parent
        self.path=path

        self.parent.resizable(False,False)

        self.pil_image=Image.open(path)
        self.tk_image=ImageTk.PhotoImage(self.resize_image(1000,self.pil_image))

        self.canvas=tk.Canvas(width=1000,height=1000)
        self.canvas.pack()

        self.canvas.create_image((0,0),image=self.tk_image,anchor=tk.NW)
        self.canvas.create_rectangle(30,30,400,400, fill="gray",stipple="gray50")



def main():
    path="./media/test2.jpg"

    root=tk.Tk()
    root.title('Click to crop')

    QuickCropper(root,path)
    root.mainloop()

if __name__=="__main__":
    main()
