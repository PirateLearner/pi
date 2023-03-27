import xml.etree.ElementTree as ET


COMPARE_KEY_X = 1
COMPARE_KEY_Y = 2
COMPARE_KEY_WIDTH = 3
COMPARE_KEY_HEIGHT = 4
COMPARE_KEY_ROW = 5
COMPARE_KEY_COLUMN = 6

class HtmlTree:
    def __init__(self):
        self.root = ET.Element('div')
        self.root.set('class', 'container_main')
        self.root.set('name', 'main')
        self.tree = ET.ElementTree(self.root)
        self.current_node = self.root
    def add_node(self, node, parent=None):
        if parent:
            parent.append(node)
        else:
            self.root.append(node)

    def create_node(self,node_name, parent=None):
        self.current_node = ET.SubElement(parent,str(node_name))
        return self.current_node

    def add_attribute(self,node,**kwargs):
        
        for k,v in kwargs.items():
            node.set(k,v)
    
    def add_text(self,node,text):
        node.text = str(text)
        

html = HtmlTree()


class plugins:
    def __init__(self, left,top,width,height):
        self.x = left
        self.y = top
        self.width = width
        self.height = height
        self.option  = {COMPARE_KEY_X: self.compare_x,
                        COMPARE_KEY_Y: self.compare_y,
                        COMPARE_KEY_WIDTH: self.compare_width,
                        COMPARE_KEY_HEIGHT: self.compare_height,
                        COMPARE_KEY_ROW: self.compare_row,
                        COMPARE_KEY_COLUMN: self.compare_column
                        }
    
    def is_less(self,obj):
        if(self.x < obj.x and self.y < obj.y):
            return True
        else:
            return False
    def print_node(self):
        print(("( "+ str(self.x) + " - "+ str(self.y) +", "+ str(self.width) +", "+ str(self.height) + ")"))
    
    def node_str(self):
        return str("( "+ str(self.x) + " - "+ str(self.y) +", "+ str(self.width) +", "+ str(self.height) + ")")
    
    def compare(self,obj,key=COMPARE_KEY_X):
        return self.option[key](obj)
    
    def compare_x(self,obj):
        if self.x > obj.x:
            return 1
        elif obj.x > self.x:
            return -1
        else:
            return 0

    def compare_y(self,obj):
        if self.y > obj.y:
            return 1
        elif obj.y > self.y:
            return -1
        else:
            return 0

    def compare_width(self,obj):
        if self.width > obj.width:
            return 1
        elif obj.width > self.width:
            return -1
        else:
            return 0

    def compare_height(self,obj):
        if self.height > obj.height:
            return 1
        elif obj.height > self.height:
            return -1
        else:
            return 0
        
    def compare_row(self,obj):
        if self.x > obj.x:
            if self.y > obj.y:
                return 1
            elif self.y < obj.y:
                return -1
            else:
                return 1
        elif self.x < obj.x:
            if self.y < obj.y:
                return -1
            elif self.y > obj.y:
                return 1
            else:
                return -1
        else:
            if self.y < obj.y:
                return -1
            elif self.y > obj.y:
                return 1
            else:
                return 0

    def compare_column(self,obj):
        if self.y > obj.y:
            if self.x > obj.x:
                return 1
            elif self.x < obj.x:
                return -1
            else:
                return 1
        elif self.y < obj.y:
            if self.x < obj.x:
                return -1
            elif self.x > obj.x:
                return 1
            else:
                return -1
        else:
            if self.x < obj.x:
                return -1
            elif self.x > obj.x:
                return 1
            else:
                return 0
            


def insert_sort(obj_list,key):
    for i in range(len(obj_list)):
        for j in range(i,0,-1):
            if obj_list[j].compare(obj_list[j-1],key) <= 0:
                tmp = obj_list[j-1]
                obj_list[j-1] = obj_list[j]
                obj_list[j] = tmp
            else:
                break
    
    return obj_list
    

def create_row(obj_list,root):
    """
    1. Pop first object from the list.
    2. Set MAX_HEIGHT to obj.y + obj.height
    3. for all other objects do following:
        a. if obj.y  < MAX_HEIGHT the add it to temp list and pop it from original list.
        b. if obj.y + obj.height > MAX_HEIGHT then change it to obj.y + obj.height.
    4. Open the ROW div.
    5. Call the create_column(temp_list).
    6. close the ROW div 
    """
    if len(obj_list) == 0:
        return
    
    #sort the list accordingly
    obj_list = insert_sort(obj_list,COMPARE_KEY_ROW)
    

#     print "create_row called with list"
#     
#     for elem in obj_list:
#         elem.print_node()

    
    # Pop first element and set max HEIGHT
    obj = obj_list.pop(0)
    MAX_HEIGHT = obj.y + obj.height
    row_list = [obj]
    

    # create the row list to be passed to the column function 

    i = 0
    n = len(obj_list)
    while i < n:
        element = obj_list[i]
        if element.y < MAX_HEIGHT:
            row_list.append(element)
            if element.y + element.height > MAX_HEIGHT:
                MAX_HEIGHT = element.y + element.height
            del obj_list[i]
            n = n - 1
        else:
            i = i + 1
    
    tmp = html.create_node('div',root)
    kwargs = {"name":'row',"class":'ROW'}
    html.add_attribute(tmp,**kwargs)
#     print("<div class='ROW'>")
    create_column(row_list,tmp)
#     print("</div> !< ROW !>")

    if len(obj_list) == 0:
        return
    create_row(obj_list,root)

def create_column(obj_list,root):
    """
    1. Pop first object from the list.
    2. Set MAX_WIDTH to obj.x + obj.width
    3. for all other objects do following:
        a. if obj.x  < MAX_WIDTH the add it to temp list and pop it from original list.
        b. if obj.x + obj.width > MAX_WIDTH then change it to obj.x + obj.width.
    4. Open the COLUMN div.
    5. Call the create_row(temp_list).
    6. close the COLUMN div 
    """
    if len(obj_list) == 0:
        return
    #sort the list accordingly
    obj_list = insert_sort(obj_list,COMPARE_KEY_COLUMN)
    
#     print "create_column called with list"
#     
#     for elem in obj_list:
#         elem.print_node()
    
    # Pop first element and set max HEIGHT
    obj = obj_list.pop(0)
    MAX_WIDTH = obj.x + obj.width
    column_list = [obj]

    if len(obj_list) == 0:
        tmp = html.create_node('div',root)
        kwargs = {"name":'column',"class":'COLUMN'}
        html.add_attribute(tmp,**kwargs)
        html.add_text(tmp,obj.node_str())
        
#         print("<div class='COLUMN'>")
#         obj.print_node()
#         print("</div> !< COLUMN !>")
        return
    
    # create the column list to be passed to the row function 
    i = 0
    n = len(obj_list)
    while i < n:
        element = obj_list[i]
        if element.x < MAX_WIDTH:
            column_list.append(element)
            if element.x + element.width > MAX_WIDTH:
                MAX_WIDTH = element.x + element.width
            del obj_list[i]
            n = n - 1
        else:
            i = i + 1

    # pass to create row only if it contains more than 1 items
    tmp = html.create_node('div',root)
    kwargs = {"name":'column',"class":'COLUMN'}
    html.add_attribute(tmp,**kwargs)
#     print("<div class='COLUMN'>")
    if len(column_list) > 1:
        create_row(column_list,tmp)
    else:
        html.add_text(tmp,obj.node_str())
#         column_list[0].print_node()
#     print("</div> !< COLUMN !>")
    create_column(obj_list,root)
   
def create_array(object_list):
#     obj_list = [plugins(0,0,10,15),plugins(12,17,5,10),plugins(20,30,8,12),plugins(0,45,10,15),plugins(12,45,10,15),plugins(24,45,5,10)]
#     obj_list = [plugins(0,0,10,15),plugins(12,0,5,10),plugins(20,0,8,12)]
 
#     for elem in  obj_list:
#         elem.print_node() 
#     print "after sorting the array in row"
#     obj_list = insert_sort(obj_list, COMPARE_KEY_ROW)
#     for elem in  obj_list:
#         elem.print_node() 
#   
#     print "after sorting the array in column"
#     obj_list = insert_sort(obj_list, COMPARE_KEY_COLUMN)
#     for elem in  obj_list:
#         elem.print_node() 
     
    create_row(object_list,html.root)
    
    print("\n\n\n Printing the Tree \n\n\n")
    
    ET.dump(html.root)
    
if __name__ == "__main__":
    create_array()