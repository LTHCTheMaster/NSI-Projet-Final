# -*- coding: utf-8 -*-

from math import sqrt
from PIL import Image as pimg

#GraphCore
class GraphCore:
    def __init__(self):
        pass

    def gap(self, pointa, pointb):
        """return the distance between two tridimensional vectors (currently the two colors we want to compare)"""
        return sqrt( (pointb[0] - pointa[0])**2 + (pointb[1] - pointa[1])**2 + (pointb[2] - pointa[2])**2 )

    def mdcl(self, image_path, color_list):
        """Return the color matrix of the image with only specified colors in color_list"""
        img = pimg.open(image_path)
        wd, hg = img.size
        out = []
        for i in range(hg):
            line = []
            for j in range(wd):
                colr, colg, colb = img.getpixel((j,i))
                line.append(color_list[self.closest((colr,colg,colb), color_list)])
            out.append(line)
        img.close()
        return out

    def closest(self, compared, comparing):
        """return the index of the closest tridimensional vector (currently a color) to compared (comparing is a list)"""
        closest = comparing[0]
        out = 0
        for c in range(len(comparing)):
            if self.gap(comparing[c], compared) < self.gap(closest, compared):
                closest = comparing[c]
                out = c
        return out

    def gmdcl(self, image_path):
        """return the grey scale image"""
        img = pimg.open(image_path)
        wd, hg = img.size
        out = []
        for i in range(hg):
            line = []
            for j in range(wd):
                colr, colg, colb = img.getpixel((j,i))
                g = int((colr+colg+colb)/3)
                line.append((g, g, g))
            out.append(line)
        img.close()
        return out

    def nmdcl(self, image_path):
        """Return the negative image"""
        img = pimg.open(image_path)
        wd, hg = img.size
        out = []
        for i in range(hg):
            line = []
            for j in range(wd):
                colr, colg, colb = img.getpixel((j,i))
                nr = 255 - colr
                ng = 255 - colg
                nb = 255 - colb
                line.append((nr, ng, nb))
            out.append(line)
        img.close()
        return out

    def cimdcl(self, image_path, mode='r'):
        """
        -> default mode: r (R) => ignore red so R in RGB = 0
        -> g (G) => ignore green so G in RGB = 0
        -> b (B) => ignore blue so B in RGB = 0
        -> k (K) => keep red so G & B in RGB = 0
        -> l (L) => keep green so R & B in RGB = 0
        -> m (M) => keep blue so R & G in RGB = 0
        -> => Warning : You cannot use uppercase letters for mode
        """
        img = pimg.open(image_path)
        wd, hg = img.size
        out = []
        for i in range(hg):
            line = []
            for j in range(wd):
                colr, colg, colb = img.getpixel((j,i))
                if mode == 'r':
                    line.append((0, colg, colb))
                elif mode == 'g':
                    line.append((colr, 0, colb))
                elif mode == 'b':
                    line.append((colr, colg, 0))
                elif mode == 'k':
                    line.append((colr, 0, 0))
                elif mode == 'l':
                    line.append((0, colg, 0))
                elif mode == 'm':
                    line.append((0, 0, colb))
                elif not mode in 'rgbklm':
                    line.append((colr, colg, colb))
            out.append(line)
        img.close()
        return out

    def mmdcl(self, image_path, mode='rg'):
        """
        -> default mode: rg (RG) => R & G in RGB equals the average of R & G
        -> rb (RB) => R & B in RGB equals the average of R & B
        -> gb (GB) => G & B in RGB equals the average of G & B
        -> => Warning : You cannot use uppercase letters for mode
        """
        img = pimg.open(image_path)
        wd, hg = img.size
        out = []

        for i in range(hg):
            line = []
            for j in range(wd):
                colr, colg, colb = img.getpixel((j,i))
                if mode == 'rg':
                    m = int((colr+colg)/2)
                    line.append((m, m, colb))
                elif mode == 'rb':
                    m = int((colr+colb)/2)
                    line.append((m, colg, m))
                elif mode == 'gb':
                    m = int((colg+colb)/2)
                    line.append((colr, m, m))
                elif mode not in ['rg','rb','gb']:
                    line.append((colr,colg,colb))
            out.append(line)
        img.close()
        return out

    def rsz(self, image_path, out_image_path, mode='w', width=256, height=256, scale=0.5):
        """
        Save a rescaled image
        Mode => -> w (W) => rescale by a new width
        -> h (H) => rescale by a new height
        -> wh (WH) => rescale by a new width and a new height
        -> s (S) => rescale by a ratio
        -> => Warning : You cannot use uppercase letters for mode
        """
        img = pimg.open(image_path)

        wd, hg = img.size

        if mode == 'w':
            ratio = width / wd
            nhg = int(hg * ratio)
            img = img.resize((width, nhg))
        elif mode == 'h':
            ratio = height / hg
            nwd = int(wd * ratio)
            img = img.resize((nwd, height))
        elif mode == 'wh':
            img = img.resize((width, height))
        elif mode == 's':
            nwd = int(wd * scale)
            nhg = int(hg * scale)
            img = img.resize((nwd, nhg))
        elif mode not in ['w', 'h', 'wh', 's']:
            return

        img.save(out_image_path,'JPEG')
        img.close()

    def smz(self, image_path, out_image_path, mode='h'):
        """
        Save a symetrized image created with the original image
        Mode => -> h (H) => do the horizontal symetry
        -> v (V) => do the vertical symetry
        -> => Warning : You cannot use uppercase letters for mode
        """
        img = pimg.open(image_path)

        wd, hg = img.size

        imgout = pimg.new('RGB', (wd, hg))

        if mode == 'h':
            for i in range(wd):
                for j in range(hg):
                    x = wd - i - 1
                    r, g, b = img.getpixel((i, j))
                    imgout.putpixel((x, j), (r, g, b))
        elif mode == 'v':
            for i in range(wd):
                for j in range(hg):
                    y = hg - j - 1
                    r, g, b = img.getpixel((i, j))
                    imgout.putpixel((i, y), (r, g, b))
        elif mode not in 'hv':
            return

        img.close()
        imgout.save(out_image_path,'JPEG')
        imgout.close()
    
    def trim(self, image_path, out_image_path, value=16, mode='t'):
        """
        Trim an image by removing value pixels on the mode part of image
        => mode -> t (T) = Top
        -> b (B) = Bottom
        -> l (L) = Left
        -> r (R) = Right
        -> => Warning : You cannot use uppercase letters for mode
        """
        img = pimg.open(image_path)

        wd, hg = img.size

        if mode == 't':
            if value < hg - 1:
                imgout = pimg('RGB', (wd, hg - value))

                for i in range(wd):
                    for j in range(value, hg):
                        colr, colg, colb = img.getpixel((i,j))
                        imgout.putpixel((i,j-value), (colr, colg, colb))
                
                img.close()
                imgout.save(out_image_path,'JPEG')
                imgout.close()
        elif mode == 'b':
            if value < hg - 1:
                imgout = pimg('RGB', (wd, hg - value))

                for i in range(wd):
                    for j in range(hg - value):
                        colr, colg, colb = img.getpixel((i,j))
                        imgout.putpixel((i,j), (colr, colg, colb))
                
                img.close()
                imgout.save(out_image_path,'JPEG')
                imgout.close()
        elif mode == 'l':
            if value < wd - 1:
                imgout = pimg('RGB', (wd - value, hg))

                for i in range(value, wd):
                    for j in range(hg):
                        colr, colg, colb = img.getpixel((i,j))
                        imgout.putpixel((i-value,j), (colr, colg, colb))
                
                img.close()
                imgout.save(out_image_path,'JPEG')
                imgout.close()
        elif mode == 'r':
            if value < wd - 1:
                imgout = pimg('RGB', (wd - value, hg))

                for i in range(wd - value):
                    for j in range(hg):
                        colr, colg, colb = img.getpixel((i,j))
                        imgout.putpixel((i,j), (colr, colg, colb))
                
                img.close()
                imgout.save(out_image_path,'JPEG')
                imgout.close()
        elif mode not in 'tblr':
            img.save(out_image_path)
            img.close()

#TransformSys
class TransformSys:
    def __init__(self):
        self.gphc = GraphCore()

    def transformImg_nms(self, image_path, out_image_path, mode='p', color_list=[(255,255,255),(0,0,0)]):
        """
        Transform an image to an other image with a specified mode
        => Mode list: -> p (P) => use a limited color system to transform the image
        -> g (G) => create the corresponding grey scale image
        -> n (N) => create the corresponding negative image
        -> ci_r (CI_R) => ignore red
        -> ci_g (CI_G) => ignore green
        -> ci_b (CI_B) => ignore blue
        -> k_r (K_R) => keep only red
        -> k_g (K_G) => keep only green
        -> k_b (K_B) => keep only blue
        -> m_rg (M_RG) => R & G in RGB equals the average of R & G
        -> m_rb (M_RB) => R & B in RGB equals the average of R & B
        -> m_gb (M_GB) => G & B in RGB equals the average of G & B
        -> => Warning : You cannot use uppercase letters for mode
        """
        if mode == 'p':
            colors = self.gphc.mdcl(image_path, color_list)
        elif mode == 'g':
            colors = self.gphc.gmdcl(image_path)
        elif mode == 'n':
            colors = self.gphc.nmdcl(image_path)
        elif mode == 'ci_r':
            colors = self.gphc.cimdcl(image_path, 'r')
        elif mode == 'ci_g':
            colors = self.gphc.cimdcl(image_path, 'g')
        elif mode == 'ci_b':
            colors = self.gphc.cimdcl(image_path, 'b')
        elif mode == 'k_r':
            colors = self.gphc.cimdcl(image_path, 'k')
        elif mode == 'k_g':
            colors = self.gphc.cimdcl(image_path, 'l')
        elif mode == 'k_b':
            colors = self.gphc.cimdcl(image_path, 'm')
        elif mode == 'm_rg':
            colors = self.gphc.mmdcl(image_path, 'rg')
        elif mode == 'm_rb':
            colors = self.gphc.mmdcl(image_path, 'rb')
        elif mode == 'm_gb':
            colors = self.gphc.mmdcl(image_path, 'gb')
        elif mode not in ['p', 'g', 'n', 'ci_r', 'ci_g', 'ci_b', 'k_r', 'k_g', 'k_b', 'm_rg', 'm_rb', 'm_gb']:
            return

        outimg = pimg.new(size=(len(colors[0]),len(colors)),mode='RGB')
        for i in range(len(colors[0])):
            for j in range(len(colors)):
                outimg.putpixel((i,j),colors[j][i])
        outimg.save(out_image_path,'JPEG')
        outimg.close()

    def transformImg_ms(self, image_path, out_image_path, mode='r_w', width=256, height=256, scale=0.5, value=16):
        """
        Transform an image to an other image with a specified mode
        => Mode list: -> r_w (R_W) => resize by width
        -> r_h (R_H) => resize by height
        -> r_wh (R_WH) => resize by width and height
        -> r_s (R_S) => resize by scale
        -> s_h (S_H) => create the horizontal symetry
        -> s_v (S_V) => create the vertical symetry
        -> t_t (T_T) => Trim an image by removing value pixels on the top part of image
        -> t_b (T_B) => Trim an image by removing value pixels on the bottom part of image
        -> t_l (T_L) => Trim an image by removing value pixels on the left part of image
        -> t_r (T_R) => Trim an image by removing value pixels on the right part of image
        -> => Warning : You cannot use uppercase letters for mode
        """
        if mode == 'r_w':
            self.gphc.rsz(image_path, out_image_path, 'w', width, height, scale)
        elif mode == 'r_h':
            self.gphc.rsz(image_path, out_image_path, 'h', width, height, scale)
        elif mode == 'r_wh':
            self.gphc.rsz(image_path, out_image_path, 'wh', width, height, scale)
        elif mode == 'r_s':
            self.gphc.rsz(image_path, out_image_path, 's', width, height, scale)
        elif mode == 's_h':
            self.gphc.smz(image_path, out_image_path, 'h')
        elif mode == 's_v':
            self.gphc.smz(image_path, out_image_path, 'v')
        elif mode == 't_t':
            self.gphc.trim(image_path, out_image_path, value, 't')
        elif mode == 't_b':
            self.gphc.trim(image_path, out_image_path, value, 'b')
        elif mode == 't_l':
            self.gphc.trim(image_path, out_image_path, value, 'l')
        elif mode == 't_r':
            self.gphc.trim(image_path, out_image_path, value, 'r')
        elif mode not in ['r_w','r_h','r_wh','r_s','s_h','s_v','t_t','t_b','t_l','t_r']:
            return

#Trasform Method
TRFSYS = TransformSys()
def transformImg(image_path, out_image_path, main_mode='c', sub_mode='p', color_list=[(255,255,255),(0,0,0)], width=256, height=256, scale=0.5, value=16):
    """
    Main Mode: -> c => color; -> s => shape/structure
    Sub Mode: 
    ==> c => -> p (P) => use a limited color system to transform the image
    -> g (G) => create the corresponding grey scale image
    -> n (N) => create the corresponding negative image
    -> ci_r (CI_R) => ignore red
    -> ci_g (CI_G) => ignore green
    -> ci_b (CI_B) => ignore blue
    -> k_r (K_R) => keep only red
    -> k_g (K_G) => keep only green
    -> k_b (K_B) => keep only blue
    -> m_rg (M_RG) => R & G in RGB equals the average of R & G
    -> m_rb (M_RB) => R & B in RGB equals the average of R & B
    -> m_gb (M_GB) => G & B in RGB equals the average of G & B
    ==> s => -> r_w (R_W) => resize by width
    -> r_h (R_H) => resize by height
    -> r_wh (R_WH) => resize by width and height
    -> r_s (R_S) => resize by scale
    -> s_h (S_H) => create the horizontal symetry
    -> s_v (S_V) => create the vertical symetry
    -> t_t (T_T) => Trim an image by removing value pixels on the top part of image
    -> t_b (T_B) => Trim an image by removing value pixels on the bottom part of image
    -> t_l (T_L) => Trim an image by removing value pixels on the left part of image
    -> t_r (T_R) => Trim an image by removing value pixels on the right part of image
    ==> Warning : You cannot use uppercase letters for mode
    """
    if main_mode == 'c':
        TRFSYS.transformImg_nms(image_path, out_image_path, sub_mode, color_list)
    elif main_mode == 's':
        TRFSYS.transformImg_ms(image_path, out_image_path, sub_mode, width, height, scale, value)
    elif main_mode not in 'cs':
        return
