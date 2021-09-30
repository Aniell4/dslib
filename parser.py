import os

s = " " * 4
for File in os.listdir('structs'):
    if '.txt' in File:
        with open('structs/'+File) as F:
            Head, *Fields = [Ln.strip().split('\t') for Ln in F.readlines()]
        Object = File.split('.')[0]
        with open('structs/'+Object+'.py', 'w') as F:
            F.write(f"class {Object.capitalize()}:\n")
            F.write(s + f"def __init__(s, d):\n")
            for Name, Type, Description in Fields:
                Name = Name.replace('*', '').replace('?', '')
                F.write(s*2 + f"s.__{Name} = d.get('{Name}', None)\n")
            for Name, Type, Description in Fields:
                Name = Name.replace('*', '').replace('?', '')
                F.write(s + f"@property\n")
                F.write(s + f"def {Name}(s):\n")
                F.write(s*2 + f"'''{Description.capitalize()}'''\n")
                F.write(s*2 + f"return s.__{Name}\n")
                F.write(s + f"@{Name}.setter\n")
                F.write(s + f"def {Name}(s, val):\n")
                F.write(s*2 + f"s.__{Name} = val\n")

        
    
