import re
def calculation(string):
    stk = []
    i = 0
    while (i < len(string)):
        if string[i].isnumeric(): stk.append(string[i])
        elif string[i] in "*/%":
            temp = 0
            if (string[i] == "*"): temp = int(stk[-1]) * int(string[i + 1])
            elif (string[i] == "/"): temp = int(stk[-1]) // int(string[i + 1])
            else: temp = int(stk[-1]) % int(string[i + 1])
            stk.pop()
            stk.append(temp)
            i += 1
        else:
            if string[i] in "+-": stk.append(string[i])
            else: stk.append(dict_variable_value[string[i]])
        i += 1
    sum = 0
    length=len(stk)
    while (stk and length>2):
        if stk[-1] in "+-":
            if stk[-1] == "+": sum = int(stk[-2]) + sum
            else: sum = int(stk[-2]) - sum
            stk.pop()
            stk.pop()
        else:
            sum += int(stk[-1])
            stk.pop()
    return sum

def operation(lst,variable,operator):
    lst1=["+=","-=","*=","/=","%="]
    if operator=="++": return 1
    if operator=="--": return -1
    if operator in lst1: lst[1]=variable+operator[0]+lst[1]
    return calculation(lst[1])

def str_matching(string):
    arth_operator = ["+", "+=", "++", "-", "-=", "--", "*", "*=", "/", "/=", "%", "%=","="]
    rela_operator=["<","=<",">=",">","==","!="]
    if "int" in string:
        if "=" in string:return "initialization"
        else:return "initialazeWithoutValue"
    for i in string:
        if i in rela_operator:
            if "cout" not in string: return "condition"
        if i in arth_operator: return "increament"
    return "No matching"

def pattern_matching(pattern,string):
    pattern_regex=""
    operator=""
    lst_operator=["+","+=","++","-","-=","--","*","*=","/","/=","%","%=","="]

    if string=="initialization": pattern_regex="int([a-z]*)=([0-9]*)"
    if string=="initialazeWithoutValue": pattern_regex="int([a-z]*[0-9]*)"
    if string=="condition": pattern_regex="([a-z]*)([<]*)(?:<=?|>=?|==|!=)([0-9]*)"
    if string=="increament": pattern_regex = "([+-]*)([a-z]*)([+*%/=-]*)([a-z0-9+%*/-]*)"

    lst = []
    match= re.findall(pattern_regex,pattern)
    match= list(match[0])
    for i in match:
        if i != '':
            if i!='int':
                if i in lst_operator: operator=i
                else: lst += [i]
    if string=="increament": return lst,operator,"increament"
    return lst

def splitting_condition(string):
    start_index = string.index("(")
    end_index = string.rindex(")")
    line = string[start_index + 1:end_index].split(";")
    return line
def for_loop(start,end):
    if not visited[start-1]:
        line = splitting_condition(input_file_lst[start - 1])
        visited[start-1]=True

        lst_con=pattern_matching(line[1], str_matching(line[1])) # i<5
        variable,value_con=lst_con[0],int(lst_con[1])

        temp=str_matching(line[0])
        lst_init= pattern_matching(line[0], temp) #int i, int i=0
        if temp == "increament":
            variable_init, value_init = lst_init[0][0], int(lst_init[0][1])
        else:
            variable_init, value_init = lst_init[0], int(lst_init[1])
        dict_variable_value[variable_init] = 0

        lst_inc=pattern_matching(line[2], str_matching(line[2])) #i++
        temp=operation(lst_inc[0],variable,lst_inc[1])
        sum=abs((value_con-value_init)//temp)

        while(start<end): # inside in loop
            if not visited[start]:
                temp=str_matching(input_file_lst[start])
                visited[start]=True
                if temp != "No matching":
                    lst=pattern_matching(input_file_lst[start],temp)
                    if lst[-1]=="increament":
                        val=operation(lst[0], variable, lst[1])
                        if lst[1]=="++" or lst[1]=="--": sum=sum//2
                        else: sum=sum//val
            start+=1

    return sum

def while_loop(start,end):
    if not visited[start-1]:
        line=splitting_condition(input_file_lst[start-1])
        visited[start - 1] = True
        lst_con = pattern_matching(line[0], str_matching(line[0]))
        variable, value_con = lst_con[0], int(lst_con[1])
        sum=abs(value_con-int(dict_variable_value[variable]))

        while (start < end):
            if not visited[start]:
                visited[start] = True
                temp = str_matching(input_file_lst[start])
                if temp != "No matching":
                    lst = pattern_matching(input_file_lst[start], temp)
                    if lst[-1] == "increament":
                        val = operation(lst[0], variable, lst[1])
                        if lst[1] == "++" or lst[1] == "--":
                            sum = sum // 1
                        else:
                            sum = sum // val
            start += 1

    return sum

def do_while_loop(start,end):
    if not visited[end-1]:
        line = splitting_condition(input_file_lst[end - 1])

        lst_con = pattern_matching(line[0], str_matching(line[0]))
        variable, value_con = lst_con[0], int(lst_con[1])
        sum = abs(value_con - int(dict_variable_value[variable]))

        while (start < end):
            if not visited[start]:
                visited[start]=True
                temp = str_matching(input_file_lst[start])
                if temp != "No matching":
                    lst = pattern_matching(input_file_lst[start], temp)
                    if lst[-1] == "increament":
                        val = operation(lst[0], variable, lst[1])
                        if lst[1] == "++" or lst[1] == "--":
                            sum = sum // 1
                        else:
                            sum = sum // val
            start += 1

    return sum

def loop_length(start,end):
    length=0
    if "for" in input_file_lst[start-1]:
        length=for_loop(start,end)
    if "while" in input_file_lst[start-1]:
        length=while_loop(start,end)
    if "do" in input_file_lst[start-1]:
        length=do_while_loop(start,end)
    if start<dict_prev["start"] and end>dict_prev["end"]:
        length=length*dict_prev["len"]

    print(length)
    dict_prev["start"]=start
    dict_prev["end"]=end
    dict_prev["len"] = length

def boundary(input_file_lst,dict_Boundary): # input_file_lst = list:string, variable=List
    stack=["stop"]
    dict_loop_opening={}
    index=0
    #-------------------------loop start---------------------------
    while(index<len(input_file_lst)-1):
        #------------- opening start------------------
        if input_file_lst[index]=="gap": pass
        if ("{" in input_file_lst[index]) or (input_file_lst[index+1][0]=="{"): #for(int i=0;i<5;i++){ or for(int i=0;i<5;i++) : (next line {)
            if(input_file_lst[index+1][0]=="{"):
                dict_loop_opening[index+1]=input_file_lst[index]
                stack.append(index+1)
                index+=1
            else:
                dict_loop_opening[index+1]=input_file_lst[index]
                stack.append(index+1)

        else:
            if("for" in input_file_lst[index]) or ("while" in input_file_lst[index]) or ("do" in input_file_lst[index]): # if there is no scoping
                if "do" in input_file_lst[index]:
                    dict_Boundary[index + 1] = {(index+2):input_file_lst[index]}
                    print("loop start:",index+1, " ","loop end:", index + 2) # index+1=do{} index+2=while(i<5)
                    loop_length(index+1, index + 2)
                    index+=1
                else:
                    dict_Boundary[index + 1] = {(index + 1):input_file_lst[index]}
                    print("loop start:",index+1, " ","loop end:", index + 1)
                    loop_length(index + 1, index + 1)
            else:
                temp=str_matching(input_file_lst[index])
                if temp=="initialization":
                    variable,value=pattern_matching(input_file_lst[index],temp)
                    dict_variable_value[variable]=value
                if temp=="initialazeWithoutValue":
                    variable=pattern_matching(input_file_lst[index],temp)
                    dict_variable_value[variable[0]]=0
        #---------------------opening end --------------------

        #------------------- closing start---------------------
        if( "}" in input_file_lst[index]):
            temp=stack[-1]
            if stack[-1]!="stop":
                if ("for" in dict_loop_opening[temp]) or ("while" in dict_loop_opening[temp]) or ("do" in dict_loop_opening[temp]):
                    if "do" in dict_loop_opening[temp]:
                        dict_Boundary[temp]={index+2:dict_loop_opening[temp]}
                        print("loop start:",temp, " ","loop end:", index+2)
                        loop_length(temp, index + 2)
                        index+=1
                    else:
                        dict_Boundary[temp] = {index+1:dict_loop_opening[temp]}
                        print("loop starts:",temp," ","loop end:",index+1)
                        loop_length(temp, index + 1)
                stack.pop()
        #------------------- closing end -----------------------------
        index+=1
    #----------------------loop end-------------------------------
    return dict_Boundary

######################################################
input_file=open("input2.txt")
input_file_lst=[]
dict_Boundary={}
dict_variable_value={}
relation_operator=["<","<=",">",">=","==","!="]
flag=False
visited=[]
dict_prev={"start":0,"end":0,"len":1}
for i in input_file:
    visited.append(False)
    if(len(i)!=1):
        i=i.strip()
        if(i[0]=="/"): input_file_lst+=["gap"] # define comments as gap
        else:
            if "int main" in i: flag=True
            if flag:
                input_file_lst+=[i.replace(" ","")]
            else: input_file_lst+=["gap"]
    else:
        input_file_lst+=["gap"] # define gap
boundary(input_file_lst,dict_Boundary)
