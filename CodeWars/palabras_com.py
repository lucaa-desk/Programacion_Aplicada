def is_comfortable_word(word):
    left_hand = set("qwertasdfgzxcvb")
    right_hand = set("yuiophjklnm")
    
    use_left_hand = word[0] in left_hand
    
    for char in word[1:]:
        if use_left_hand and char in left_hand:
            return False
        if not use_left_hand and char in right_hand:
            return False
        use_left_hand = not use_left_hand
    
    return True
