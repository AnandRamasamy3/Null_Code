import sys,os,re,json
from src.data_structures.stack import *

class database:
    def __init__(self):
        self.keywords=[]
        self.variables={}
        self.load_database()
    def load_database(self):
        fobj=open("src/database.json")
        data=json.load(fobj)
        fobj.close()
        self.keywords=data["keywords"][:]
        self.operator_priority=data["operator_priority"][:]
        self.functions=data["functions"][:]

class Compiler:
    def __init__(self,CODE):
        self.CODE=CODE
        self.database=database()
        self.variable_constraints=[95]+list(range(48,58))+list(range(97,123))+list(range(65,91))
        self.variable_constraints_for_initial=[95]+list(range(97,123))+list(range(65,91))
        self.loop=stack()
        self.result_text_for_label=""
    def split_as_variables_operators_and_integers(self):
        final=[]
        item=stack()
        last=None
        inside_string=False
        self.CODE_divided_by_new_line=self.CODE.split("\n",)
        for line in self.CODE_divided_by_new_line:
            result=[]
            for character in line+" ":
                if character=="\"":
                    if len("".join(item.values))>0:
                        prev_index=(line.index(character))-1
                        if len("".join(item.values))==1:
                            result.append("".join(item.values))
                        else:
                            result.append("\""+"".join(item.values))
                    item.empty()
                    inside_string=not inside_string
                    continue
                if inside_string:
                    item.push(character)
                    continue
                if character in [" "]:
                    if len("".join(item.values))>0:
                        result.append("".join(item.values))
                    item.empty()
                elif ord(character) in self.variable_constraints:
                    if last!=None:
                        if ord(last) in self.variable_constraints:
                            item.push(character)
                        else:
                            if len("".join(item.values))>0:
                                result.append("".join(item.values))
                            item.empty()
                            item.push(character)
                    else:
                        item.push(character)
                else:
                    if len("".join(item.values))>0:
                        result.append("".join(item.values))
                    item.empty()
                    item.push(character)
                last=character
            final.append(result)
        self.CODE=final[:]
        if "EOL" in self.CODE:
            self.make_error(message="EOL is a reserved keyword. Don't use it in the Code.")
        while "\n" in self.CODE:
            self.CODE[self.CODE.index("\n")]="EOL"
        # self.CODE.insert(0,"EOL")
    def is_variable(self,word):
        for character_index in range(len(word)):
            character=list(word)[character_index]
            if character_index==0:
                if ord(character) not in self.variable_constraints_for_initial:
                    return False
            else:
                if ord(character) not in self.variable_constraints:
                    return False
        return True
    def make_error(self,line_index=None,message="syntax error"):
        print ("error message")
        self.result_text_for_label+="error message\n"
        if line_index==None:
            print (message)
            self.result_text_for_label+=message+"\n"
        else:
            print (message,"on line:",line_index+1)
            self.result_text_for_label+=message+" on line: "+str(line_index+1)+"\n"
            print (self.CODE_divided_by_new_line[line_index])
            self.result_text_for_label+=self.CODE_divided_by_new_line[line_index]+"\n"
        sys.exit()
    def and_operator(self,prev,next,line_index):
        if prev=="false" and next=="false":
            return "false"
        elif prev=="false" and next=="true":
            return "false"
        elif prev=="true" and next=="false":
            return "false"
        elif prev=="true" and next=="true":
            return "true"
        else:
            self.make_error(line_index=line_index,message="data error")
    def or_operator(self,prev,next,line_index):
        if prev=="false" and next=="false":
            return "false"
        elif prev=="false" and next=="true":
            return "true"
        elif prev=="true" and next=="false":
            return "true"
        elif prev=="true" and next=="true":
            return "true"
        else:
            self.make_error(line_index=line_index,message="data error")
    def not_operator(self,next,line_index):
        if next=="false":
            return "true"
        elif next=="true":
            return "false"
        else:
            self.make_error(line_index=line_index,message="data error")
    def get_value(self,word,line_index):
        # print (word,line_index)
        try:
            if str(word)[0]=="\"":
                return word
            elif "." in str(word):
                return float(word)
            elif 48<=ord(str(word)[0])<=57:
                return int(word)
            elif str(word) in ["true","false"]:
                return str(word)
            elif self.is_variable(str(word)):
                if str(word) in self.database.variables:
                    # print ("ooops",word)
                    return self.get_value(self.database.variables[str(word)],line_index)
                else:
                    self.make_error(line_index=line_index,message=str(word)+" not defined")
            elif str(word)[0]=="-":
                # print ("hahahahahaha",(-1)*self.get_value(str(word)[1:],line_index))
                return (-1)*self.get_value(str(word)[1:],line_index)
            else:
                self.make_error(line_index=line_index,message="cannot identify value")
        except:
            self.make_error(line_index=line_index,message="cannot identify value")
    def display(self,result,line_index):
        value=self.solve(result,line_index)
        if str(type(value))[8:-2]=="str":
            if str(value)[0]=="\"":
                print (value[1:])
        else:
            print (value)
        self.result_text_for_label+=str(value)+"\n"
    def solve(self,expression,line_index):
        # print ("before",expression,line_index)
        for operator in self.database.operator_priority:
            while operator in expression:
                index=expression.index(operator)
                prev_index=index-1
                next_index=index+1
                if operator=="(":
                    temp_stack=stack()
                    for word in expression:
                        if word=="(":
                            temp_stack.empty()
                        elif word==")":
                            sub_expression=temp_stack.values[:]
                            result=self.solve(sub_expression,line_index)
                            # print ("ooops",result)
                            start_index=expression.index(word)-len(temp_stack.values)-1
                            iterations_to_delete=len(temp_stack.values)+2
                            # print ("a value",self.database.variables["a"])
                            # print (expression)
                            for ___ in range(iterations_to_delete):
                                expression.pop(start_index)
                            expression.insert(start_index,result)
                            # print ("brackets",expression)
                            # return expression
                        else:
                            temp_stack.push(word)
                elif operator==".":
                    try:
                        prev_value=str(self.get_value(expression[prev_index],line_index))
                        next_value=str(self.get_value(expression[next_index],line_index))
                        for ___ in range(3):
                            expression.pop(prev_index)
                        # print (expression)
                        value=float(prev_value+"."+next_value)
                        expression.insert(prev_index,value)
                        # print ("hahahahahaha")
                    except:
                        # print ("ooops")
                        self.make_error(line_index=line_index)
                elif operator=="/":
                    # print ("hahahahahaha")
                    try:
                        prev_value=self.get_value(expression[prev_index],line_index)
                        next_value=self.get_value(expression[next_index],line_index)
                        # print ("ooops",prev_value,next_value)
                        for ___ in range(3):
                            expression.pop(prev_index)
                        value=self.get_value(prev_value/next_value,line_index)
                        expression.insert(prev_index,value)
                    except:
                        self.make_error(line_index=line_index)
                elif operator=="*":
                    try:
                        # print ("ooops",expression[prev_index],expression[next_index])
                        prev_value=self.get_value(expression[prev_index],line_index)
                        next_value=self.get_value(expression[next_index],line_index)
                        for ___ in range(3):
                            expression.pop(prev_index)
                        value=self.get_value(prev_value*next_value,line_index)
                        expression.insert(prev_index,value)
                    except:
                        self.make_error(line_index=line_index)
                elif operator=="%":
                    try:
                        prev_value=self.get_value(expression[prev_index],line_index)
                        next_value=self.get_value(expression[next_index],line_index)
                        for ___ in range(3):
                            expression.pop(prev_index)
                        value=self.get_value(prev_value%next_value,line_index)
                        expression.insert(prev_index,value)
                    except:
                        self.make_error(line_index=line_index)
                elif operator=="+":
                    try:
                        prev_value=self.get_value(expression[prev_index],line_index)
                        next_value=self.get_value(expression[next_index],line_index)
                        for ___ in range(3):
                            expression.pop(prev_index)
                        value=self.get_value(prev_value+next_value,line_index)
                        expression.insert(prev_index,value)
                    except:
                        self.make_error(line_index=line_index)
                elif operator=="-":
                    prev_value=str(expression[prev_index])
                    if 48<=ord(prev_value[0])<=57 or self.is_variable(prev_value):
                        try:
                            # print (expression)
                            prev_value=self.get_value(expression[prev_index],line_index)
                            next_value=self.get_value(expression[next_index],line_index)
                            for ___ in range(3):
                                expression.pop(prev_index)
                            value=self.get_value(prev_value-next_value,line_index)
                            expression.insert(prev_index,value)
                            # print ("ooops",prev_value,next_value)
                        except:
                            self.make_error(line_index=line_index)
                    else:
                        try:
                            next_value=self.get_value(expression[next_index],line_index)
                            for ___ in range(2):
                                expression.pop(index)
                            value=self.get_value((-1)*next_value,line_index)
                            expression.insert(index,value)
                        except:
                            self.make_error(line_index=line_index)
                    # print ("final - simplification",expression)
                elif operator=="is":
                    try:
                        prev_value=self.get_value(expression[prev_index],line_index)
                        next_value=self.get_value(expression[next_index],line_index)
                        for ___ in range(3):
                            expression.pop(prev_index)
                        value="true" if (prev_value==next_value) else "false"
                        value=self.get_value(value,line_index)
                        expression.insert(prev_index,value)
                    except:
                        self.make_error(line_index=line_index)
                elif operator=="lt":
                    try:
                        prev_value=self.get_value(expression[prev_index],line_index)
                        next_value=self.get_value(expression[next_index],line_index)
                        for ___ in range(3):
                            expression.pop(prev_index)
                        value="true" if (prev_value<next_value) else "false"
                        value=self.get_value(value,line_index)
                        expression.insert(prev_index,value)
                    except:
                        self.make_error(line_index=line_index)
                elif operator=="le":
                    try:
                        prev_value=self.get_value(expression[prev_index],line_index)
                        next_value=self.get_value(expression[next_index],line_index)
                        for ___ in range(3):
                            expression.pop(prev_index)
                        value="true" if (prev_value<=next_value) else "false"
                        value=self.get_value(value,line_index)
                        expression.insert(prev_index,value)
                    except:
                        self.make_error(line_index=line_index)
                elif operator=="gt":
                    try:
                        prev_value=self.get_value(expression[prev_index],line_index)
                        next_value=self.get_value(expression[next_index],line_index)
                        for ___ in range(3):
                            expression.pop(prev_index)
                        value="true" if (prev_value>next_value) else "false"
                        value=self.get_value(value,line_index)
                        expression.insert(prev_index,value)
                    except:
                        self.make_error(line_index=line_index)
                elif operator=="ge":
                    try:
                        prev_value=self.get_value(expression[prev_index],line_index)
                        next_value=self.get_value(expression[next_index],line_index)
                        for ___ in range(3):
                            expression.pop(prev_index)
                        value="true" if (prev_value>=next_value) else "false"
                        value=self.get_value(value,line_index)
                        expression.insert(prev_index,value)
                    except:
                        self.make_error(line_index=line_index)
                elif operator=="and":
                    try:
                        prev_value=self.get_value(expression[prev_index],line_index)
                        next_value=self.get_value(expression[next_index],line_index)
                        for ___ in range(3):
                            expression.pop(prev_index)
                        value=self.get_value(self.and_operator(prev_value,next_value,line_index),line_index)
                        expression.insert(prev_index,value)
                    except:
                        self.make_error(line_index=line_index)
                elif operator=="or":
                    try:
                        prev_value=self.get_value(expression[prev_index],line_index)
                        next_value=self.get_value(expression[next_index],line_index)
                        for ___ in range(3):
                            expression.pop(prev_index)
                        value=self.get_value(self.or_operator(prev_value,next_value,line_index),line_index)
                        expression.insert(prev_index,value)
                    except:
                        self.make_error(line_index=line_index)
                elif operator=="not":
                    try:
                        next_value=self.get_value(expression[next_index],line_index)
                        for ___ in range(2):
                            expression.pop(index)
                        # print ("here",next_value)
                        value=self.get_value(self.not_operator(next_value,line_index),line_index)
                        expression.insert(index,value)
                    except:
                        self.make_error(line_index=line_index)
        # print (expression)
        if len(expression)==1:
            return self.get_value(expression[0],line_index)
        else:
            self.make_error(line_index=line_index)
    def enable_if_loop(self,line_index):
        LOC=self.CODE[line_index][:]
        if LOC[-1]==":":
            # print (LOC[1:-1])
            value=self.solve(LOC[1:-1],line_index)
            # print (value)
            if value=="true":
                pass
                self.loop.push({
                    "type":"if",
                    "line_index":line_index
                })
                return line_index
            else:
                last_line=line_index+1
                temp_stack=stack()
                while True:
                    temp_code=self.CODE[last_line][:]
                    if len(temp_code)<=0:
                        pass
                    elif temp_code[0]=="#":
                        pass
                    elif temp_code[0] in ["if","for","while"]:
                        temp_stack.push(temp_code[0])
                    elif temp_code[0]==";":
                        if temp_stack.pointer==-1:
                            break
                        else:
                            temp_stack.pop()
                    last_line+=1
            return last_line
        else:
            self.make_error(line_index=line_index)
    def enable_for_loop(self,line_index):
        LOC=self.CODE[line_index][:]
        if len(LOC)>=7:
            variable_name=LOC[1]
            if self.is_variable(variable_name):
                pass
                if LOC[2]=="from" and LOC[-1]==":" and "to" in LOC:
                    try:
                        start_value=self.solve(LOC[3:LOC.index("to")],line_index)
                        end_value=self.solve(LOC[LOC.index("to")+1:-1],line_index)
                        # print (start_value,end_value)
                        last_line=line_index+1
                        temp_stack=stack()
                        while True:
                            temp_code=self.CODE[last_line][:]
                            if len(temp_code)<=0:
                                pass
                            elif temp_code[0]=="#":
                                pass
                            elif temp_code[0] in ["if","for","while"]:
                                temp_stack.push(temp_code[0])
                            elif temp_code[0]==";":
                                if temp_stack.pointer==-1:
                                    break
                                else:
                                    temp_stack.pop()
                            last_line+=1
                        self.database.variables.update({
                            variable_name:start_value
                        })
                        self.loop.push({
                            "type":"for",
                            "from":variable_name,
                            "upto":end_value,
                            "first_line":line_index,
                            "last_line":last_line
                        })
                        # print (last_line,line_index)
                    except:
                        self.make_error(line_index=line_index)
                else:
                    self.make_error(line_index=line_index)
            else:
                self.make_error(line_index=line_index,message="invalid variable name")
        else:
            self.make_error(line_index=line_index)
    def re_loop_for(self,line_index):
        variable_name=self.loop.top()["from"]
        # print ("till now there is no error",variable_name)
        current_value=self.get_value(variable_name,line_index)
        upto=self.loop.top()["upto"]
        if current_value<upto:
            first_line=self.loop.top()["first_line"]
            self.database.variables[variable_name]+=1
            return first_line
        else:
            last_line=self.loop.top()["last_line"]
            self.loop.pop()
            return last_line
    def enable_while_loop(self,line_index):
        LOC=self.CODE[line_index][:]
        if len(LOC)>=3:
            if LOC[-1]==":":
                pass
                try:
                    value=self.solve(LOC[1:-1],line_index)
                    if value=="true":
                        last_line=line_index+1
                        temp_stack=stack()
                        while True:
                            temp_code=self.CODE[last_line][:]
                            if len(temp_code)<=0:
                                pass
                            elif temp_code[0]=="#":
                                pass
                            elif temp_code[0] in ["if","for","while"]:
                                temp_stack.push(temp_code[0])
                            elif temp_code[0]==";":
                                if temp_stack.pointer==-1:
                                    break
                                else:
                                    temp_stack.pop()
                            last_line+=1
                        self.loop.push({
                            "type":"while",
                            "first_line":line_index,
                            "last_line":last_line
                        })
                        # print (last_line,line_index)
                        return line_index
                    elif value=="false":
                        last_line=line_index+1
                        temp_stack=stack()
                        while True:
                            temp_code=self.CODE[last_line][:]
                            if len(temp_code)<=0:
                                pass
                            elif temp_code[0]=="#":
                                pass
                            elif temp_code[0] in ["if","for","while"]:
                                temp_stack.push(temp_code[0])
                            elif temp_code[0]==";":
                                if temp_stack.pointer==-1:
                                    break
                                else:
                                    temp_stack.pop()
                            last_line+=1
                        return last_line
                    else:
                        self.make_error(line_index=line_index)
                except:
                    self.make_error(line_index=line_index)
            else:
                self.make_error(line_index=line_index)
        else:
            self.make_error(line_index=line_index)
    def re_loop_while(self,line_index):
        LOC=self.CODE[self.loop.top()["first_line"]][:]
        # print (LOC)
        value=self.solve(LOC[1:-1],line_index)
        # print ("here")
        if value=="true":
            line_index=self.loop.top()["first_line"]
            return line_index
        else:
            return line_index+1
    def break_and_continue(self,line_index):
        LOC=self.CODE[line_index][:]
        if self.loop.pointer>-1:
            if self.loop.top()["type"]=="if":
                self.loop.pop()
                if self.loop.top()["type"] in ["if","while"]:
                    if LOC[0]=="break":
                        next_line=self.loop.top()["last_line"]
                        self.loop.pop()
                        return next_line
                    else:
                        next_line=self.loop.top()["first_line"]
                        return next_line
            else:
                if LOC[0]=="break":
                    next_line=self.loop.top()["last_line"]
                    self.loop.pop()
                    return next_line
                else:
                    next_line=self.loop.top()["first_line"]
                    return next_line
        else:
            self.make_error(line_index=line_index,message="break cannot be used here")
    def parse(self):
        line_index=0
        while line_index<=len(self.CODE)-1:
            LOC=self.CODE[line_index][:]
            # print (">>>",line_index," ".join(LOC))
            if len(LOC)<=0:
                pass
            elif LOC[0]=="#":
                pass
            elif LOC[0]=="if":
                line_index=self.enable_if_loop(line_index)
            elif LOC[0]=="for":
                self.enable_for_loop(line_index)
            elif LOC[0]=="while":
                line_index=self.enable_while_loop(line_index)
            elif LOC[0]==";":
                pass
                if self.loop.top()!=None:
                    if self.loop.top()["type"]=="for":
                        line_index=self.re_loop_for(line_index)
                    elif self.loop.top()["type"]=="if":
                        self.loop.pop()
                    elif self.loop.top()["type"]=="while":
                        # print ("here")
                        line_index=self.re_loop_while(line_index)
            elif LOC[0] in ["break","continue"]:
                pass
                self.break_and_continue(line_index)
            elif self.is_variable(LOC[0]) and LOC[1]=="=":
                variable_name=LOC[0]
                value=self.solve(LOC[2:][:],line_index)
                value=self.get_value(value,line_index)
                self.database.variables.update({
                    variable_name:value
                })
            elif LOC[0]=="display":
                self.display(LOC[1:],line_index)
            else:
                # print ("ooops")
                pass
            line_index+=1
    def run(self):
        pass
        self.split_as_variables_operators_and_integers()
        self.parse()
        # for variable_name in self.database.variables:
        #     print (variable_name,self.database.variables[variable_name])
        # result=self.get_value("e",1)
        # print (result,type(result))

if __name__=="__main__":
    if len(sys.argv)>1:
        try:
            fobj=open(sys.argv[1],"r")
        except:
            self.make_error(message="cannot find file")
        CODE=fobj.read()
        compiler=Compiler(CODE)
        compiler.run()

    else:
        about_text=open("src/about.txt").read()
        print (about_text)



# ------------------------------------------------------------------------------
