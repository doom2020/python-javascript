class Node(object):
    def __init__(self, data):
        self.data = data
        self.lchild = None
        self.rchild = None

    
class Btree(object):
    def front_order(self, root):
        """
        前序遍历
        """
        if root is None:
            return
        print(root.data, end=',')
        if root.lchild:
            self.front_order(root.lchild)
        if root.rchild:
            self.front_order(root.rchild)

    def mid_order(self, root):
        """
        中序遍历
        """
        if root is None:
            return
        if root.lchild:
            self.mid_order(root.lchild)
        print(root.data, end=',')
        if root.rchild:
            self.mid_order(root.rchild)

    def tail_order(self, root):
        """
        后续遍历
        """
        if root is None:
            return
        if root.lchild:
            self.tail_order(root.lchild)
        if root.rchild:
            self.tail_order(root.rchild)
        print(root.data, end=',')

    def tral_order(self, root):
        """
        广度遍历
        """
        if root is None:
            return
        queue = [root]
        while queue:
            result = []
            for item in queue:
                print(item.data, end=',')
                if item.lchild:
                    result.append(item.lchild)
                if item.rchild:
                    result.append(item.rchild)
            queue = result

    def tree_is_same(self, root1, root2):
        """
        比较两棵树是否相同
        """
        if root1 is None and root2 is None:
            return True
        elif root1 and root2: 
            return root1.data == root2.data and self.tree_is_same(root1.lchild, root2.lchild) and self.tree_is_same(root1.rchild, root2.rchild)
        else:
            return False

    def tree_max_deepth(self, root):
        """
        树的最大深度
        """
        if root is None:
            return 0
        return max(self.tree_max_deepth(root.lchild), self.tree_max_deepth(root.rchild)) + 1


if __name__ == "__main__":
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)
    node5 = Node(5)
    node6 = Node(6)
    node7 = Node(7)
    node1.lchild = node2
    node1.rchild = node3
    node2.lchild = node4
    node2.rchild = node5
    node3.lchild = node6
    node3.rchild = node7
    b_tree = Btree()
    b_tree.front_order(node1)
    print('*******************')
    b_tree.mid_order(node1)
    print('*******************')
    b_tree.tail_order(node1)
    print('*******************')
    b_tree.tral_order(node1)
    deepth = b_tree.tree_max_deepth(node1)
    print(deepth)



        