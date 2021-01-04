from root import Root

"""
TODO:
- add checkbox parameter adjuster type
- instead of typing 'none' into entry, have a checkbox to the left
- add buttons for control of left/middle/right click events
- add district counters for each party
- add incrementer parameter adjuster type 
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
