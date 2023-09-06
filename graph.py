from pandas_datareader import data
from datetime import date 
end = date.today()

string_value = 'itslinuxfoss'
index_position = 2
new_value = 'h'
 
string_value = end[:index_position] + new_value + end[index_position+1:]
print(string_value)