# video-segment
Short and simple heuristic to automatically find and clip gestures in unsegmented video.

Script identifies gross pixel-wide changes between frames. Changes that are two standard deviations from the mean identify potential gestures (usually the 'stroke' or high energey phase of the gesture). These peaks are centered within a user-defined window to try to include the beginning and end of the gestures.

## To use

Run the script from the command line with

```Python
./video-segment.py filename [--window-size N] [--spacing N]
```

`window-size`/2 indicates how many seconds before and after the peak to clip the video.

`spacing` indicates how far peaks must be from each other, in seconds (default = 4 seconds)

Clips are output according to the following formula: input_name + clip# .mp4

## example

1. Example video can be found at [https://drive.google.com/file/d/1wa17L57tkPbL85-JANaD_gWN78GlCg4r/view?usp=sharing]. (921MB).
2. Every gesture successfully clipped from provided sample ('np.MP4'). See provided reference ('np_start_times.py') for list of gestures and their  hand-coded approximate start times.
3. However, script over produces: Transitional movements and some self-grooming actions additionally clipped. 

## limitations

1. Less effective at identifying gestures from participants who move a lot.
2. Parameters should be tweaked s.t. minimum peak spacing is reduced.
