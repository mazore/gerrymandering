from root import Root

"""
TODO:
- don't use 'default' in adjuster types just get from Parameters
- instead of typing 'none' into entry, have a checkbox to the left
- add buttons for control of left/middle/right click events
- have different system for 'invalid' parameters (red outline, empty StringVar)
- add district counters for each party
- add 'precincts' or 'neighborhoods' that represent a certain number of people that vote different ways but are swapped
  as one person
- add incrementer parameter adjuster type
- visualization of districts separate from canvas (for better understanding)
- redo code structure diagram & add more for ui package
- improve favor_tie (allow a not tied district to flip to tie if a tied district flips to not tied)
- implement get_district2_weight in District class
- better performance by different drawing method (not tkinter.Canvas), maybe website (flask)
- line smoothing (spline, make districts look more organic)
- multiple parties? make red and blue into other non american colors?
"""

if __name__ == '__main__':
    Root()
