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
                "A3sg", "A1pl","A2pl", "A3pl", "Present", "Past", "Progressive", "Future", "Copular"])

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
#print(products)
dummy_added_products = {}
for k,v in products.items():
    if(len(k) > 2):
        #print(k)
        for lhs in v:
            #print(lhs)
            for i in range(len(k)-1):
                if(i == 0):
                    key = k[:2]
                    #print(key)
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
        
#print(dummy_added_products)
#print(reverse_products)
#print(dummy_added_products[("Verb", "Past")])
products = dummy_added_products.copy()
#print(dummy_added_products[("NP",)])

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


with open("CNF_products_intermediate.txt", "w", encoding = "utf-8-sig") as filename:
    filename.write(text)
    
temp_dict = {}
for k,v in products.items():
    for lhs in v:
        if(lhs in temp_dict):
            temp_dict[lhs].append(k)
        else:
            temp_dict[lhs] = [k]
            
reverse_products = temp_dict.copy()
#print(reverse_products.keys())

for product_lhs, product_rhs_list in reverse_products.items():
    for product_rhs in product_rhs_list:
        if(len(product_rhs) == 1 and (product_rhs[0] not in lexical_rules)):
            #print(product_lhs, product_rhs,"*0*0*")
            to_be_visited = []
            if(product_rhs[0] in reverse_products):
                to_be_added = reverse_products[product_rhs[0]].copy()
               # print(to_be_added)
                for adds in to_be_added:
                    to_be_visited.append((adds, [product_rhs[0]]))
                #print(to_be_visited)
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
                #print(visited)
                if(len(visited[0]) != 1):
                    #print(visited, "*****")
                    if(product_lhs not in new_reverse_products):
                        new_reverse_products[product_lhs] = [visited]
                    else:
                        new_reverse_products[product_lhs].append(visited)
                   # print(new_reverse_products)
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
                    #print(new_reverse_lexical_rules)

                else:
                    if(visited[0][0] in reverse_products):
                        to_be_added = reverse_products[visited[0][0]].copy()
                       # print(to_be_added)
                        for adds in to_be_added:
                            #print(visited[1],visited[0][0],"????")
                            to_be_visited.append((adds, visited[1]+[visited[0][0]]))
                       # print(to_be_visited)
                    else:
                        #print(visited[1],visited[0][0],"????##")
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
#print(new_reverse_products)

#print(products[("X24","A1sg")])
#print(new_products[("X24","A1sg")])
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

#print(cnf_products)


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


with open("CNF_products.txt", "w", encoding = "utf-8-sig") as filename:
    filename.write(text)


other_text = ""
for k,v in cnf_lexical_rules.items():
    
    for lhs in v:
        if(type(lhs) == str):
            other_text = other_text + lhs+" -> " + k + "\n"
            
            
        else:
            other_text = other_text + lhs[0]+" -> " + k + "\n"
              
#print(cnf_lexical_rules["-Im"])
with open("CNF_lexical_rules.txt", "w", encoding = "utf-8-sig") as filename:
    filename.write(other_text)
    
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
    #print(k,v)

#print(reverse_cnf_products)

class Node():
    def __init__(self, content, children = None, parent = None):
        self.content = content
        self.children = children
        self.parent = parent
        self.bracket_notation = ""
        self.intermediate = None
        
        
def create_duplicate_node(node):
    copy_node = Node(node.content[:])
    if(node.children == None):
        #print(node.content, "pasdpads")
        copy_node.children = None
    else:
        copy_node.children = []
        for child in node.children:
            copy_node.children.append(create_duplicate_node(child))
        #copy_node.children = node.children.copy()
    copy_node.bracket_notation = node.bracket_notation[:]
    copy_node.intermediate = node.intermediate
    
    return copy_node
"""
def copy(node):
    #print(node.content)
    if(node == None):
        return 
    #print(node.content)
    if (node.children == None):
        copy_node = create_duplicate_node(node)
        #print(node.content, node.intermediate)
        return
    
    for child in node.children:
        print_tree(child)
        
    
    #print(node.content, node.intermediate)
    return 
"""
class Grammar():
    def __init__(self, products, lexical_rules):
        self.products = products
        self.lexical_rules = lexical_rules

def print_tree(node):
    #print(node.content)
    if(node == None):
        return 
    #print(node.content)
    if (node.children == None):
        node.bracket_notation = "["+node.content+"]"
        #print(node.content, node.intermediate,"###")
        return
    node.bracket_notation = "["+node.content
    for child in node.children:
        print_tree(child)
        node.bracket_notation += child.bracket_notation
    node.bracket_notation += "]"
    
    #print(node.content, node.intermediate,"###")
    return 
def turn_into_cfg_tree_step_1(node):
    if(node == None):
        return 
    #if(node.left_child == None and node.right_child == None):
    #   print(node.content)
    #   return node
    
    #else:
    #    print(node.content)
    #    left_child = print_tree(node.left_child)
    #    right_child = print_tree(node.right_child)
    #print(node.content)
    if (node.children == None):
        #print(node.content, node.intermediate)
        return
    
    if(node.intermediate != None):
        
        #print(node.content, node.intermediate)
        for ara in node.intermediate:
            temp = Node(ara)
            temp.children = node.children.copy()
            for temp_child in temp.children:
                temp_child.parent = temp
            temp.parent = node
            node.children = [temp]
            #print(temp.content)
            #print(node.content, node.intermediate)
            node = temp
    for child in node.children:
        turn_into_cfg_tree_step_1(child)
    #print(node.content, node.intermediate)
    return 

def turn_into_cfg_tree_step_2(node):
    if(node == None):
        return 
    if (node.children == None):
        #print(node.content, node.intermediate)
        return
    
    if(node.content.startswith("X")):
        #print(node.content,"ömöm")
        
        actual_rule = reverse_cnf_products[node.content]
        Parent = node.parent
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
    #print(node.content, node.intermediate)
    return 

def clear_bracket_notation(node):
    #print(node.content)
    if(node == None):
        return 
    #if(node.left_child == None and node.right_child == None):
    #   print(node.content)
    #   return node
    
    #else:
    #    print(node.content)
    #    left_child = print_tree(node.left_child)
    #    right_child = print_tree(node.right_child)
    #print(node.content)
    if (node.children == None):
        node.bracket_notation = ""
        #print(node.content, node.intermediate)
        return
    
    for child in node.children:
        clear_bracket_notation(child)
    node.bracket_notation = ""
    
    #print(node.content, node.intermediate)
    return 

def traverse_tree(node):
    #print(node.content)
    if(node == None):
        return 
    #if(node.left_child == None and node.right_child == None):
    #   print(node.content)
    #   return node
    
    #else:
    #    print(node.content)
    #    left_child = print_tree(node.left_child)
    #    right_child = print_tree(node.right_child)
    #print(node.content)
    if (node.children == None):
        #node.bracket_notation = ""
       # print(node, node.content)   
        #print(node.content, node.intermediate)
        return
    
    for child in node.children:
        traverse_tree(child)
#    node.bracket_notation = ""
    #print(node, node.content)   
    #print(node.content, node.intermediate)
    return 
    
def cky_parse(grammar, words):
    table = [[[] for i in range(len(words)+1)] for j in range(len(words)+1)]
    for i in range(len(words)):
        
        possiblities = grammar.lexical_rules[words[i]]
        #print(possiblities)
        primary_node = Node(words[i])
        for pos in possiblities:
            copy_primary_node = create_duplicate_node(primary_node)
            #print(copy_primary_node)
            if(type(pos) == str):
                node = Node(pos)
                node.children = [copy_primary_node]
                copy_primary_node.parent = node
            else:
                node = Node(pos[0])
                node.children = [copy_primary_node]
                copy_primary_node.parent = node
                node.intermediate = pos[1]
            #table[i][i+1].append((pos, None, None))
            table[i][i+1].append(node)
            #print(node,"etretrret")
            
        #for node in table[i][i+1]:
            #print(node.content)
            #print(node.intermediate)
            #for child in node.children:
            #    print(child.content)
    for j in range(2,len(words)+1):
        for i in range(j-2,-1,-1):
            for k in range(i+1,j):
                for l in range(len(table[i][k])):
                    for m in range(len(table[k][j])):
                        #print(table[i][k][l].content, table[k][j][m].content, i,k,j)
                        if((table[i][k][l].content, table[k][j][m].content) in grammar.products):
                            derivations = grammar.products[(table[i][k][l].content, table[k][j][m].content)]
                           # print(derivations, i,k,j)
                            for derivation in derivations:
                                #print(table[i][k][l].content, table[k][j][m].content, i,k,j)
                                if(type(derivation) == str):
                                   # print(table[i][k][l].content, table[k][j][m].content, i,k,j, "??", derivation)
                                    node = Node(derivation)
                                    
                                        
                                    copy_node_1 = create_duplicate_node(table[i][k][l])
                                    copy_node_2 = create_duplicate_node(table[k][j][m])
                                   # if(derivation == "S" and table[k][j][m].content == "PRED"):
                                       # print(copy_node_1, "xdxd", node)
                                   # if(table[i][k][l].content == "X24" and table[k][j][m].content == "A1sg"):
                                        #print(copy_node_1, copy_node_2, table[i][k][l], table[k][j][m], derivation)
                                    #node.children = [table[i][k][l], table[k][j][m]]
                                    node.children = [copy_node_1, copy_node_2]
                                    #print(copy_node_1.children,l,m, "qweqwqew")
                                    #table[i][k][l].parent = node
                                    #table[k][j][m].parent = node
                                    copy_node_1.parent = node
                                    copy_node_2.parent = node
                                    table[i][j].append(node)            
                                else:
                                   # print(table[i][k][l].content, table[k][j][m].content, i,k,j, derivation)
                                    node = Node(derivation[0])
                                    copy_node_1 = create_duplicate_node(table[i][k][l])
                                    copy_node_2 = create_duplicate_node(table[k][j][m])
                                    #if(table[k][j][m].content == "PRED"):
                                      #  print(copy_node_1, "xddd")
                                    #if(table[i][k][l].content == "X24" and table[k][j][m].content == "A1sg"):
                                       # print(copy_node_1, copy_node_2, table[i][k][l], table[k][j][m], derivation, "asd")
                                    #node.children = [table[i][k][l], table[k][j][m]]
                                    node.children = [copy_node_1, copy_node_2]
                                    node.intermediate = derivation[1]
                                    #table[i][k][l].parent = node
                                    #table[k][j][m].parent = node
                                    copy_node_1.parent = node
                                    copy_node_2.parent = node
                                    table[i][j].append(node) 
    
    return table

def make_tree(table):
    possible_parses = []
    final_cell = table[0][-1]
    #for node in final_cell:
        #print(node.content,"*****")
    trees = []
    for node in final_cell:
        if node.content == "S":
            trees.append(node)
            #copy_node = create_duplicate_node(node)
            #clear_bracket_notation(node)
            #clear_bracket_notation(copy_node)
            #print("xd")
            #print_tree(node)
            #print(node.bracket_notation, "asdsd")
            
            turn_into_cfg_tree_step_1(node)
            #turn_into_cfg_tree_step_1(copy_node)
            print_tree(node)
            #print(node.bracket_notation, "asdasd")
            #print(node.bracket_notation,"\\\\")
            #print_tree(copy_node)
            #print(copy_node.bracket_notation, "**")
            if("X" in node.bracket_notation):
                boolean = True
            else:
                boolean = False
            #if("X" in copy_node.bracket_notation):
            #    boolean = True
            #else:
            #    boolean = False
            counter = 0
            while(boolean == True and counter < 5):
                #print("asd")
                print_tree(node)
                #print(node.bracket_notation,"wewer")
                turn_into_cfg_tree_step_2(node)
                print_tree(node)
                #print(node.bracket_notation,"arewe")
                #print("X"  in node.bracket_notation)
                if("X" in node.bracket_notation):
                    boolean = True
                    clear_bracket_notation(node)
                else:
                    #print("lol")
                    boolean = False
                #print(boolean)
                counter += 1
            #turn_into_cfg_tree_step_2(node)
            #print_tree(node)
            #print(node.bracket_notation,"arewe")
            #turn_into_cfg_tree_step_2(node)
            #print_tree(node)
            #print(node.bracket_notation,"arewe")
            #while(boolean == True):
            #    print("asd")
            #    turn_into_cfg_tree_step_2(copy_node)
            #    print_tree(copy_node)
            #    if("X" in bracket_notation):
             #       boolean = True
            #    else:
             #       boolean = False
            #
           # possible_parses.append(copy_node.bracket_notation)
            possible_parses.append(node.bracket_notation)
            traverse_tree(node)
    #for children in childrens:
    #    for child in children:
    #        print(child.children, child.content)
    #print(childrens)
    
    return possible_parses, trees
"""
def check_agreement(node):
    #print(node.content)
    if(node == None):
        return True
    #if(node.left_child == None and node.right_child == None):
    #   print(node.content)
    #   return node
    
    #else:
    #    print(node.content)
    #    left_child = print_tree(node.left_child)
    #    right_child = print_tree(node.right_child)
    #print(node.content)
    if (node.children == None):
        #node.bracket_notation = ""
       # print(node, node.content)   
        #print(node.content, node.intermediate)
        return True
    
    for child in node.children:
        if(check_agreement(child) == False):
            return False
    
    for child in node.children
#    node.bracket_notation = ""
    #print(node, node.content)   
    #print(node.content, node.intermediate)
    return 
"""
#lexical_rules = {"dün": ["Adv","ADVP"], "al": ["Verb"], "-dI": ["Past"], "-m": ["A1sg"] }
#products = {("Verb","Past"): ["PRED"], ("PRED", "A1sg"): ["PRED"], ("ADVP", "PRED"): ["S"]}
grammar = Grammar(cnf_products, cnf_lexical_rules)

words = ["dün", "arkadaş","-Im", "-yA", "bir", "hediye","al","-dI", "-m"]
node = Node("xd")
node_2 = Node("asd")
node.intermediate = ["asd"]
node.children = [node_2]
copy_node = create_duplicate_node(node)
node.intermediate = ["bnndf"]
#print(node.children, copy_node.children, "asdadwerwer")
#print(node.intermediate, copy_node.intermediate, "asdadwerwer")
table = cky_parse(grammar,words)
parses,trees = make_tree(table)
#print(parses[0])
#print(parses[1])
if len(parses) != 0:
    for parse in parses:
        print(parse)
print(len(parses))