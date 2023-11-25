# Put the numbers here ↴
numbers = "4371 4470 519 1621 519"
number_list = numbers.split()
number_list = [int(num) for num in number_list]
hex_list = ['0x{}'.format(hex(num)[2:]) for num in number_list]
hex_string = ', '.join(hex_list)
print(hex_string)