import PIL
from PIL import Image, ImageTk
import tkinter as tk
import numpy as np
import os
import argparse


class QuickCropper(tk.Frame):

    def _on_x_press(self, event):
        self.parent.destroy()

    def _on_key_press(self, event):
        key = event.char

        if key == 'x':
            self._on_x_press(event)
        elif key.isdigit():
            self.grid_num = int(key)
        else:
            print("Unrecognized key '{}'".format(key))

        x, y = event.x, event.y
        return

    def _on_mouse_move(self, event):
        x, y = event.x, event.y
        self._draw_bbox(x, y)
        self._shade_outside_bbox(x, y)
        return

    def _on_space_press(self, event):
        x, y = event.x, event.y
        self._flip_bbox()
        self._draw_bbox(x, y)
        self._shade_outside_bbox(x,y)
        return

    def _get_cropped_pathname(self):
        directory, filename = os.path.split(self.path)
        base_name, extension = os.path.splitext(filename)

        return os.path.join(
            directory,
            "sc-r{}-{}".format(self.str_ratio, base_name) + extension)

    def _crop(self, x, y):
        w, h = self.img_w, self.img_h
        r = self.crop_ratio
        _, coords = self._calculate_crop_region_coords(x, y, w, h)

        print("coords:{}".format(coords))
        cimg = self.img.crop(coords)
        return cimg

    def _commit(self, event):
        x, y = event.x, event.y

        #x and y are canvas positions, not true image positions
        x = x * self.img_w / self.cvs_w
        y = y * self.img_w / self.cvs_w

        new_file = self._get_cropped_pathname()
        cimg = self._crop(x, y)
        cimg.save(new_file)
        print("Cropped! Saved to {}".format(new_file))
        self.parent.destroy()
        return

    def _flip_crop_region(self):
        self.crop_ratio = 1 / self.crop_ratio
        return

    def _calculate_coords_for_landscape_crop_region(self, x, y, w, h, r):
        dx = w
        dy = dx // r
        x = dx / 2

        max_h = w / r
        y = max(y, max_h / 2)
        y = min(h - max_h / 2, y)

        coords = (x - dx / 2, y - dy / 2, x + dx / 2, y + dy / 2)
        return coords

    def _calculate_coords_for_portrait_crop_region(self, x, y, w, h, r):
        dy = h
        dx = dy * r
        y = dy / 2

        max_w = h * r
        x = max(x, max_w / 2)
        x = min(w - max_w / 2, x)

        coords = np.array((x - dx / 2, y - dy / 2, x + dx / 2, y + dy / 2))
        return coords

    def _calculate_crop_region_coords(self, x, y, w, h):
        cvsr = self.cvs_w / self.cvs_h
        r = self.crop_ratio

        portrait_crop = cvsr < r
        if portrait_crop:
            coords = self._calculate_coords_for_landscape_crop_region(
                x, y, w, h, r)
        else:
            coords = self._calculate_coords_for_portrait_crop_region(
                x, y, w, h, r)

        return portrait_crop, coords


    def _shade_outside_bbox(self, x, y):
        for s in self.draw_shade:
            self.canvas.delete(s)

        bbox = self._calculate_bbox(x, y)

        self.draw_shade[0] = self.canvas.create_rectangle(0,
                                                          0,
                                                          self.cvs_w,
                                                          bbox[1],
                                                          outline='',
                                                          fill="gray",
                                                          stipple="gray75")
        self.draw_shade[1] = self.canvas.create_rectangle(0,
                                                          0,
                                                          bbox[0],
                                                          self.cvs_h,
                                                          outline='',
                                                          fill="gray",
                                                          stipple="gray75")
        self.draw_shade[2] = self.canvas.create_rectangle(bbox[2],
                                                          0,
                                                          self.cvs_w,
                                                          self.cvs_h,
                                                          outline='',
                                                          fill="gray",
                                                          stipple="gray75")
        self.draw_shade[3] = self.canvas.create_rectangle(0,
                                                          bbox[3],
                                                          self.cvs_w,
                                                          self.cvs_h,
                                                          outline='',
                                                          fill="gray",
                                                          stipple="gray75")

    def _draw_grid(self, coords):
        n = self.grid_num
        for l in self.current_grid:
            self.canvas.delete(l)

        self.current_grid = []

        x0, y0, x1, y1 = coords
        x = np.linspace(x0, x1, n + 1)
        y = np.linspace(y0, y1, n + 1)

        for i in range(n + 1):
            self.current_grid.append(self.canvas.create_line(
                x[i], y0, x[i], y1))
            self.current_grid.append(self.canvas.create_line(
                x0, y[i], x1, y[i]))
        return

    def _calculate_bbox(self, x, y):
        xy = np.array([x, y])
        wh = np.array(self.bbox_span)*self.zoom

        #Prevent bbox from exiting the canvas
        xy_min = 0.5 * wh
        xy_max = np.array([self.cvs_w, self.cvs_h]) - 0.5 * wh
        xy = np.maximum(xy, xy_min)
        xy = np.minimum(xy, xy_max)

        #upper left (north west)
        nw = xy - 0.5 * wh
        #lower right (south east)
        se = xy + 0.5 * wh

        return (*nw, *se)

    def _flip_bbox(self):
        if self.bbox_span is self.possible_spans[0]:
            self.bbox_span=self.possible_spans[1]
        else:
            self.bbox_span=self.possible_spans[0]

    def _draw_bbox(self, x, y):
        self.canvas.delete(self.bbox_rectangle)
        self.bbox_rectangle = self.canvas.create_rectangle(
            *self._calculate_bbox(x, y))

    def _assign_canvas_dimensions(self, win_size):
        w, h = self.img_w, self.img_h

        if w > h:
            self.cvs_w = win_size
            self.cvs_h = int(win_size / self.img_r)
        else:
            self.cvs_h = win_size
            self.cvs_w = int(self.img_r * win_size)
        return

    def _start_canvas(self):
        self.canvas = tk.Canvas(width=self.cvs_w, height=self.cvs_h)
        resized_image = self.img.resize((self.cvs_w, self.cvs_h), Image.LANCZOS)

        self.canvas.pack()

        self.tk_image = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image((0, 0), image=self.tk_image, anchor=tk.NW)
        return

    @staticmethod
    def _parse_ratio(crop_ratio):
        w, h = crop_ratio.split('x')
        return int(w) / int(h)

    def _rectify_ratio(self):
        if self.crop_ratio < 1 and self.img_r < 1:
            return
        self.crop_ratio=1/self.crop_ratio

    def _assign_possible_spans(self):
        span1=[self.cvs_w, self.cvs_w*self.crop_ratio]
        span2=[self.cvs_w, self.cvs_w/self.crop_ratio]
        span3=[self.cvs_h*self.crop_ratio,self.cvs_h]
        span4=[self.cvs_h/self.crop_ratio,self.cvs_h]

        good_spans=[span for span in [span1,span2,span3,span4] if span[0]*span[1] <= self.cvs_w*self.cvs_h]
        sorted_spans = sorted(good_spans, key=lambda v: sum(x*x for x in v), reverse=True)

        self.possible_spans=sorted_spans

    def _span_large(self):
        self.bbox_span=self.possible_spans[0]

    def _span_small(self):
        self.bbox_span=self.possible_spans[1]

    def __init__(self,
                 parent,
                 path,
                 crop_ratio,
                 win_size=1000,
                 *args,
                 **kwargs):

        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.path = path
        self.str_ratio = crop_ratio
        self.crop_ratio = self._parse_ratio(crop_ratio)
        self.zoom=1.0

        self.parent.resizable(False, False)
        self.parent.bind("<Motion>", self._on_mouse_move)
        self.parent.bind("<space>", self._on_space_press)
        self.parent.bind("<Button-1>", self._commit)
        self.parent.bind("<Key>", self._on_key_press)

        self.img = Image.open(path)
        self.img_w, self.img_h = self.img.size
        self.img_r = self.img_w / self.img_h

        self._assign_canvas_dimensions(win_size)
        self._rectify_ratio()
        self._start_canvas()

        self.possible_spans=[]
        self._assign_possible_spans()
        self.bbox_span = [0,0]
        self._span_large()

        #garbage rectangles so we have something to delete
        #self.current_crop=[self.canvas.create_rectangle(0,0,0,0),self.canvas.create_rectangle(0,0,0,0)]
        self.draw_shade = [self.canvas.create_rectangle(0, 0, 0, 0)] * 4
        self.bbox_rectangle = self.canvas.create_rectangle(0, 0, 0, 0)

        self.grid_num = 1
        self.current_grid = []
        #self._draw_crop_region(*self.parent.winfo_pointerxy())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-j",
                        "--jpgs",
                        nargs='+',
                        required=True,
                        help="List of pictures you want to crop")
    parser.add_argument("-r",
                        "--crop-ratio",
                        required=True,
                        help="Proportion in which to crop as wxh, e.g. 4x6")

    args = parser.parse_args()

    image_files = args.jpgs

    for f in image_files:
        root = tk.Tk()
        root.title('Click to crop')

        QuickCropper(root, f, args.crop_ratio)
        root.mainloop()


if __name__ == "__main__":
    main()
