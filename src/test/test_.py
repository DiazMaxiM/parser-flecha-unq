import pytest
from parser import Parser
import glob
import json
import os
from src.ast.nodos import jsonConfig

def read_file(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def get_test_files(subfolder, test_num, ext='input', json_fmt=False):
    filepath = glob.glob(f"{os.getcwd()}/**/{subfolder}/test{test_num}.{ext}", recursive=True)[0]
    input_data = read_file(filepath)
    expected_path = filepath[:-len(ext)] + 'expected'
    expected_data = json.dumps(json.loads(read_file(expected_path)), **jsonConfig) if json_fmt else read_file(expected_path)
    return input_data, expected_data

test_names = [
    'Programa vacio', 'Numeros', 'Variables', 'Constructores', 'Caracteres', 'Estructuras', 'Cadenas', 
    'Si', 'Caso', 'Aplicar', 'Declaraciones locales', 'Funciones anonimas', 'Secuencias', 
    'Anidacion de estructuras de control', 'Operadores', 'Asociatividad', 'Anidacion Operadores/Aplicar', 
    'Precedencia', 'Algun programa',
]

@pytest.mark.parametrize('n, desc', [(f"{i:02}", name) for i, name in enumerate(test_names)])
def test_files(n, desc):
    p = Parser()
    program, expected = get_test_files("data*", n, json_fmt=True)
    assert str(p.parse(program)) == expected