s = s.strip()  # s is the input as a string

from collections import defaultdict
from re import compile, findall

ELEMENT_PATTERN = compile(r"[A-Z][a-z]?")
CallibrationTable = dict[str, dict[str, int]]
Molecule = dict[str, int]

def callibrate(elements: CallibrationTable, molecule: Molecule):
    new_molecule = defaultdict(int)
    for element, element_count in molecule.items():
        for product, product_count in elements[element].items():
            new_molecule[product] += product_count * element_count

elements_string, molecule_string = s.split('\n\n')

elements = {}
for e in elements_string.splitlines():
    element, product_string = e.split(" => ")
    products = set(findall(ELEMENT_PATTERN, product_string))

    elements[element] = {}
    for product in products:
        elements[element][product] = product_string.count(product)

molecule = defaultdict(int)
for element in findall(ELEMENT_PATTERN, molecule_string):
    molecule[element] += 1




def get_possible(elements, molecule_string):
    products = set()

    for i, element in enumerate(molecule_string):
        if element.islower():
            continue

        if i + 1 < len(molecule_string) and (char2:=molecule_string[i+1]).islower():
            element += char2
            
        for product_string in elements[element]:
            products.add(molecule_string[:i] + product_string + molecule_string[i + len(element):])
    
    return products