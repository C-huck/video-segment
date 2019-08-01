# video-segment
Short heuristic to automatically find and clip gestures in unsegmented video

## example

1. Example video can be found at [https://drive.google.com/file/d/1wa17L57tkPbL85-JANaD_gWN78GlCg4r/view?usp=sharing]. (920MB).
2. Every gesture successfully clipped from provided sample ('np.mp4'). See provided reference ('np_start_times.py') for list of anticipated gestures.
3. However, script over produces: Transitional movements and some self-grooming actions additionally clipped. 

## limitations

1. Less effective at identifying gestures from participants who move a lot.
2. Parameters should be tweaked s.t. minimum peak spacing is reduced.
