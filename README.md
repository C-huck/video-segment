# video-segment
Short heuristic to automatically find and clip gestures in unsegmented video

## example

Example video can be found at []. (920MB).
Every gesture successfully clipped from provided sample ('np.mp4'). See provided reference ('np_start_times.py') for list of anticipated gestures.
However, script over produces: Transitional movements and some self-grooming actions additionally clipped. 

## limitations

Less effective at identifying gestures from participants who move a lot.
Parameters should be tweaked s.t. minimum peak spacing is reduced.
