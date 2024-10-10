def frame(text, char):
    max_len = max(len(word) for word in text)
    
    border = char * (max_len + 4)
    
    result = [border]
    for word in text:
        result.append(f"{char} {word.ljust(max_len)} {char}")
    result.append(border)
    
    return "\n".join(result)

print(frame(['Create', 'a', 'frame'], '+'))
