from typing import Tuple
import easygui
import os


class TrieNode(object):
    def __init__(self, dirOrFile: str):
        self.dirOrFile = dirOrFile
        self.children = []
        self.word_finished = False
        self.counter = 1


def add(root, word: str):
    node = root
    for dirOrFile in word.split("\\"):
        found_in_child = False
        # Search for the character in the children of the present `node`
        for child in node.children:
            if child.dirOrFile == dirOrFile:
                # We found it, increase the counter by 1 to keep track that another
                # word has it as well
                child.counter += 1
                # And point the node to the child that contains this char
                node = child
                found_in_child = True
                break
        # We did not find it so add a new chlid
        if not found_in_child:
            new_node = TrieNode(dirOrFile)
            node.children.append(new_node)
            # And then point node to the new child
            node = new_node
    # Everything finished. Mark it as the end of a word.
    node.word_finished = True


def find_prefix(root, prefix: str) -> Tuple[bool, int]:
    """
    Check and return tuple (1, 2)
      1. Boolean, does the current path already exist from previous files added
      2. If True, then how many files have been down this path
    """
    node = root
    # no
    if not root.children:
        return False, 0
    for dirOrFile in prefix:
        dir_or_file_not_found = True
        # Search through all the children of the present `node`
        for child in node.children:
            if child.dirOrFile == dirOrFile:
                # We found the directory or file existing in the child.
                dir_or_file_not_found = False
                # Assign node as the child containing the char and break
                node = child
                break
        # Return False anyway when we did not find a char.
        if dir_or_file_not_found:
            return False, 0

    return True, node.counter


def print_children(WholeText, WholeTextEnd, root):
    """
    Recursive function that adds to a string XML representation of the directory structure.
    :param WholeText: start of xml built from parent objects, being built recursively and depth first sequence traversal
    :param WholeTextEnd: End of xml, to be combined with WholeText when recursion is finished.
    :param root: Current node in the directory, each folder is a node, each file is a leaf.
    :return: return the modified string representation to include the part for this visit to the

    When a directory is encountered it adds
        <node POSITION="right" TEXT="<Dir_Name>">\n
            calls on each child print_children(root.child)
        </node>

    when a file is encountered it adds
        <node POSITION="right" TEXT="<File_Name>"/>\n
    """
    endText = ""
    newText = """<node POSITION="right" TEXT="{0}" """.format((root.dirOrFile.replace("&", "...")))

    if root.children:
        # if the root is a directory
        WholeText = WholeText + newText
        WholeText += ">\n"
        for i in root.children:
            WholeText, WholeTextEnd = print_children(WholeText, WholeTextEnd, i)
        WholeText += "</node>\n"
    else:
        # if the root is a file
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
