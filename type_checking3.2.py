# from ply_parser import st
from io import BytesIO
from io import StringIO
from skbio import read
from skbio.tree import TreeNode
from ply_parser import st
import re
import sys
import bitstring

class TypeChecking:
    def __init__(self, ast):
        self.treeString = ast.replace('"', '')
        self.tree = TreeNode.read(StringIO(self.treeString))
        self.numbersFloat = re.compile(r'\d+\.{1}\d+')
        self.numbersInt = re.compile(r'\d+')
        self.logicalExpr = re.compile(r'(\|\|)|(&&)|(\!)')
        self.compOps = re.compile(r'(==)|(\!=)|(>=)|(<=)')
        self.scope = 0
        self.funcName = ''


    def run(self):
        for node in self.tree.children:
            if (node.name == '='):
                node.children = self.variablesTC(node.children)
                continue 
            elif ('func-' in node.name):
                self.funcName = node.name.replace('func-', '')
                self.scope += 1
                node.children = self.functionsTC(node.children)
                continue 
            else:
                continue

        with open('ast.txt', mode='w', encoding='utf-8') as f:
            self.tree.write(f, format='newick')

        with open('ast.txt', mode='r', encoding='utf-8') as f:
            ast = f.readlines()

        return ast[0]

    def functionsTC(self, nodes):
        for node in nodes:
            if ('stmt' in node.name):
                node.children = self.checkStatement(node.children)
                continue 
        return nodes 
    
    def checkStatement(self, nodes):
        for node in nodes:
            if ('=' == node.name):
                node.children = self.variablesTC(node.children)
                continue 
            elif ('return' == node.name):
                node.children = self.returnTC(node.children)
                continue
        