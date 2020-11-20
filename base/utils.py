import math, random 
   
def generate_class_code(total_digits,existing_codes) :  
    digits = ''.join([str(i) for i in range(0,10)])
    code = ""  
    while True:
        for i in range(total_digits) : 
            code += digits[math.floor(random.random() * 10)] 
        if code not in existing_codes:
            print('Code not in existing codes')
            break
    return code 