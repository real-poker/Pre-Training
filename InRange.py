# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 05:12:31 2020

@author: Jeffrey McClure
"""

def InRange(hand, handrange):
    
    if hand[1] == hand[3]:
        hand = hand[0] + hand[2] + "s"
    else:
        hand = hand[0] + hand[2]
        
    splitrange = handrange.split(",")

    for freq in splitrange:
        if freq[0] + freq[1] == hand[0] + hand[1]:
            if len(freq) < 3:
                return True
            else:
                if len(hand) > 2 and freq[2] == "s":
                    return True
                elif len(hand) == 2 and freq[2] == "o":
                    return True
                elif freq[2] == ":":
                    return True
                
    return False