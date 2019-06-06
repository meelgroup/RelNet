.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
    :target: https://opensource.org/licenses/MIT/

======
RelNet
======

RelNet is a counting-based network reliability framework using
state-of-the-art approximate model counters like ApproxMC_.

------------
Requirements
------------

- Python 3
- ApproxMC_ (for model counting)

-------
Install
-------

First download the repository:

.. code-block:: sh

    $ git clone https://github.com/paredesroger/relnet
    $ cd relnet

Install (optional) the package to make sure you meet Python dependencies:

.. code-block:: sh

    $ python setup.py install

----------
Background
----------

In the K-terminal network reliability problem you are given a graph :code:`G=(V,K,E)` and you are asked to
compute the probability that the terminal nodes in :code:`K`, a subset of :code:`V`, will remain connected
given that each edge :code:`e` in :code:`E` fails with probability :code:`p_e`.

-------
Example
-------

The toy problem in Fig. 1(a) of our `paper <https://arxiv.org/abs/1806.00917>`_ considers a graph :code:`G=(V,K,E)`
with :code:`V=[1, 2, 3, 4]`, :code:`K=[1, 4]`, and :code:`E=[(1,2), (1,3), (2, 4), (3, 4)]`, and edge "down"
probabilities :code:`P=[0.5, 0.375, 0.5, 0.5]`. The input file format for this graph is as follows: ::

    c "c" lines are comments
    c problem type
    p g
    c terminal nodes
    T 1 4
    c edges and corresponding "up" probabilities
    e 1 2 0.5
    e 1 3 0.625
    e 2 4 0.5
    e 3 4 0.5


To compute the unreliability :code:`u` of the graph, construct the CNF file issuing:

.. code-block:: sh

     $ python -m relnet example_graph.txt example_graph.cnf
     [relnet] CNF file "example_graph.cnf" saved
     [relnet] Number of sampling variables is 6
     [relnet] For counting issue:
              $  approxmc example_graph.cnf


If you install ApproxMC_, you can compute the count issuing:

.. code-block:: sh

    $ approxmc example_graph.cnf
    ...
    [appmc] FINISHED AppMC T: 0.02 s
    [appmc] Number of solutions is: 33 x 2^0

Finally, the unreliability is :code:`u = (33 * 2^0 ) / 2^6 = 0.515625`

------------------------
Approximation Guarantees
------------------------

For a large graph you can set multiplicative error threshold :code:`epsilon_val` and chance of exceeding it
:code:`delta_val` as follows:

.. code-block:: sh

    $ approxmc --epsilon epsilon_val --delta delta_val large_graph.cnf

-----------
How to Cite
-----------

If you use RelNet, please cite these papers `PMDV2019 <https://doi.org/10.1016/j.ress.2019.04.025>`_ and
`AAAI17 <https://www.comp.nus.edu.sg/~meel/bib/DMPV17.bib>`_.

.. _ApproxMC: https://github.com/meelgroup/ApproxMC/