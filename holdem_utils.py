"""
# Function that generates random Hold'em starting hand.
"""

def deal_hand():
    import random
    
    suit_dict = {0: 's', 1:'c', 2:'h', 3:'d'}
    value_dict = {10:'T', 11:'J', 12:'Q', 13:'K', 14:'A'}
    
    def match_card(num):
        try:
            value = value_dict[num % 13 + 2]
        except KeyError:
            value = num % 13 + 2
        suit = suit_dict[num // 13]     
        return f'{value}{suit}'

    num1 = random.randint(0,51)
    while True:
        num2 = random.randint(0,51)
        if num1 != num2: break
    card1 = match_card(num1)
    card2 = match_card(num2)
    
    if num2 % 13 > num1 % 13:
        return f'{card2}{card1}'
    return f'{card1}{card2}'

"""
# Function that randomly selects both the positions and game-tree position of two players.
"""

def deal_pos():
    import random  
    
    positions_dict = {0: "EP", 1: "MP", 2: "CO", 3: "BN", 4: "SB", 5: "BB"}
    tree_dict = {0: "Open", 1: "Facing Open", 2: "Facing 3Bet", 3: "Facing 4Bet"}
    
    pos1 = random.randint(0,5)
    while True:
        pos2 = random.randint(0,5)
        if pos1 != pos2: break
    tree = random.randint(0,3)
    
    if tree in [0, 2]:
        if pos1 > pos2:
            return (tree, positions_dict[pos2], positions_dict[pos1], tree_dict[tree])
    else:
        if pos1 < pos2:
            return (tree, positions_dict[pos2], positions_dict[pos1], tree_dict[tree])
    return (tree, positions_dict[pos1], positions_dict[pos2], tree_dict[tree])

"""
# Function that determines whether a given hand is within a given hand range.
"""

def in_range(hand, handrange):
    
    if len(handrange) < 2:
        return False   
    
    if hand[1] == hand[3]:
        hand = f'{hand[0]}{hand[2]}s'
    else:
        hand = f'{hand[0]}{hand[2]}'
        
    hand_list = handrange.split(",")
    
    for entry in hand_list:  
        if entry.split(':')[0] == hand:
            return True
    return False