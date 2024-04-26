import PIL
from PIL import Image, ImageTk
import tkinter as tk
import numpy as np




class QuickCropper(tk.Frame):

    def _flip_crop_region(self,event):
        self.crop_ratio=1/self.crop_ratio

    def _calculate_coords_for_landscape_crop_region(self, x, y):
        w,h=self.cvs_w,self.cvs_h

        dx=w
        dy=dx//self.crop_ratio
        x=dx/2
        
        max_h=w/self.crop_ratio
        y=max(y,max_h/2)
        y=min(h-max_h/2,y)

        coords=(x-dx/2,y-dy/2,x+dx/2,y+dy/2)
        return coords

    def _calculate_coords_for_portrait_crop_region(self, x, y):
        w,h=self.cvs_w,self.cvs_h

        dy=h
        dx=dy*self.crop_ratio
        y=dy/2
        
        max_w=h*self.crop_ratio
        x=max(x,max_w/2)
        x=min(w-max_w/2,x)

        coords=(x-dx/2,y-dy/2,x+dx/2,y+dy/2)
        return coords

    def _draw_top_crop(self,coords):
        self.canvas.delete(self.current_top_crop)
        self.current_top_crop=self.canvas.create_rectangle(0,0,self.cvs_w,coords[1], fill="gray",stipple="gray75")
        return

    def _draw_bottom_crop(self,coords):
        self.canvas.delete(self.current_bottom_crop)
        self.current_bottom_crop=self.canvas.create_rectangle(0,coords[3],self.cvs_w,self.cvs_h, fill="gray",stipple="gray75")
        return

    def _draw_left_crop(self,coords):
        self.canvas.delete(self.current_left_crop)
        self.current_left_crop=self.canvas.create_rectangle(0,0,coords[0],self.cvs_h, fill="gray",stipple="gray75")
        return

    def _draw_right_crop(self,coords):
        self.canvas.delete(self.current_right_crop)
        self.current_right_crop=self.canvas.create_rectangle(coords[2],0,self.cvs_w,self.cvs_h, fill="gray",stipple="gray75")
        return

    def _draw_crop_region(self,event):
        x,y=event.x,event.y
        self.canvas.delete(self.current_rectangle)

        if self.crop_ratio > 1:
            coords=self._calculate_coords_for_landscape_crop_region(x,y)

        else:
            coords=self._calculate_coords_for_portrait_crop_region(x,y)

        self._draw_top_crop(coords)
        self._draw_bottom_crop(coords)
        self._draw_left_crop(coords)
        self._draw_right_crop(coords)
        return

    def _assign_canvas_dimensions(self, win_size):
        w,h=self.img_w,self.img_h

        if w>h:
            self.cvs_w=win_size
            self.cvs_h=int(win_size/self.img_r)
        else:
            self.cvs_h=win_size
            self.cvs_w=int(self.img_r*win_size)
        return

    def _assign_long_short_axis(self):
        if self.crop_ratio < 1:
            self.long_ax=self.cvs_h
            self.short_ax=self.cvs_w
        else:
            self.long_ax=self.cvs_w
            self.short_ax=self.cvs_h
        return
    
    @staticmethod
    def resize_image(final_width,image, window_width):
        w,h=image.size
        ratio=w/h

        if w>h:
            return image.resize((window_width,int(window_width/ratio)), Image.LANCZOS)

        return image.resize((int(window_width*ratio),window_width), Image.LANCZOS)

    def _start_canvas(self):
        self.canvas=tk.Canvas(width=self.cvs_w,height=self.cvs_h)
        resized_image=self.img.resize((self.cvs_w,self.cvs_h), Image.LANCZOS)

        self.canvas.pack()

        self.tk_image=ImageTk.PhotoImage(resized_image)
        self.canvas.create_image((0,0),image=self.tk_image,anchor=tk.NW)

    def __init__(self, parent, path, crop_ratio, win_size=1000, *args, **kwargs):

        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.parent=parent
        self.path=path
        self.crop_ratio=crop_ratio

        self.parent.resizable(False,False)
        self.parent.bind("<Motion>", self._draw_crop_region)
        self.parent.bind("<space>", self._flip_crop_region)

        self.img=Image.open(path)
        self.img_w,self.img_h=self.img.size
        self.img_r=self.img_w/self.img_h

        self._assign_canvas_dimensions(win_size)
        self._assign_long_short_axis()
        self._start_canvas()

        #garbage rectangle so we have something to delete
        self.current_rectangle=self.canvas.create_rectangle(0,0,0,0)
        self.current_top_crop=self.canvas.create_rectangle(0,0,0,0)
        self.current_bottom_crop=self.canvas.create_rectangle(0,0,0,0)
        self.current_left_crop=self.canvas.create_rectangle(0,0,0,0)
        self.current_right_crop=self.canvas.create_rectangle(0,0,0,0)



def main():
    path="./media/test_landscape.jpg"
    path="./media/test_portrait.jpg"

    root=tk.Tk()
    root.title('Click to crop')

    QuickCropper(root,path,4/6)
    root.mainloop()

if __name__=="__main__":
    main()
