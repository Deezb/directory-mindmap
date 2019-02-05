import easygui
from pathlib import Path
import os

class TrieNode(object):
    def __init__(self, dirOrFile: str):
        self.baseDir = dirOrFile
        self.dirOrFile = dirOrFile
        self.children = []
        self.word_finished = False
        self.counter = 1


def colour_map(argu):
    """

    :param argu: string, the filename to examine for colour
    :return: tuple( node colour , node background colour)
    """

    COLOUR_MAP = {
        'xlsx' : ("#33ff33", "#4f844e"),
        'xls' : ("#33ff33", "#4f844e"),
        'docx' : ("#33ff33", "#4c82ce"),
        'doc' : ("#33ff33", "#4c82ce"),
        'dwg' : ("#33ff33", "#bcb662"),
        'pdf' : ("#33ff33", "#ea6464"),
        'jpg': ("#33ff33", "#d06df2"),
        'png': ("#33ff33", "#b058ce"),
        'js': ("#33ff33", "#891876"),
        'html': ("#33ff33", "#891876"),
        'css': ("#33ff33", "#891876"),
        'mp4': ("#33ff33", "#777777"),
        'mpg': ("#33ff33", "#777777"),
        'avi': ("#33ff33", "#777777"),
        'mpeg': ("#33ff33", "#777777"),
        'nef': ("#33ff33", "#777777"),
        'gif': ("#33ff33", "#777777"),
    }
    colours = COLOUR_MAP.get(argu.split('.')[-1], ("#33ff33", "#777777"))
    return colours

def add(root, word: str):
    node = root
    for dirOrFile in word._parts:
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


def print_children(WholeText, WholeTextEnd, root, path):
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
    newText = """<node TEXT="{0}" """.format((root.dirOrFile.replace("&", "...")))

    if root.children:
        # if the root is a directory
        WholeText = WholeText + newText
        WholeText += ">\n"
        for subroot in root.children:
            WholeText, WholeTextEnd = print_children(WholeText, WholeTextEnd, subroot, Path(path, subroot.dirOrFile))
        WholeText += "</node>\n"
    else:
        # if the root is a file

        WholeText = WholeText + newText
        colours = colour_map(root.dirOrFile)
        WholeText += 'COLOR="{0}" BACKGROUND_COLOR="{1}"'.format(colours[0], colours[1])
        link = ' LINK="{link}"/>\n'.format(link=path)
        link = link.replace("&", "&amp;")
        WholeText += link

    return WholeText, WholeTextEnd


if __name__ == "__main__":
    filename1 = easygui.diropenbox()
    fsss = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(filename1):
        for file in f:
            fsss.append(Path(r, file))
    root = TrieNode("")
    WholeText = """<map version = "1.0.1" >
                    <node CREATED="1548918823219" ID="ID_1805243291" MODIFIED="1548918823219" TEXT="Directory Map">"""
    WholeTextEnd = """</node>
        </map>"""

    for directory in fsss:
        add(root, directory)


    #while the root has children step through the children and add them to the text
    countec = root.counter

    if countec > 0:
        WholeText, WholeTextEnd=print_children(WholeText, WholeTextEnd, root, root.dirOrFile)
    print(WholeText, WholeTextEnd)
    with open(r"C:\DavidB\MindMaps\first.mm", 'w') as fh:
        fh.write(WholeText)
        fh.write(WholeTextEnd)
