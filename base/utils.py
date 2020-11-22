import math, random  

def generate_class_code(total_digits) :  
    digits = ''.join([str(i) for i in range(0,10)])
    code = ""  
    for i in range(total_digits) : 
        code += digits[math.floor(random.random() * 10)]   
    return code