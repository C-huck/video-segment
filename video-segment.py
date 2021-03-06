import cv2
from scipy import signal
import numpy as np
import subprocess
import argparse

"""
NB: script requires installation of ffmpeg, but can be modified to use opencv
"""

def hist(img):
	"""
	Returns a histogram analysis of a single image (in this case, a video frame)
	"""
	return cv2.calcHist([img],[0],None,[256],[0,256])

def read_frames(video):
    """
    Reads a video file and returns a list of the histogram data for each frame
    """
    v = cv2.VideoCapture(video)
    fps=v.get(cv2.CAP_PROP_FPS)
    frames = []
    success,image = v.read()
    while success:
        success,image = v.read()
        if success:
            frames.append(hist(image))
    return frames,fps

def get_frame_difference(video):
    """
    Goes through the histograms of video frames pairwise and returns a list of 
	frame indices (x) and histogram differences (y)
    """
    frames,fps = read_frames(video)
    x = []
    y = []
    for n,f in enumerate(frames):
        if n!=len(frames)-1:
            x.append(n)
            y.append(1-(cv2.compareHist(hist(f),hist(frames[n+1]),cv2.HISTCMP_CORREL)))
    hist_dif = list(zip(x,y))
    return hist_dif,fps

def get_vid_stats(hist_dif):
    """
    Use heuristic: differences that are 2x magnitude of standard deviation are relevant
    """
    avg = np.mean([x[1] for x in hist_dif]) #get average between-hist difference
    std = np.std([x[1] for x in hist_dif])*2 #get 2x standard deviation of between-hist differences
    sig_peaks = [(x,y) if (y-std)>avg else (x,0) for (x,y) in hist_dif] #zero-out peaks that do not meet heuristic
    return sig_peaks

def peak_spacing(sig_peaks,fps,spacing=4):
    """
    cleaning up: Of significant peaks, return those that are at least X seconds apart (here 4). Tweak for subjects who move a lot
    """
    spaced_peaks = signal.find_peaks([y[1] for y in sig_peaks],distance=spacing*fps) #peaks in frames
    spaced_peaks = [x/fps for x in spaced_peaks[0]] #convert frames to seconds to avoid head-math in applying temporal window later
    return spaced_peaks
  
def video_cut(video,spaced_peaks,window=4):
    """
    cut video using ffmpeg: use list of significant peaks to identify where to clip videos. 
    Script assumes that relevant movement begins 2 seconds before peak and ends 2 seconds after peak. 
    """
    outName = video.split(".")[0]+'_'
    for i,y in enumerate(spaced_peaks):
        subprocess.call(['ffmpeg', '-y', '-ss', str(y-window/2), '-i', video, '-c', 'copy', '-t', str(window), outName+str(i)+'.mp4'])
        print("video cut")

def main():
	parser = argparse.ArgumentParser(description='Video segmenter')
	parser.add_argument('fileName',type=str,help='Name of the file you want to segment, including extension')
	parser.add_argument('--window',dest='window',type=int,help='How far before and after the peak to clip the video.')
	parser.add_argument('--spacing',dest='spacing',type=int,help='How far peaks must be from each other')

	args = parser.parse_args()
	if len(args.fileName.split(".")[1]) < 2:
		print("Please include extension")
	else:
		hist_dif,fps = get_frame_difference(fileName)
		sig_peaks = get_vid_stats(hist_dif)
		spaced_peaks = peak_spacing(sig_peaks,fps,spacing=args.spacing)
		video_cut(fileName,spaced_peaks,window=args.window)

if __name__ == "__main__":
    main()






