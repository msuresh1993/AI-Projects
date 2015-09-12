class TreeNode(object):
    #this is a class to make tree nodes for ID3
    def __init__(self):
        self.attribute = None
        self.branches = {}
        self.decision = None
