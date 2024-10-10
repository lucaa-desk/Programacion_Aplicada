def find_longest_word_length(s):
    words = s.split()  
    longest = max(words, key=len)  
    return len(longest)  
