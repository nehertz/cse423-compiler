class Node:
    def __init__(self,children=None,leaf=None):
        if children:
            self.children = children
        else:
            self.children = [ ]
        self.leaf = leaf
    #def __repr__(self): 
        #return '%s %s' % (self.leaf,self.children)