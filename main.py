from root import Root

"""
TODO:
- shade districts with different intensities based on margins
- visualize how good the program is at different grid_widths and district_sizes
- add entry and tick-box parameter adjuster types and the rest of the adjusters
- add parameters and control of starting and stopping swaps
- visualization of districts separate from canvas (for better understanding)
- redo code structure diagram
- improve favor_tie (allow a not tied district to flip to tie if a tied district flips to not tied)
- implement get_district2_weight in District class
- better performance by different drawing method (not tkinter.Canvas), maybe website (flask)
- line smoothing (spline, make districts look more organic)
- multiple parties? make red and blue into other non american colors?
"""

if __name__ == '__main__':
    Root()
