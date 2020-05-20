# -*- coding: utf-8 -*-
import cProfile
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput

from brownian.simulation1 import Simulation1
from brownian.simulation2 import Simulation2
from brownian.outils import stats

import os
os.environ["PATH"] += r";C:\Program Files (x86)\Graphviz2.38\bin"


def main_a():
    a = Simulation1(nb_etapes=10, density=0.5, epsilon_time=0.02, time_interval=4, speed=10, speed_BP_init=10)
    a.calcul()
    stats(a)


def main_b():
    b = Simulation2(nb_etapes=10, density=0.5, epsilon_time=0.02, dim=180, speed=10, speed_BP_init=10)
    b.calcul()
    stats(b)


config = Config(include_stdlib=True)
config.trace_filter = GlobbingFilter(exclude=['pycallgraph.*', 'numpy.*'])

with PyCallGraph(output=GraphvizOutput(output_file='Simulation1.png'), config=config):
    main_a()

with PyCallGraph(output=GraphvizOutput(output_file='Simulation2.png'), config=config):
    main_b()

cProfile.run('main_a()')
cProfile.run('main_b()')
