from root import Root

"""
TODO:
- update code structure diagram with ui package
- have different system for 'invalid' parameters (red outline, empty StringVar)
- test for valid inputs that will break it (line_width = -1 is technically valid but will crash)
- district hover information
- add more draw modes
- release
- pie charts for representation vs population
- experiment with trying to keep big districts more cohesive/clumped/less strung out
- don't stall ui on sleep between draws
- add 'precincts' or 'neighborhoods' that represent a certain number of people that vote different ways but are swapped
  as one person
- add incrementer parameter adjuster type
- improve favor_tie (allow a not tied district to flip to tie if a tied district flips to not tied)
- implement get_district2_weight in District class
- better performance by different drawing method (not tkinter.Canvas), maybe website (flask)
- custom people ratios and grids
- line smoothing (spline, make districts look more organic) 
- multiple parties? make red and blue into other non american colors?
"""

if __name__ == '__main__':
    Root()
