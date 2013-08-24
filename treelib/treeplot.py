#!/usr/bin/python2
"""
treeplot.py
by Lars Otten <lotten@ics.uci.edu>, 2011

Python script that plots a labeled tree from a simple string
representation and outputs it to a SVG file. The output file name is
the same as the input with .svg attached.

The input file should follow this simple grammar:
  T = ( <label> T* )

For instance:
  ( 0 ( 1 ( 2 ) ( 3 ) ) )
corresponds to this tree:

  0
  |
  1
 / \
2   3

See more examples (and their output) in the example/ folder.

--------------------------
Licensed under MIT License

Copyright (c) 2011 by Lars Otten

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Sets the radius and horizontal/vertical node distance for plotting.
NODE_RADIUS = 20
NODE_DIST_X = 50
NODE_DIST_Y = 60
# Node fill color
NODE_FILL = "#b0b0b0"
# Line width for plotting
LINE_WIDTH = 2


import sys
from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *
from pysvg.builders import *


class TreePlotter:

    """Provides the tree plotting functionality through pySVG."""
    def __init__(self):
        self.indent = 0
        self.plot = svg()

        self.builder = ShapeBuilder()
        self.style_node = StyleBuilder()
        self.style_node.setFilling(NODE_FILL)
        self.style_node.setStroke("black")
        self.style_node.setStrokeWidth(LINE_WIDTH)

        self.style_text = StyleBuilder()
        self.style_text.setTextAnchor("middle")
        self.style_text.setDominantBaseline("central")

        self.style_line = StyleBuilder()
        self.style_line.setStroke("black")
        self.style_line.setStrokeWidth(LINE_WIDTH)

    def plotNode(self, tree, nid):
        """Adds a single node to the plot, incl. connection to parent."""
        # Compute node position

        node = tree[nid]
        pos_y = node.depth * NODE_DIST_Y
        pos_y += NODE_DIST_Y * 0.5
        pos_x = self.indent * NODE_DIST_X
        pos_x += node.width * NODE_DIST_X * 0.5
        node.pos_x = pos_x
        node.pos_y = pos_y

        # Actual node (circle)
        circle = self.builder.createCircle(pos_x, pos_y, NODE_RADIUS)
        circle.set_style(self.style_node.getStyle())
        self.plot.addElement(circle)

        # Node label
        T = text(node.tag, pos_x, pos_y)
        T.set_style(self.style_text.getStyle())
        self.plot.addElement(T)

        # Connection to parent (if any)
        if node.bpointer:
            father_node = tree[node.bpointer]
            # Can use parent.pos_x/y since we're going depth-first.
            L = line(father_node.pos_x, father_node.pos_y + NODE_RADIUS,
                     pos_x, pos_y - NODE_RADIUS)
            L.set_style(self.style_line.getStyle())
            self.plot.addElement(L)

    def plotTree(self, tree):
        """Go over nodes depth-first and add them to plot."""

        tree.update_depth(tree.root)
        tree.update_height(tree.root)
        tree.update_width(tree.root)
        for i in tree.expand_tree():
            self.plotNode(tree, i)
            node = tree[i]
            if not node.fpointer:
                self.indent += 1


def plot(filename, tree):
    """Main plotting routine."""

    plotter = TreePlotter()
    plotter.plotTree(tree)

    # For debugging:
    #print plotter.plot.getXML()
    plotter.plot.save(filename + ".svg")


if __name__ == "__main__":
    pass
