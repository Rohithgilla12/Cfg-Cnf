from itertools import product
from itertools import islice

def nth_index(iterable, value, n):
    matches = (idx for idx, val in enumerate(iterable) if val == value)
    return next(islice(matches, n-1, n), None)

def filler(word, from_char, to_char):
    options = [(c,) if c != from_char else (from_char, to_char) for c in word]
    return (''.join(o) for o in product(*options))

productions=[]
replacements=[]
unit_productions=[]

with open('cfg.txt') as cfg:
    for rule in cfg:
        check=0
        lhs=rule.split(':')[0]
        rhs=rule.split(':')[1]
        for i in range(len(productions)):
            if lhs==productions[i][0] :
                productions[i].append(rhs.replace('\n',''))
                check=1
        if check==1:
            pass
        else:
            productions.append([rule.split(':')[0],rule.split(':')[1].replace('\n','')])

if any("S" in s for s in productions):
    productions.append(["S'","S"])

null_productions=[]
for rule in productions:
    if 'e' in ''.join(rule[1:]):
        null_productions.append(rule[0])

new_productions=[]
while(len(null_productions)>=1):
    target=null_productions[0]
    for rule in productions:
        for variable in rule:
            if target in variable and rule.index(variable)!=0:
                print(variable)
                temp=rule[:]
                temp2=list(filler(variable,target,''))
                temp2.pop(0)
                temp.extend(temp2)
                new_productions.append(temp)
                if(len(variable)==1):
                    null_productions.append(rule[0])
    null_productions.pop(0)

for rule in new_productions:
    target=rule[0]
    main_index=new_productions.index(rule)
    #print("mainindex",main_index)
    for j in range(len(new_productions)):
        if(new_productions[j][0]==target and j!=main_index and j>main_index):
            temp=list(set(new_productions[j]).union(set(new_productions[main_index])))
            temp.insert(0,target)
            new_productions[j]=temp
            print(new_productions)
            new_productions.pop(main_index)


for rule in new_productions:
    target=rule[0]
    for i in range(len(productions)):
        if target==productions[i][0]:
            productions[i]=rule


for rule in productions:
    for j in range(1,len(rule)):
        if(rule[j]=='e'):
            rule.pop(rule.index('e'))
            
for rule in productions:
    for j in range(1,len(rule)):
        if(rule[j]==''):
            rule.pop(rule.index(''))            

for rule in productions:
    for j in range(1,len(rule)):
        try:
            if(rule[0]==rule[j]):
                rule.pop(nth_index(rule,rule[0],2))
        except:
            pass

for rule in productions:
    for j in range(1,len(rule)):
        if(len(rule[j])==1 and rule[j].isupper()):
            unit_productions.append([rule[0],rule[j]])

for rule in unit_productions:
    target=rule[-1]
    for i in range(len(productions)):
        if target==productions[i][0]:
            print(rule[0],productions[i][1:])
            for j in productions:
                for k in range(len(j)):
                    if j[k]==rule[0]:
                        j.pop(j.index(target))
                        j.extend(productions[i][1:])

for rule in productions:
    for variable in rule:
        if sum(1 for c in variable if c.isupper()) >2 :
            replacements.append(variable)

replacements=list(set(replacements))
job="ASA"
temp=job[:2]
for rule in productions:
    for variable in rule:
        if sum(1 for c in variable if c.isupper()) >2 :
            rule[rule.index(variable)]=variable.replace(temp,"X")
productions.append(["X","AS"])
print(productions)
with open('cnf.txt','w') as cnf:
    for rule in productions:
        for j in range(1,len(rule)):
            cnf.writelines(rule[0]+":"+rule[j]+'\n')