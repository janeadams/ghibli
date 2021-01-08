import cv2
import numpy as np
import progressbar
from skimage import io
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import multiprocessing
import os
from os import walk
from shutil import copyfile
import csv


def get_files(path):
    files = []
    for (dirpath, dirnames, filenames) in walk(path):
        files.extend(filenames)
        break
    str_files = [f for f in files]
    return str_files

def get_hsv(RGBarray):
    rgb2float = interp1d([0,255],[0,1])
    hue2degree = interp1d([0,1],[0,360])
    float2pct = interp1d([0,1],[0,100])
    hsv = mcolors.rgb_to_hsv(rgb2float(RGBarray))
    converted = [float(hue2degree(hsv[0])), float(float2pct(hsv[1])), float(float2pct(hsv[2]))]
    return list(converted)

def viz_colors(palette, img, counts):
    average = img.mean(axis=0).mean(axis=0)
    avg_patch = np.ones(shape=img.shape, dtype=np.uint8)*np.uint8(average)
    indices = np.argsort(counts)[::-1]   
    freqs = np.cumsum(np.hstack([[0], counts[indices]/float(counts.sum())]))
    rows = np.int_(img.shape[0]*freqs)

    dom_patch = np.zeros(shape=img.shape, dtype=np.uint8)
    for i in range(len(rows) - 1):
        dom_patch[rows[i]:rows[i + 1], :, :] += np.uint8(palette[indices[i]])

    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(12,6))
    ax0.imshow(avg_patch)
    ax0.set_title('Average color')
    ax0.axis('off')
    ax1.imshow(dom_patch)
    ax1.set_title('Dominant colors')
    ax1.axis('off')
    plt.show(fig)

def get_colors(file, film, viz=False, output=True):
    try:
        img = io.imread(f'frames/{film}.mkv/{file}')
        pixels = np.float32(img.reshape(-1, 3))
        n_colors = 5
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
        flags = cv2.KMEANS_RANDOM_CENTERS

        _, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
        _, counts = np.unique(labels, return_counts=True)
        dominant = palette[np.argmax(counts)]
        secondary = palette[np.argmax(counts)-1]
        dominantHSV = get_hsv(dominant)
        secondaryHSV = get_hsv(secondary)
        
        isgreen = False
        iswarm = False
        isblue = False

        for color in [dominantHSV]:
            if (70 < color[0] < 160) and (color[1] > 20) and (color[2] > 40):
                if viz:print(f'Green trigger: {color}')
                isgreen = True

            if ((color[0] < 65) or (color[0] > 330)) and (color[1] > 20) and (color[2] > 40):
                if viz:print(f'Warm trigger: {color}')
                iswarm = True

            if (170 < color[0] < 250) and (color[1] > 20) and (color[2] > 40):
                if viz:print(f'Blue trigger: {color}')
                isblue = True

        if isgreen:
            if viz:
                io.imshow(img)
                plt.show()
                plt.clf()
                viz_colors(palette, img, counts)
                print(file)
            if output: copyfile(f'frames/{film}.mkv/{file}', f'color_frames/green/{file}')

        if isblue:
            if viz:
                io.imshow(img)
                plt.show()
                plt.clf()
                viz_colors(palette, img, counts)
                print(file)
            if output: copyfile(f'frames/{film}.mkv/{file}', f'color_frames/blue/{file}')
                
        if iswarm:
            if viz:
                io.imshow(img)
                plt.show()
                plt.clf()
                viz_colors(palette, img, counts)
                print(file)
            #if output: copyfile(f'frames/{film}.mkv/{file}', f'color_frames/warm/{file}')

        if output:
            tosave = [film,file,isgreen,iswarm,isblue]
            i=0
            for color in palette:
                tosave.append(get_hsv(color))

            with open(f'framecolors.csv', 'a') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(tosave)
    except:
        print(f'Error processing {film} {file}')


def process_frames(film, viz=False, output=True):
    files = get_files(f'frames/{film}.mkv/')
    for file in progressbar.progressbar(files, redirect_stdout=True):
        get_colors(file, film, viz, output)




