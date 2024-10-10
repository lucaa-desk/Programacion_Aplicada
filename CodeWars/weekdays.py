import calendar

def most_frequent_days(year):
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    first_day, total_days = calendar.yearrange(year)
    
    most_frequent = []
    
    if total_days == 365:
        most_frequent.append(days_of_week[first_day])
    else:
        most_frequent.append(days_of_week[first_day])
        most_frequent.append(days_of_week[(first_day + 1) % 7])
    
    return most_frequent

print(most_frequent_days(2427))  # Salida: ['Friday']
print(most_frequent_days(2185))  # Salida: ['Saturday']
print(most_frequent_days(2860))  # Salida: ['Thursday', 'Friday']
