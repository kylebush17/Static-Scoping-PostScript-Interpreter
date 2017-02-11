 #Programmer: Kyle Bush
# Project: Static Scoping Postscript Interpreter
# Completion: 95% - code is implemented properly just needs a few finishing touches
# Date: November 30th, 2016


import re
#definition for the operand stack to be used for the program
opstack = []

#definition for the dict stack to be used for the program
dictstack = [{}]

#static chain is a list of tuples that contains an index and a dictionary
staticChain = []

index = 0

def dictPush(d):
    #pushes a dictionary d onto the dictionary stack
    dictstack.append(d)

def dictPop():
    #pops the top value from the dictionary stack
    if(dictstack == []):
        return_dict = {}
        return return_dict
    return_dict = dictstack[-1]
    del dictstack[-1]
    return return_dict

def define(scopingRules):

    global opstack,dictstack
    global index
    value = opPop()
    key = opPop()
    key = key[1:]
    Dict = {key:value}
    if scopingRules == "Dynamic" : #add a new dictionary to the dict stack just like last normal
        dictstack[-1][key] = value
    elif scopingRules == "Static": #static rules are a bit different
    #add to the static chain based on index
    	staticChain.append((index,Dict))
    	index += 1
    else:
    	print("invalid operation")
    	
    	


def lookup(name):
    #looks up the name in the list of dictionaries in the stack
    top_dict = dictstack[len(dictstack)-1]
    if name in top_dict.keys():
        return top_dict[name]
    else:
        return False
        
#returns the link
def staticLink(x):
	length = len(staticChain)
	count = 0
	while(count<length):
		#temporary tuple that holds current spot in static chain
		(link,Dict) = staticChain[count]
		
		#return the static link
		if (x in Dict.keys()):
			return link
		else:
			count+=1
	
	#can't find desired index
	return None

def StaticDefined(x):
	length = len(staticChain)
	count = 0
	while(count<length):
		#temporary tuple that holds current spot in static chain
		(link,dict) = staticChain[count]
		
		#return the static link
		if (x in dict.keys()):
			return True
		else:
			count+=1
	return False
	
def is_defined(token,scopingRules):
	if scopingRules == "Dynamic":
		result = in_dict(token)
		return result
	elif scopingRules == "Static": #static rules
		if(len(staticChain)>0):
			(static_link,dict) = staticChain[0]
			is_found = StaticDefined(token) #search static chain
			return is_found
	else:
		return False #was not found
	
def static_lookup(x):			#modified lookup to support static scoping
	if(len(staticChain)>0):
		link = staticLink(x)
		if(link != None):
			(l,Dict) = staticChain[link]
			return Dict[x]
		else:
			return None
	else:
		return None
	
def opPop():
    #pops the top value from the operand stack and returns it.
    #also deletes the element once it has been popped
    if(opstack == []):
       value = 0
       return value
    value = opstack[-1]
    del opstack[-1]
    return value

def opPush(value):
	#push onto the operand stack

	opstack.append(value)
	return
	#adds to the end

def add():
       #pops both of the top two values from the operand stack and adds them
       x = opPop()
       y = opPop()
       z = x + y
       opPush(z)
       return z

def div():
       #pops both of the top two values from the operand stack and divides them
       x = opPop()
       y = opPop()
       z = x/y
       opPush(z)
       return z

def sub():
       #subtracts the two values from the top of the operand stack
       x = opPop()
       y = opPop()
       z = x-y
       opPush(z)
       return z

def mul():
       #multiplies the two values from the top of the operand stack
       x = opPop()
       y = opPop()
       z = x * y
       opPush(z)
       return z

def mod():
       #performs modular division from the top two elements of the operand stack
       x = opPop()
       y = opPop()
       z = x % y
       opPush(z)
       return z

#now begins the string operations:

#returns the length of a string from the top of the stack
def length():       
	s = opPop()
	l = len(s)
	opPush(l)
	return l

#returns the ascii value of the desired character and pushes it onto the stack
def get():
    x = opPop()
    s = opPop()
    a = ord(s[x])
    opPush(a)
    return a

def put():
    a = opPop()
    i = opPop()
    s = opPop()
    s = list(s)
    s[i] = chr(a)
    r =''.join(s)
    opPush(r)
    return r

def getinterval():
    end = opPop()
    begin = opPop()
    s = opPop()
    new = s[begin:end] + ')'
    opPush(new)
    return new

#stack operations:

def sPop():
    x = opPop()

def dup():
    x = opPop()
    opPush(x)
    opPush(x)
    return x

def exch():
    x = opPop()
    y = opPop()
    opPush(x)
    opPush(y)

def copy():
    x = opPop()
    swap = []
    for i in range(x):
        swap.append(opPop())
    for i in range(len(swap)):
        opPush(swap[i])

def stack(scopeRules):
    print('=========================')
    length = len(opstack) -1
    while(length!= -1):
        print(opstack[length])
        length -= 1
    print('=========================')
    if(scopeRules == "Static"):
        length = 0
        while(length <len(staticChain)):
            print('-----m-----n-----')
            print(staticChain[length])
            length += 1


def clear():
    opstack.clear()

def is_name(value):
    if not type(value) is str:
	    return False
    if value[0] != '/':
	    return False
    return True

def is_int_val(s):
    if type(s) is list:
        return False
    try:
        int(s)

        return True
    
    except ValueError:
        return False

#tokenize function given by the assignment
def tokenize(s):
	return re.findall("/?[a-zA-Z][a-zA-Z0-9_]*|[(][\w \W]*[)]|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)



#i took a slightly different approach to the parsing problem. instead of using an
#iterator (which i found to be quite confusing), i used a for loop that recursively
#calls the parse function and creates a separate list every time it
#encounters the '{' character and appends everything between that curly brace and
#the corresponding brace. creates the same result as function
#outlined in the homework 
def parse(tokens):
	i = 0
	nested_code_array = ""
	final_code_array = []
	for token in tokens:
            #i keeps track of the curley braces 
            #if i is one, it has an unclosed curly brace
            #if it is 0 you can append that code array to the
            #final code array
		if i != 0:
			if token == '{': #encounters a nested code array
				i += 1 
			if token == '}':#finds end of a nestedd code array
                           
				i -= 1
			if i == 0:#check to see if all nested code arrays are closed

                                #append nested code array recursively
                                #checking to see if there is another
                                #nested code array inside
				final_code_array.append(parse(tokenize(nested_code_array[:-1])))

				nested_code_array = ""
			else:
				nested_code_array += token + " "
		else:
			if token == '{':
				i += 1
			else: #if not part of a code array, appends to final
				final_code_array.append(token)

	return final_code_array

def in_dict(s):
	for i in dictstack:
		if s in i.keys():
			return True
	return False
   
 
def is_str(token):
	if token[0] != '(':
		return False
	return True



#bulk of the work is done in the interpret function
#modified to accept scoping rules "Dynamic" or "Static"
def interpret(code_array, scopeRules):
    global opstack,dictstack
    global index
    for token in code_array:

        if type(token) is list:
            opPush(token)
        else:
            if token == 'add':
                add()

            elif token == 'dict':
                x = opPop()
                d = {}

            elif token == 'begin':
                dictPush(d)

            elif token == 'sub':
                sub()

            elif token == 'mul':
                mul()

            elif token == 'div':
                div()

            elif token == 'mod':
                print('mod')

            elif token == 'length':
                length()

            elif token == 'get':
                get()

            elif token == 'put':
                put()

            elif token == 'getinterval':
                getinterval()

            elif token == 'sPop':
                opPop()

            elif token == 'dup':
                dup()

            elif token == 'exch':
                exch()

            elif token == 'copy':
                copy()

            elif token == 'stack':
                stack(scopeRules)

            elif token == 'clear':
                clear()

            elif token == 'def':
                define(scopeRules)
             
            elif token == 'end':
                print('end')
                
            elif token == 'for':
                print('enter foor loop')
            else:
            #---pushing onto the "opstack"---
                if is_defined(token,scopeRules):
                    if(scopeRules == "Static"):
                        call = static_lookup(token)
                        if(type(call) == type([])):
                            interpret(call,scopeRules)
                        else:
                            opPush(call)
                    elif scopeRules == "Dynamic":
                        if type(lookup(token) )is list:
                            interpret(lookup(token),scopeRules)
                        else:
                            opPush(lookup(token))
                    else:
                        print("invalid")
                elif is_int_val(token):		#is it an integer? push
                    opPush(int(token))
                    
                elif is_name(token):		#is it a name? push
                    opPush(token)
                    
                elif is_str(token):			#string? push
                    opPush(token)
            #-----------------------------
                    
                        
                    	
                else:
                    break
                

                    
                   
                    

                    



                
                




if __name__ == "__main__":
    sample = '''/fact {
0 dict
begin
/n exch def
1
n -1 1 {mul} for 
end
}def
(factorial function !)  0 9 getinterval 
stack
5 fact 
stack'''
    test2 = '''/x 4 def
/g { x stack } def
/f { /x 7 def g } def
f'''

    

    interpret(parse(tokenize(test2)),"Static")
