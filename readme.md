Tortoise
========

A Template Engine inspired by Jinja2, built for fun!

## Parser
1. Create a base _Node class.
2. Various different types of _Classes that inherit from _Node.
3. Each has its own render_node() method, that works according to its function.
4. Each stores a list of children nodes.
5. Final render() method renders the node itself, and all its children.
6. Start from the Root node and build the tree by adding children and then render the final tree.


## TODO
+ Fix the token cleanup. It's a mess. :-/
+ Loop and Conditional constructs.
+ Filters.
+ Loaders.
+ Variable injection in global scope (See context processors in jinja).


[MIT License (c) Manish Gill](http://manish.mit-license.org/)
