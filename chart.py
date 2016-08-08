#!/usr/bin/python

# Python 3 caution: this code works with Python 3,
# but there is a bug in svg.charts.plot (with Python 3) that
# makes it omit labels and circles.

from __future__ import print_function

import csv
import math
import re

import svg.charts.plot

data_file = 'apro_acs_a.tsv'

from collections import namedtuple

Datum = namedtuple("Datum", 'x y text')

# C1410 is Oats, Avena sativa
def data(fn, RE=r'C1410,..,..'):
    with open(fn) as f:
        rows = csv.reader(f, delimiter='\t')
        header = next(rows)
        for row in rows:
            if re.match(RE, row[0]):
                yield row

def median(xs):
    if not xs:
        return None

    ss = sorted(xs)
    m = (len(ss)-1) * 0.5
    mf = int(math.floor(m))
    mc = int(math.ceil(m))
    return (ss[mf] + ss[mc]) * 0.5

def main():
    crop = ['C1410', 'Oats',
      'C1110', 'Wheat',
      'C1300', 'Barley',
      'P1100', 'Field peas',
      'R1000', 'Potatoes',
      'R2000', 'Sugar beet',
    ]

    for code, cropname in zip(crop[0::2], crop[1::2]):
        chart(code, cropname)

def chart(code, cropname):
    yi = {}     # yield
    area = {}
    for row in data(data_file, RE=code+',..,..'):
        crop, element, country = row[0].split(',')
        numbers = [re.match(r'[\d.]+', s) for s in row[1:]]
        numbers = [float(x.group()) for x in numbers if x]
        v = median(numbers)
        if v is None:
            continue
        if element == 'YI':
            yi[country] = v / 10.0
        if element == 'AR':
            area[country] = v

    # Countries reporting both yield and area.
    countries = set(yi.keys()) & set(area.keys())

    points = []
    for c in countries:
        points.append(Datum(area[c], yi[c], c))

    g = svg.charts.plot.Plot(dict(
      graph_title='Agricultural yield, EU countries',
      min_x_value=0,
      min_y_value=0,
      draw_lines_between_points=False,
      show_data_points=True,
      show_data_values=True,
      show_graph_title=True,
      show_x_guidelines=True,
      show_x_title=True,
      show_y_title=True,
      x_title='Production Area, k hectares',
      y_title='Yield, tonne / hectare',
      ))
    if max(p[0] for p in points) > 999:
        g.scale_x_divisions = 1000.0
    else:
        g.scale_x_divisions = 100.0
    g.scale_y_divisions = 1.0
    if max(p[1] for p in points) > 20:
        g.scale_y_divisions = 10.0
    g.width = 800
    g.height = 600

    g.add_data(dict(data=points, title=cropname))
    with open('output/' + code + '.svg', 'wb') as f:
        f.write(g.burn())

if __name__ == '__main__':
    main()
