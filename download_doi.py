# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 16:16:54 2019

@author: Abhis
"""

import sys
from scbooks import api_unpaywall


j=0
doi = sys.argv[0]

flag = api_unpaywall(doi,j)
if flag == 0:
    print("not found")
else:
    ("downloaded")
