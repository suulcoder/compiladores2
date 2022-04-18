import itertools
from pickle import NONE


class Leaf(object):
    """Leaf
    
    This Class is a node of three generated by 
    the regex in order to work with the direct 
    method

    Args:
        object (id): This must be a string, this
        is a nullable object that can be used to
        define the type of the Leaf. The following
        options are available:
        
        "star" = star or kleene node
        "concat" = concatenation node
        "or" = or node
        None = Leaf node, must be a numeric value
    """
    new_id = itertools.count()
        
    def __init__(self, _id, firstpos=None, lastpos=None, nullable=False, value=None, left=None, right=None):
        super(Leaf, self).__init__()
        self._id = _id
        self.firstpos = firstpos
        self.lastpos = lastpos
        self.followpos = []
        self.nullable = nullable
        self.value = value
        self.left = left
        self.right = right
        
    def getNullable(self):
        if(self.value=='*' and self.value=='ε'):
            self.nullable = True
        elif(self.value=='|'):
            self.nullable = self.right.nullable or self.left.nullable
        elif(self.value=='•'):
            self.nullable = self.right.nullable and self.left.nullable if (self.right and self.left) else True
        else:
            self.nullable = False
    
    def getFirstPos(self):
        if(self.value == 'ε'):
            self.firstpos = []
        elif(self.value=='*'):
            self.firstpos = self.right.firstpos 
        elif(self.right==None or self.left==None):
            self.firstpos = [self]
        elif(self.value=='|'):
            self.firstpos = self.right.firstpos + self.left.firstpos
        elif(self.value=='•'):
            self.firstpos =  self.right.firstpos + self.left.firstpos if self.left.nullable == True else self.left.firstpos
        elif(isinstance(self.id, int)):
            self.firstpos = [self]
        for n in self.firstpos:
            if(not isinstance(n.id, int)):
                self.firstpos.remove(n)
    
    def getLastPos(self):
        if(self.value == 'ε'):
            self.lastpos = []
        elif(self.right==None and self.left==None):
            self.lastpos = [self]
        elif(self.value=='*'):
            self.lastpos = self.right.lastpos
        elif(self.value=='|'):
            self.lastpos = self.right.lastpos + self.left.lastpos
        elif(self.value=='•'):
            self.lastpos =  self.right.lastpos + self.left.lastpos if self.right.nullable == True else self.right.lastpos
        elif(isinstance(self.id, int)):
            self.lastpos = [self]
        for n in self.lastpos:
            if(not isinstance(n.id, int)):
                self.firstpos.remove(n)
    
    def getFollowPos(self, nodes):
        if self.value == 'CONCATENATION':
            for lastpos_node in self.left.lastpos:
                list(filter(lambda x: x._id == lastpos_node, nodes))[0].followpos += self.right.firstpos
        elif self.value == 'KLEENE':
            for lastpos_node in self.lastpos:
                list(filter(lambda x: x._id == lastpos_node, nodes))[0].followpos += self.firstpos
            
        