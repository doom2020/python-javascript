"""
简单的单链表
循环链表: 尾部(next)指向首部
双向链表: 相互之间指向
双向循环链表
"""


class Node(object):
    def __init__(self, data):
        self.data = data
        self.next = None

class SimpleLink(object):
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def lenght(self):
        """
        链表的长度
        """
        size = 0
        if self.is_empty():
            return size
        current = self.head
        while current is not None:
            size += 1
            current = current.next
        return size

    def iter_item(self):
        """
        遍历链表
        """
        current = self.head
        while current is not None:
            data = current.data
            yield data

    def head_insert(self, val):
        """
        头部插入
        """
        node = Node(data=val)
        # 空链表
        if self.is_empty():
            self.head = node
        # 非空链表
        else:
            node.next = self.head
            self.head = node
    
    def tail_inser(self, val):
        """
        尾部插入
        """
        node = Node(data=val)
        # 空链表
        if self.is_empty():
            self.head = node
        # 非空链表
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node

    def insert(self, index, val):
        """
        指定位置插入
        """
        node = Node(val)
        cur = self.head
        for i in range(index):
            cur = cur.next
        node.next = cur.next
        cur.next = node
        
    def remove(self, val):
        """
        删除item
        """
        if self.is_empty():
            return
        cur = self.head
        while cur.data != val:
            pre = cur
            cur = cur.next
        pre.next = cur.next

    def find_item(self, data):
        """
        查询某个item
        """
        if self.is_empty():
            return False
        current = self.head
        while current is not None:
            if current.data == data:
                return True
            current = current.next
        return False


class CycleLink(object):
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def head_insert(self, val):
        node = Node(val)
        if self.is_empty():
            self.head = Node
        else:
            tail = None
            current = self.head
            while current.next != self.head:
                current = current.next
            tail = current
            tail.next = node
            node.next = self.head
            self.head = node

    def tail_insert(self, val):
        node = Node(val)
        if self.is_empty():
            self.head = Node
        else:
            tail = None
            current = self.head
            while current.next != self.head:
                current = current.next
            tail = current
            tail.next = node
            node.next = self.head

    def insert(self, index, val):
        node = Node(val)
        if self.is_empty():
            self.head = node
        else:
            current = self.head
            for i in range(index):
                current = current.next
            node.next = current.next
            current.next = node

    def remove(self, val):
        if self.is_empty():
            return
        current = self.head
        while current.data != val:
            pre = current
            current = current.next
        pre.next = current.next


class DoubleNode(object):
    def __init__(self, data):
        self.data = data
        self.next = None
        self.pre = None
    
class DoubleLink(object):
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def head_insert(self, val):
        node = DoubleNode(val)
        if self.is_empty():
            self.head = node
        else:
            node.next = self.head
            self.head.pre = node
            self.head = node

    def tail_insert(self, val):
        node = DoubleNode(val)
        if self.is_empty():
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node
            node.pre = current

    def insert(self, index, val):
        node = DoubleNode(val)
        if self.is_empty():
            self.head = node
        else:
            current = self.head
            for i in range(index):
                current = current.next
            current.next.pre = node
            node.next = current.next
            current.next = node
            node.pre = current

    def remove(self, val):
        current = self.head
        while current.data != val:
            current = current.next
        current.pre.next = current.next
        current.next.pre = current.pre

class DoubleCycleLink(object):
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None
    
    def head_insert(self, val):
        node = DoubleNode(val)
        if self.is_empty():
            self.head = node
        else:
            tail = None
            current = self.head
            while current.next != self.head:
                current = current.next
            tail = current
            node.next = self.head
            tail.next = node
            node.pre = tail
            self.head.pre = node
            self.head = node


    def tail_insert(self, val):
        node = DoubleNode(val)
        if self.is_empty():
            self.head = None
        else:
            tail = None
            current = self.head
            while current.next != self.head:
                current = current.next
            tail = current
            node.next = self.head
            self.head.pre = node
            tail.next = node
            node.pre = tail


    def insert(self, index, val):
        node = DoubleNode(val)
        if self.is_empty():
            self.head = node
        else:
            current = self.head
            for i in range(index):
                current = current.next
            current.next.pre = node
            node.next = current.next
            current.next = node
            node.pre = current

    def remove(self, val):
        if self.is_empty():
            return
        else:
            current = self.head
            while current.data != val:
                current = current.next
            current.pre.next = current.next
            current.next.pre = current.pre

        


if __name__ == "__main__":
    sl = SimpleLink()
    for i in range(10):
        sl.tail_inser(i)
    # for i in sl.iter_item():
    #     print(i)
    print(sl.lenght())
    print(sl.head.data)
    sl.head_insert(20)
    print(sl.head.data)
    print(sl.head.next.data)
    



