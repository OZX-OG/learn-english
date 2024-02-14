f = open("words.txt", "r", encoding='UTF-8')
x = f.readlines()
l = 'قبر'
print(x[0].strip() )
print( l)
print( x == l)
# print( f.readlines()[0].split(":")[1] )
