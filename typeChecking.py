from ply_parser import st
from io import BytesIO
from io import StringIO
from skbio import read
from skbio.tree import TreeNode


def typeChecking(ast):
        f = StringIO(ast)
        tree = read(f, format="newick", into=TreeNode)
        f.close
        tree.ascii_art()

        