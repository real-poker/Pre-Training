# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 19:04:09 2020
function that generates random Hold'em starting hand
"""

def DealHand():
    import random
    hands = {0: "2s",
             1: "3s",
             2: "4s",
             3: "5s",
             4: "6s",
             5: "7s",
             6: "8s",
             7: "9s",
             8: "Ts",
             9: "Js",
             10: "Qs",
             11: "Ks",
             12: "As",
             13: "2c",
             14: "3c",
             15: "4c",
             16: "5c",
             17: "6c",
             18: "7c",
             19: "8c",
             20: "9c",
             21: "Tc",
             22: "Jc",
             23: "Qc",
             24: "Kc",
             25: "Ac",
             26: "2h",
             27: "3h",
             28: "4h",
             29: "5h",
             30: "6h",
             31: "7h",
             32: "8h",
             33: "9h",
             34: "Th",
             35: "Jh",
             36: "Qh",
             37: "Kh",
             38: "Ah",
             39: "2d",
             40: "3d",
             41: "4d",
             42: "5d",
             43: "6d",
             44: "7d",
             45: "8d",
             46: "9d",
             47: "Td",
             48: "Jd",
             49: "Qd",
             50: "Kd",
             51: "Ad",
             }
    
    c1 = random.randint(0,51)
    c2 = c1
    while c1 == c2:
        c2 = random.randint(0,51)
    if c2 % 13 > c1 % 13:
        return hands[c2]+hands[c1]
    else:
        return hands[c1]+hands[c2]