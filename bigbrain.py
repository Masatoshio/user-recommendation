# -*- coding: utf-8 -*-
"""
Created on Wed May 26 22:35:19 2021

@author: adela
"""
import pandas as pd
import sys

#
# predicted rating function to take in parameters and list the top n predicted
# ratings for the locations given
#
#   Parameters:
#           group: group type member belongs to
#           loc_array: array of locations to predict rating of
#           amt: amount of results to return
#           choice_table: table of all ratings made by each group
#           weight_table: table to compare the similarity of each group (0-1)
#   Returns: 
#           toJson: Json formatted list of top n locations for that user
#
#
def predRating(group, loc_array, amt, choice_table, weight_table):
    
    # read file
    choices = pd.DataFrame(pd.read_csv(choice_table))
    weights = pd.DataFrame(pd.read_csv(weight_table))
    
    locations = loc_array
    
    # set weights of each group
    adv_weight = weights.iloc[0][group]
    sch_weight = weights.iloc[1][group]
    see_weight = weights.iloc[2][group]
    loc_weight = weights.iloc[3][group]
    tou_weight = weights.iloc[4][group]
    fod_weight = weights.iloc[5][group]
    
    # denominator of the prediction formula
    denominator = adv_weight + sch_weight + see_weight + loc_weight + tou_weight + fod_weight
    
    predicted_ratings = {}
    
    # for each location, find its score among each group, subtract the average
    # then multiply by weight to build numerator
    for location in locations:
        loc = location - 1
        rating = choices.iloc[loc][group + '_score']
        
        # calculate average for all groups
        loc_avg = (choices.iloc[loc]['adv_score'] + choices.iloc[loc]['sch_score'] + choices.iloc[loc]['see_score'] + \
                    choices.iloc[loc]['loc_score'] + choices.iloc[loc]['tou_score'] + choices.iloc[loc]['fod_score']) / 6

        adv_numerator = (choices.iloc[loc]['adv_score'] - loc_avg) * adv_weight
        sch_numerator = (choices.iloc[loc]['sch_score'] - loc_avg) * sch_weight
        see_numerator = (choices.iloc[loc]['see_score'] - loc_avg) * see_weight
        loc_numerator = (choices.iloc[loc]['loc_score'] - loc_avg) * loc_weight
        tou_numerator = (choices.iloc[loc]['tou_score'] - loc_avg) * tou_weight
        fod_numerator = (choices.iloc[loc]['fod_score'] - loc_avg) * fod_weight
        
        numerator = adv_numerator + sch_numerator + see_numerator + loc_numerator \
                    + tou_numerator + fod_numerator
                    
        pred_rating = rating + (numerator / denominator)
        
        predicted_ratings[location] = pred_rating
        
    
    # write dictionary to a series to be exported as a Json
    toSeries = pd.Series(predicted_ratings, name='predictedRating')
    toSeries = toSeries.nlargest(n=amt)
    toJson = toSeries.to_json(orient="table")
    
    return toJson


#
# main function to call predRating()
# can use system arguments or local files
#
def __main__():
    group = sys.argv[1]
    #location_array = sys.argv[2]
    amount = sys.argv[2]
    
    predRating(group, [1, 5, 10, 6, 2, 7, 9, 17], amount, 'test_choices.csv', 'weights.csv')


__main__()
