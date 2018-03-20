# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 15:16:24 2018

@author: Worrarat
"""


from waitress import serve
from app import api

serve(api, host='localhost',port=8000)
