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
    yi = {}     # yield
    area = {}
    for row in data(data_file):
        crop, element, country = row[0].split(',')
        numbers = [re.match(r'[\d.]+', s) for s in row[1:]]
        numbers = [float(x.group()) for x in numbers if x]
        v = median(numbers)
        if element == 'YI':
            yi[country] = v
        if element == 'AR':
            area[country] = v

    # Countries reporting both yield and area.
    countries = set(yi.keys()) & set(area.keys())

    points = []
    for c in countries:
        points.extend([area[c], yi[c]])
    print(points)

    g = svg.charts.plot.Plot(dict(
      min_x_value=0,
      min_y_value=0,
      draw_lines_between_points=False,
      scale_x_integers=True,
      scale_y_divisions=10.0,
      show_data_points=True,
      show_data_values=False,
      show_x_guidelines=True,
      show_x_title=True,
      show_y_title=True,
      x_title='Production Area, k hectares',
      y_title='Yield, 100 kg / hectare',
      ))
    g.scale_x_divisions = 100.0

    g.add_data(dict(data=points, title='Avena'))
    with open('pretty.svg', 'wb') as f:
        f.write(g.burn())

if __name__ == '__main__':
    main()
