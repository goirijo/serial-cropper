import PIL
from PIL import Image, ImageTk
import tkinter as tk
import numpy as np




class QuickCropper(tk.Frame):
    def flip_crop_region(self,event):
        self.crop_was_flipped=(not self.crop_was_flipped)

    def draw_crop_region(self,event):
        x,y=event.x,event.y
        self.canvas.delete(self.current_rectangle)

        x_off=(self.max_side_length)/2
        y_off=(x_off/self.crop_ratio)/2

        if self.crop_was_flipped:
            x_off,y_off=y_off,x_off

        self.current_rectangle=self.canvas.create_rectangle(x-x_off,y-y_off,x+x_off,y+y_off, fill="gray",stipple="gray50")
        #print("{}, {}".format(x,y))
        return
    
    @staticmethod
    def resize_image(final_width,image, window_width):
        width,height=image.size
        ratio=width/height

        return image.resize((window_width,int(window_width/ratio)), Image.LANCZOS)

    def _start_canvas(self):
        self.canvas=tk.Canvas(width=self.max_side_length,height=self.max_side_length)
        resized_image=self.resize_image(self.max_side_length,self.pil_image,self.max_side_length)

        self.canvas.pack()

        self.tk_image=ImageTk.PhotoImage(resized_image)
        self.canvas.create_image((0,0),image=self.tk_image,anchor=tk.NW)

    def __init__(self, parent, path, crop_ratio, max_side_length=1000, *args, **kwargs):
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.parent=parent
        self.path=path
        self.crop_ratio=crop_ratio
        self.max_side_length=max_side_length

        self.parent.resizable(False,False)
        self.parent.bind("<Motion>", self.draw_crop_region)
        self.parent.bind("<space>", self.flip_crop_region)
        self.crop_was_flipped=False;

        self.pil_image=Image.open(path)
        w,h=self.pil_image.size
        self.is_landscape=(w>h)
        self.starting_ratio=w/h


        self._start_canvas()
        #garbage rectangle so we have something to delete
        self.current_rectangle=self.canvas.create_rectangle(0,0,0,0)



def main():
    path="./media/test2.jpg"

    root=tk.Tk()
    root.title('Click to crop')

    QuickCropper(root,path,4/6)
    root.mainloop()

if __name__=="__main__":
    main()
