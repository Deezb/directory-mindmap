from typing import Tuple
import easygui
import os


class TrieNode(object):
    def __init__(self, title: str):
        self.title = title
        self.children = []
        self.word_finished = False
        self.counter = 1


def add(root, word: str):
    node = root
    for char in word.split("\\"):
        found_in_child = False
        # Search for the character in the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found it, increase the counter by 1 to keep track that another
                # word has it as well
                child.counter += 1
                # And point the node to the child that contains this char
                node = child
                found_in_child = True
                break
        # We did not find it so add a new chlid
        if not found_in_child:
            new_node = TrieNode(char)
            node.children.append(new_node)
            # And then point node to the new child
            node = new_node
    # Everything finished. Mark it as the end of a word.
    node.word_finished = True


def find_prefix(root, prefix: str) -> Tuple[bool, int]:
    """
    Check and return
      1. If the prefix exsists in any of the words we added so far
      2. If yes then how may words actually have the prefix
    """
    node = root
    # If the root node has no children, then return False.
    # Because it means we are trying to search in an empty trie
    if not root.children:
        return False, 0
    for char in prefix:
        char_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.char == char:
                # We found the char existing in the child.
                char_not_found = False
                # Assign node as the child containing the char and break
                node = child
                break
        # Return False anyway when we did not find a char.
        if char_not_found:
            return False, 0
    # Well, we are here means we have found the prefix. Return true to indicate that
    # And also the counter of the last node. This indicates how many words have this
    # prefix
    return True, node.counter


def print_children(WholeText, WholeTextEnd, root):
    endText = ""
    newText = """<node POSITION="right" TEXT="{0}" """.format((root.char.replace("&", "...")))

    if root.children:
        WholeText = WholeText + newText
        WholeText += ">\n"
        for i in root.children:
            WholeText, WholeTextEnd = print_children(WholeText, WholeTextEnd, i)
        WholeText += "</node>\n"
    else:
        WholeText = WholeText + newText
        WholeText += "/>\n"

    return WholeText, WholeTextEnd


if __name__ == "__main__":
    filename1 = easygui.diropenbox()
    fsss = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(filename1):
        for file in f:
            fsss.append(os.path.join(r, file))
    root = TrieNode('*')
    WholeText = """<map version = "1.0.1" >
                    <node CREATED="1548918823219" ID="ID_1805243291" MODIFIED="1548918823219" TEXT="New Mindmap">"""
    WholeTextEnd = """</node>
        </map>"""

    for directory in fsss:
        add(root, directory)


    #while the root has children step through the children and add them to the text
    countec = root.counter

    if countec > 0:
        WholeText, WholeTextEnd=print_children(WholeText, WholeTextEnd, root)
    print(WholeText, WholeTextEnd)
    with open(r"C:\DavidB\MindMaps\first.mm", 'w') as fh:
        fh.write(WholeText)
        fh.write(WholeTextEnd)
