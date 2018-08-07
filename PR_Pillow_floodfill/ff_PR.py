import time
from PIL import Image
import sys
import os


def _color_diff(rgb1, rgb2):
    """
    Uses 1-norm distance to calculate difference between two rgb values.
    """
    return abs(rgb1[0]-rgb2[0]) + abs(rgb1[1]-rgb2[1]) + abs(rgb1[2]-rgb2[2])


def floodfill(image, xy, value, border=None, thresh=0):
    """
        (experimental) Fills a bounded region with a given color.

        :param image: Target image.
        :param xy: Seed position (a 2-item coordinate tuple). See
            :ref:`coordinate-system`.
        :param value: Fill color.
        :param border: Optional border value.  If given, the region consists of
            pixels with a color different from the border color.  If not given,
            the region consists of pixels having the same color as the seed
            pixel.
        :param thresh: Optional threshold value which specifies a maximum
            tolerable difference of a pixel value from the 'background' in
            order for it to be replaced. Useful for filling regions of non-
            homogeneous, but similar, colors.
        """
    # based on an implementation by Eric S. Raymond
    # amended by yo1995 at 180806
    pixel = image.load()
    x, y = xy
    try:
        background = pixel[x, y]
        if _color_diff(value, background) <= thresh:
            return  # seed point already has fill color
        pixel[x, y] = value
    except (ValueError, IndexError):
        return  # seed point outside image
    edge = {(x, y)}
    full_edge = set()  # use a set to record each unique pixel processed
    if border is None:
        while edge:
            new_edge = set()
            for (x, y) in edge:  # 4 adjacent method
                for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                    if (s, t) in full_edge:
                        continue  # if already processed, skip
                    try:
                        p = pixel[s, t]
                    except IndexError:
                        pass
                    else:
                        if _color_diff(p, background) <= thresh:
                            pixel[s, t] = value
                            new_edge.add((s, t))
                            full_edge.add((s, t))
            full_edge = edge  # do not record useless pixels to reduce memory consumption
            edge = new_edge
    else:
        while edge:
            new_edge = set()
            for (x, y) in edge:
                for (s, t) in ((x+1, y), (x-1, y), (x, y+1), (x, y-1)):
                    if (s, t) in full_edge:
                        continue
                    try:
                        p = pixel[s, t]
                    except IndexError:
                        pass
                    else:
                        if p != value and p != border:
                            pixel[s, t] = value
                            new_edge.add((s, t))
                            full_edge.add((s, t))
            full_edge = edge
            edge = new_edge


def test_floodfill_border(self):
    # floodfill() is experimental

    # Arrange
    im = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(im)
    draw.rectangle(BBOX2, outline="yellow", fill="green")
    centre_point = (int(W/2), int(H/2))

    # Act
    ImageDraw.floodfill(
        im, centre_point, ImageColor.getrgb("red"),
        border=ImageColor.getrgb("black"))

    # Assert
    self.assert_image_equal(
        im, Image.open("Tests/images/imagedraw_floodfill2.png"))


if __name__ == '__main__':
    test_floodfill_border()
