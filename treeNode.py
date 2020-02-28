class Node:
    def __init__(self,children=None,leaf=None):
        if children:
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
    def __str__(self):
        if not self.children:
            # There are no children
            return '{}'.format(self.leaf)
        else:
            return '{} {}'.format(self.leaf, [str(child) for child in self.children])
