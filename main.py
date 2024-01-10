# -*- coding: utf-8 -*-
"""
Created on Wed Jan 10 23:14:34 2024

@author: USER
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jan  9 23:47:40 2024

@author: USER
"""


import re
import nltk
import numpy as np

with open("CFG.txt", "r", encoding = "utf-8-sig") as filename:
    CFG = filename.readlines()

lexical_rules = {}
products = {}
pos_tags = set(["Noun","Verb", "Adj", "Adv", "Conj", "Prep", "Pronoun", "Int", "Plural", "Dative", "Locative", "Genitive",\
               "Accusative", "Ablative", "Instrumental", "P1sg", "P2sg", "P3sg", "P1pl","P2pl", "P3pl","A1sg", "A2sg",\
                "A3sg", "A1pl","A2pl", "A3pl", "Present", "Past", "Progressive", "Future", "Copular", "Rel", "Mi1sg", "Mi2sg","Mi3sg",\
                    "Mi1pl", "Mi2pl", "Mi3pl", "PastCop", "NEG"])

reverse_products = {}
reverse_lexical_rules = {}
new_reverse_products = {}
new_reverse_lexical_rules = {}
new_lexical_rules = {}
new_products = {}

for line in CFG:
    line = line.strip()
    lhs = line.split(" -> ")[0]
    rhs = line.split(" -> ")[1]
    parts = rhs.split(" | ")
    if(lhs not in pos_tags):
        constituents = rhs.split(" ")
        constituents = tuple(constituents)
        if(constituents in products):
            products[constituents].append(lhs)
        else:
            products[constituents] = [lhs]
        if(lhs in reverse_products):
            reverse_products[lhs].append(constituents)
        else:
            reverse_products[lhs] = [constituents]
    if(lhs in pos_tags):
        
        for part in parts:
            if(part in lexical_rules):
                lexical_rules[part].append(lhs)
            else:
                lexical_rules[part] = [lhs]
            if (lhs in reverse_lexical_rules):
                reverse_lexical_rules[lhs].append(part)
            
            else:
                reverse_lexical_rules[lhs] = [part]


counter = 1
dummy_added_products = {}
for k,v in products.items():
    if(len(k) > 2):
        for lhs in v:
            for i in range(len(k)-1):
                if(i == 0):
                    key = k[:2]
                    if(key in dummy_added_products):
                        dummy_added_products[key].append("X"+str(counter))
                        counter += 1
                    else:
                        dummy_added_products[key] = ["X"+str(counter)]
                        counter += 1
                elif(i == len(k)-2):
                    key = ("X"+str(counter-1), k[i+1])
                    if(key in new_products):
                        dummy_added_products[key].append(lhs)
                        counter += 1
                    else:
                        dummy_added_products[key] = [lhs]
                        counter += 1
                else:
                    key = ("X"+str(counter-1), k[i+1])
                    if(key in new_products):
                        dummy_added_products[key].append("X"+str(counter))
                        counter += 1
                    else:
                        dummy_added_products[key] = ["X"+str(counter)]
                        counter += 1
    else:
        for lhs in v:
            if(k in dummy_added_products):
                dummy_added_products[k].append(lhs)
            else:
                dummy_added_products[k] = [lhs]
        

products = dummy_added_products.copy()

text = ""
for k,v in products.items():
    
    for lhs in v:
        if(type(lhs) == str):
            text = text + lhs+" -> "
            for i in range(len(k)):
                if(i == len(k)-1):
                    text += k[i] +"\n"
                else:
                    text += k[i] +" "
            
        else:
            text = text + lhs[0]+" -> "
            for i in range(len(k)):
                if(i == len(k)-1):
                    text += k[i] +"\n"
                else:
                    text += k[i] +" "


#with open("CNF_products_intermediate.txt", "w", encoding = "utf-8-sig") as filename:
#    filename.write(text)
    
temp_dict = {}
for k,v in products.items():
    for lhs in v:
        if(lhs in temp_dict):
            temp_dict[lhs].append(k)
        else:
            temp_dict[lhs] = [k]
            
reverse_products = temp_dict.copy()


for product_lhs, product_rhs_list in reverse_products.items():
    for product_rhs in product_rhs_list:
        if(len(product_rhs) == 1 and (product_rhs[0] not in lexical_rules)):
            to_be_visited = []
            if(product_rhs[0] in reverse_products):
                to_be_added = reverse_products[product_rhs[0]].copy()
                for adds in to_be_added:
                    to_be_visited.append((adds, [product_rhs[0]]))
            elif(product_rhs[0] in reverse_lexical_rules):
                if(product_lhs in new_reverse_lexical_rules):
                    to_be_added = reverse_lexical_rules[product_rhs[0]].copy()
                    for adds in to_be_added:
                        new_reverse_lexical_rules[product_lhs].append((adds, [product_rhs[0]]))
                else:
                    to_be_added = reverse_lexical_rules[product_rhs[0]].copy()
                    to_be_appended = []
                    for adds in to_be_added:
                        to_be_appended.append((adds, [product_rhs[0]]))
                    new_reverse_lexical_rules[product_lhs] = to_be_appended.copy()
                
                to_be_visited = []
            else:
                to_be_visited = []
                
            while (len(to_be_visited) != 0):
                visited = to_be_visited.pop(0)
                if(len(visited[0]) != 1):
                    if(product_lhs not in new_reverse_products):
                        new_reverse_products[product_lhs] = [visited]
                    else:
                        new_reverse_products[product_lhs].append(visited)
                elif (visited[0][0] in pos_tags):
                    if(product_lhs in new_reverse_lexical_rules):
                        if(visited[0][0] in reverse_lexical_rules):
                            for terminal in reverse_lexical_rules[visited[0][0]]:
                                new_reverse_lexical_rules[product_lhs].append((terminal, visited[1]+[visited[0][0]]))
                    else:
                        visited[1].append(visited[0][0])
                        if(visited[0][0] in reverse_lexical_rules):
                            
                            to_be_added = reverse_lexical_rules[visited[0][0]].copy()
                            to_be_appended = []
                            for adds in to_be_added:
                                to_be_appended.append((adds, visited[1]))
                            new_reverse_lexical_rules[product_lhs] = to_be_appended.copy()

                else:
                    if(visited[0][0] in reverse_products):
                        to_be_added = reverse_products[visited[0][0]].copy()
                        for adds in to_be_added:
                            to_be_visited.append((adds, visited[1]+[visited[0][0]]))
                    else:
                        pass

for k,v in new_reverse_lexical_rules.items():
    for terminal, intermediate in v:
        if (terminal in new_lexical_rules):
            new_lexical_rules[terminal].append((k,intermediate))
        else:
            new_lexical_rules[terminal]=[(k,intermediate)]

for k,v in new_reverse_products.items():
    for constituents, intermediate in v:
        if (constituents in new_products):
            new_products[constituents].append((k,intermediate))
        else:
            new_products[constituents]=[(k,intermediate)]    

cnf_products = products.copy()
cnf_lexical_rules = lexical_rules.copy()
for k,v in new_products.items():
    if k in cnf_products:
        cnf_products[k].extend(new_products[k])
    else:
        cnf_products[k] = new_products[k]

for k,v in new_lexical_rules.items():
    if k in cnf_lexical_rules:
        cnf_lexical_rules[k].extend(new_lexical_rules[k])
    else:
        cnf_lexical_rules[k] = new_lexical_rules[k]


final_cnf_products = {}
for k,v in cnf_products.items():
    if(len(k) != 1):
        final_cnf_products[k] = v

cnf_products = final_cnf_products.copy()
        
text = ""
for k,v in cnf_products.items():
    
    for lhs in v:
        if(type(lhs) == str):
            text = text + lhs+" -> "
            for i in range(len(k)):
                if(i == len(k)-1):
                    text += k[i] +"\n"
                else:
                    text += k[i] +" "
            
        else:
            text = text + lhs[0]+" -> "
            for i in range(len(k)):
                if(i == len(k)-1):
                    text += k[i] +"\n"
                else:
                    text += k[i] +" "


#with open("CNF_products.txt", "w", encoding = "utf-8-sig") as filename:
#    filename.write(text)


other_text = ""
for k,v in cnf_lexical_rules.items():
    
    for lhs in v:
        if(type(lhs) == str):
            other_text = other_text + lhs+" -> " + k + "\n"
            
            
        else:
            other_text = other_text + lhs[0]+" -> " + k + "\n"

#with open("CNF_lexical_rules.txt", "w", encoding = "utf-8-sig") as filename:
#    filename.write(other_text)
    
reverse_cnf_products = {}
for k,v in cnf_products.items():
    for lhs in v:
        if(type(lhs) == str):
            if(lhs in reverse_cnf_products):
                reverse_cnf_products[lhs].append(k)
            else:
                reverse_cnf_products[lhs] = [k]
        else:
            if(lhs[0] in reverse_cnf_products):
                reverse_cnf_products[lhs[0]].append(k)
            else:
                reverse_cnf_products[lhs[0]] = [k]

class Node():
    def __init__(self, content, children = None, parent = None):
        self.content = content
        self.children = children
        self.parent = parent
        self.bracket_notation = ""
        self.intermediate = None
        self.person = None
        self.number = None
        self.time = None
        
        
def create_duplicate_node(node):
    copy_node = Node(node.content[:])
    if(node.children == None):
        copy_node.children = None
    else:
        copy_node.children = []
        for child in node.children:
            copy_node.children.append(create_duplicate_node(child))
    copy_node.bracket_notation = node.bracket_notation[:]
    if(node.intermediate == None):
        copy_node.intermediate = None
    else:
        copy_node.intermediate = node.intermediate[:]
    
    if(node.person == None):
        copy_node.person = None
    else:
        copy_node.person = node.person[:]
    return copy_node


class Grammar():
    def __init__(self, products, lexical_rules):
        self.products = products
        self.lexical_rules = lexical_rules

def print_tree(node):
    if(node == None):
        return 
    if (node.children == None):
        node.bracket_notation = "["+node.content+"]"
        return
    node.bracket_notation = "["+node.content
    for child in node.children:
        print_tree(child)
        node.bracket_notation += child.bracket_notation
    node.bracket_notation += "]"
    return 
def turn_into_cfg_tree_step_1(node):
    if(node == None):
        return 
    
    if (node.children == None):
        return
    
    if(node.intermediate != None):
        for ara in node.intermediate:
            temp = Node(ara)
            if(ara in person_agreements):
                temp.person = person_agreements[ara]
            if(ara in number_agreements):
                temp.number = number_agreements[ara]
            if(ara in time_agreements):
                temp.time = time_agreements[ara]
            temp.children = node.children.copy()
            for temp_child in temp.children:
                temp_child.parent = temp
            temp.parent = node
            node.children = [temp]
            node = temp
    for child in node.children:
        turn_into_cfg_tree_step_1(child)
    return 

def turn_into_cfg_tree_step_2(node):
    if(node == None):
        return 
    if (node.children == None):
        return
    
    if(node.content.startswith("X")):
        actual_rule = reverse_cnf_products[node.content]
        Parent = node.parent
        if(Parent == None):
            print(node.content)
            print("asd")
        if(Parent != None):
            for i in range(len(Parent.children)):
                if(node == Parent.children[i]):
                    break
            Parent.children = Parent.children[:i] + node.children.copy() + Parent.children[i+1:]
        for child in node.children:
            child.parent = Parent
        node.children = None
    if(node.children == None):
        return
    for child in node.children:
        turn_into_cfg_tree_step_2(child)
    return 

def clear_bracket_notation(node):
    if(node == None):
        return 
    if (node.children == None):
        node.bracket_notation = ""
        return
    
    for child in node.children:
        clear_bracket_notation(child)
    node.bracket_notation = ""
    return 

def traverse_tree(node):
    if(node == None):
        return 
    if (node.children == None):
        return
    
    for child in node.children:
        traverse_tree(child)
    return 
    
with open("person_agreements.txt", "r", encoding = "utf-8-sig") as filename:
    person_agreements_lines = filename.readlines()
with open("number_agreements.txt", "r", encoding = "utf-8-sig") as filename:
    number_agreements_lines = filename.readlines()
with open("time_agreements.txt", "r", encoding = "utf-8-sig") as filename:
    time_agreements_lines = filename.readlines()

with open("person_important_rules.txt", "r", encoding = "utf-8-sig") as filename:
    person_important_rules_lines = filename.readlines()
with open("number_important_rules.txt", "r", encoding = "utf-8-sig") as filename:
    number_important_rules_lines = filename.readlines()
with open("time_important_rules.txt", "r", encoding = "utf-8-sig") as filename:
    time_important_rules_lines = filename.readlines()
    
person_agreements = {}
number_agreements = {}
time_agreements = {}
person_important_rules = set()
number_important_rules = set()
time_important_rules =set()
for line in person_agreements_lines:
    line = line.strip()
    split = line.split(" -> ")
    lhs = split[0]
    rhs = split[1]
    person_agreements[lhs] = rhs
    

for line in number_agreements_lines:
    line = line.strip()
    split = line.split(" -> ")
    lhs = split[0]
    rhs = split[1]
    number_agreements[lhs] = rhs
    
for line in time_agreements_lines:
    line = line.strip()
    split = line.split(" -> ")
    lhs = split[0]
    rhs = split[1]
    time_agreements[lhs] = rhs

for line in person_important_rules_lines:
    line = line.strip()
    split = line.split(" -> ")
    lhs = split[0]
    rhs = split[1]
    rhs_split = tuple(rhs.split(" "))
    person_important_rules.add(rhs_split)
    

for line in number_important_rules_lines:
    line = line.strip()
    split = line.split(" -> ")
    lhs = split[0]
    rhs = split[1]
    rhs_split = tuple(rhs.split(" "))
    number_important_rules.add(rhs_split)
    
for line in time_important_rules_lines:
    line = line.strip()
    split = line.split(" -> ")
    lhs = split[0]
    rhs = split[1]
    rhs_split = tuple(rhs.split(" "))
    
    time_important_rules.add(rhs_split)


def cky_parse(grammar, words):
    table = [[[] for i in range(len(words)+1)] for j in range(len(words)+1)]
    for i in range(len(words)):
        
        possiblities = grammar.lexical_rules[words[i]]
        primary_node = Node(words[i])
        if(words[i] in person_agreements):
            primary_node.person = person_agreements[words[i]]
        if(words[i] in number_agreements):
            primary_node.number = number_agreements[words[i]]
        if(words[i] in time_agreements):
            primary_node.time = time_agreements[words[i]]
        for pos in possiblities:
            copy_primary_node = create_duplicate_node(primary_node)
            if(type(pos) == str):
                node = Node(pos)
                if(pos in person_agreements):
                    node.person = person_agreements[pos]
                if(pos in number_agreements):
                    node.number = number_agreements[pos]
                if(pos in time_agreements):
                    node.time = time_agreements[pos]
                node.children = [copy_primary_node]
                copy_primary_node.parent = node
            else:
                node = Node(pos[0])
                if(pos[0] in person_agreements):
                    node.person = person_agreements[pos[0]]
                if(pos[0] in number_agreements):
                    node.number = number_agreements[pos[0]]
                if(pos[0] in time_agreements):
                    node.time = time_agreements[pos[0]]
                node.children = [copy_primary_node]
                copy_primary_node.parent = node
                node.intermediate = pos[1]
            table[i][i+1].append(node)
    for j in range(2,len(words)+1):
        for i in range(j-2,-1,-1):
            for k in range(i+1,j):
                for l in range(len(table[i][k])):
                    for m in range(len(table[k][j])):
                        if((table[i][k][l].content, table[k][j][m].content) in grammar.products):
                            derivations = grammar.products[(table[i][k][l].content, table[k][j][m].content)]
                           
                            for derivation in derivations:
                                if(type(derivation) == str):
                                    node = Node(derivation)
                                    copy_node_1 = create_duplicate_node(table[i][k][l])
                                    copy_node_2 = create_duplicate_node(table[k][j][m])
                                    node.children = [copy_node_1, copy_node_2]
                                    copy_node_1.parent = node
                                    copy_node_2.parent = node
                                    table[i][j].append(node)            
                                else:
                                    node = Node(derivation[0])
                                    copy_node_1 = create_duplicate_node(table[i][k][l])
                                    copy_node_2 = create_duplicate_node(table[k][j][m])
                                    node.children = [copy_node_1, copy_node_2]
                                    node.intermediate = derivation[1]
                                    copy_node_1.parent = node
                                    copy_node_2.parent = node
                                    table[i][j].append(node) 
    
    return table

def make_tree(table):
    possible_parses = []
    final_cell = table[0][-1]
    trees = []
    for node in final_cell:
        if node.content == "S":
            trees.append(node)
            
            turn_into_cfg_tree_step_1(node)
            print_tree(node)
            
            if("X" in node.bracket_notation):
                boolean = True
            else:
                boolean = False
            counter = 0
            while(boolean == True and counter < 10):
                print_tree(node)
                turn_into_cfg_tree_step_2(node)
                print_tree(node)
                if("X" in node.bracket_notation):
                    boolean = True
                    clear_bracket_notation(node)
                else:
                    boolean = False
                counter += 1
           
            possible_parses.append(node.bracket_notation)
            #traverse_tree(node)
    return possible_parses, trees

    
def check_person_agreement(node):
    if(node == None):
        return True
    if (node.children == None):
        return True
    
    for child in node.children:
        if(check_person_agreement(child) == False):
            return False
    persons = set()
    for child in node.children:
        if(child.person != None):
            persons.add(child.person[:])
    
    if(len(persons)> 1):
        constituent = []
        for child in node.children:
            constituent.append(child.content)
        constituent = tuple(constituent)
        if(constituent in person_important_rules):
            return False
        else:
            node.person = None
            return True
        return False
    elif(len(persons) == 0):
        return True
    else:
        node.person = list(persons)[0][:]
        return True
    return 

def check_number_agreement(node):
    if(node == None):
        return True
    
    if (node.children == None):
        return True
    
    for child in node.children:
        if(check_number_agreement(child) == False):
            return False
    numbers = set()
    for child in node.children:
        if(child.number != None):
            numbers.add(child.number[:])
    
    if(len(numbers)> 1):
        constituent = []
        for child in node.children:
            constituent.append(child.content)
        constituent = tuple(constituent)
        if(constituent in number_important_rules):
            return False
        else:
            node.number = None
            return True
        return False
    elif(len(numbers) == 0):
        return True
    else:
        node.number = list(numbers)[0][:]
        return True

    return 

def check_time_agreement(node):
    if(node == None):
        return True
    if (node.children == None):
        return True
    
    for child in node.children:
        if(check_time_agreement(child) == False):
            return False
    times = set()
    for child in node.children:
        if(child.time != None):
            times.add(child.time[:])
    
    if(len(times)> 1):
        constituent = []
        for child in node.children:
            constituent.append(child.content)
        constituent = tuple(constituent)
        if(constituent in time_important_rules):
            return False
        else:
            node.time = None
            return True
        return False
    elif(len(times) == 0):
        return True
    else:
        node.time = list(times)[0][:]
        return True
    return 

grammar = Grammar(cnf_products, cnf_lexical_rules)

words = ["dün", "arkadaş", "-Im", "-yA", "bir", "hediye", "al", "-dI", "-m"]

table = cky_parse(grammar,words)
parses,trees = make_tree(table)


correct_parse_indices = []
if len(trees)!= 0:
    for i in range(len(trees)):
        if(check_person_agreement(trees[i]) and check_number_agreement(trees[i]) and check_time_agreement(trees[i])):
            correct_parse_indices.append(i)

if len(parses) != 0:
    for i in correct_parse_indices:
        print(parses[i])
#print(len(parses))
#print(len(correct_parse_indices))