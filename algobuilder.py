import json

    ## Version number

version = '0.0.1'

    ## Functions

def build_dict():

    ## Create potential values

    point_values = [i for i in range(2, 22)]
    dealer_values = [i for i in range(2, 12)]
    new_dict = {}

    ## Combine values in a tuple, then dictionary

    for key in range(len(point_values)):
        for value in range(len(dealer_values)):
            new_key = (point_values[key], dealer_values[value])
            new_dict.update({new_key: ''})
        
    return(new_dict)

params = build_dict()
print(params)
