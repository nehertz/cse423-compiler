# FIXME: Printing out a bunch of backslashes
# FIXME: Grammar not conducive for easy tree creation

class Node:
    def __init__(self,children=None,leaf=None):
        if children:
            # self.children = []
            if (isinstance(children, list) is False):
                # Ensure children is a list
                self.children = [children]
            else:
                self.children = children
        else:
            self.children = []
        if leaf:
            self.leaf = leaf.replace('\\', '')
        else:
            self.leaf = ''


    def print(self):
        if not self.children:
            # There are no children
            print("leaf if {0}".format(self.leaf))
            # return '{}'.format(self.leaf)

        else:
            # print("leaf: {0}".format(self.leaf))
            # print("children: {0}".format([str(child) for child in self.children]))
            print("else: {0}".format(self.leaf))
            for child in self.children:
                child.print()
            # return "{0} {1}".format(self.leaf, [str(child) for child in self.children])
            
    def __str__(self):
        if not self.children:
            return self.leaf
        else:
            return " "