from root import Root

"""
TODO:
- stats panel with changing districts per party, num swaps done, people per party,
- hide advanced parameter adjusters
- update code structure diagram with ui package
- have different system for 'invalid' parameters (red outline, empty StringVar)
- test for valid inputs that will break it (line_width = -1 is technically valid but will crash)
- district hover information
- release
- don't stall ui on sleep between draws
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
