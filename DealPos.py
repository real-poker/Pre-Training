# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 03:34:04 2020

@author: Jeffrey McClure
"""

def DealPos():
    import random    
    while True:
        p1 = random.randint(0,5)
        p2 = random.randint(0,5)
        p3 = random.randint(0,3)
    
        if p3 == 0 or p3 == 2:
            if p1 == 5:
                p1 = random.randint(0,4)
            if p3 == 2:
                while p2 <= p1:
                    p1 = random.randint(0,4)
                    p2 = random.randint(1,5)
                    
        if p3 == 1 or p3 == 3:
            if p1 == 0:
                p1 = random.randint(1,5)
            while p1 <= p2:
                p2 = random.randint(0,4)
        
        if p1 != p2:
            break
            
    positions = {0: "EP",
                 1: "MP",
                 2: "CO",
                 3: "BN",
                 4: "SB",
                 5: "BB",
                 }
    
    tree = {0: "Open",
            1: "Facing Open",
            2: "Facing 3Bet",
            3: "Facing 4Bet",
            }
    
    return (p3, positions[p1], positions[p2], tree[p3])