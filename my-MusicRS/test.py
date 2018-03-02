#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  2 14:34:34 2018

@author: aleja
"""

import pandas as pd
import numpy as np

df = pd.DataFrame({'A': [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3],
                   'B': [1, 2, 3, 4, 1, 2, 4, 5, 5, 2, 1, 4],
                   'C': np.random.randn(12)})

u = df['A'].unique()
print u
i = df['B'].unique()
print i

u_id = u[1]
print u_id

all_i = list(df['B'].unique())
print all_i


data = (df['A'] == u_id)
print data

