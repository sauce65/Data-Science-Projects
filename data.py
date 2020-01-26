import sys
import csv
import sqlite3
import re
import pandas as pd
import statistics as stats
import numpy as np
from scipy import stats as sp
import math

data = {
'precip_1992' : '25.3,,29.9,,34.3,,35.6,32.3,,,23.3,,,31.8,24.9,31.8,31.4,,,30.7,37.3,,23.5,25.3,,23.9,31.3,40.2,29.8,32.7,,32.3,26.7,,,,24.7,,,28.1,,,26.3,,31.1,28.0,31.8,,41.6,,21.1,27.2,33.0,29.2,31.4,31.2,,,,20.7,,31.8,,,35.4,,37.9,,30.5,31.3,,19.5,,28.4,31.2,,25.5,21.6,34.2,26.3,30.8,42.0,,41.2,35.8,29.0,,,,,41.1,28.2,,21.7,42.5,45.3,17.5,38.4,19.8,48.4,29.6,23.0,31.8,18.7,51.8,,,35.5,35.8,,,32.2,,21.8,33.6,51.1,',
'precip_1993' : '30.4,,37.3,,44.3,,41.8,50.0,,,26.8,,,34.8,30.9,37.5,36.0,,,39.8,48.6,,25.6,31.2,,27.5,36.0,51.0,32.0,42.6,,41.0,34.1,,,,30.5,,,34.3,,,26.9,,30.5,35.2,40.5,,48.5,,29.7,29.8,39.5,38.0,33.6,36.3,,,34.9,23.4,,42.7,,,43.4,,45.2,,35.3,37.5,,26.5,,30.2,44.1,,34.6,22.7,55.2,27.9,28.7,53.8,,44.8,47.7,34.3,,,,,60.0,33.2,,22.5,48.6,54.4,22.1,38.8,27.0,68.5,38.1,30.3,36.0,19.4,63.6,,,42.9,36.9,,,40.0,,29.9,40.5,61.8,',
'precip_1994' : '26.7,,33.1,,34.6,,34.3,34.9,,,22.0,,,28.9,21.6,32.5,33.4,,,30.6,32.2,,25.4,25.5,,23.1,27.8,42.6,27.2,32.2,,31.4,26.3,,,,24.7,,,27.9,,,27.3,,30.0,26.2,27.6,,36.4,,20.0,27.4,31.1,32.6,26.2,28.5,,,32.0,18.3,,30.6,,,31.8,,39.4,,28.3,34.3,,17.1,,31.1,28.3,,27.2,19.6,36.5,21.3,28.3,37.6,,40.0,35.2,24.5,,,,,42.3,29.7,,21.1,44.6,45.7,17.5,38.4,21.0,51.3,28.2,23.7,35.6,20.5,51.9,,,28.3,34.4,,,39.5,,22.3,31.5,51.6,',
'precip_1995' : '34.5,16.8,,,41.8,22.4,,,51.6,30.3,,,48.1,24.8,54.4,32.0,,,,,37.5,19.4,,,,,47.2,25.1,37.3,21.4,40.9,23.8,41.6,24.1,,,,,42.2,24.4,47.8,28.5,61.4,36.3,34.4,17.0,36.1,18.7,34.4,18.0,41.2,21.1,54.2,33.9,36.9,18.1,48.1,27.9,,,44.2,25.5,42.2,23.5,,,,,,,33.8,18.2,,,,,39.6,20.5,,,,,41.2,21.5,,,40.4,22.6,43.9,24.0,45.9,24.5,,,54.2,28.0,,,32.0,17.2,38.8,19.3,41.5,22.4,43.5,25.4,38.5,20.8,41.4,23.5,,,,,43.2,21.5,26.9,14.3,41.0,22.9,48.1,27.7,,,,,50.6,28.3,,,51.3,29.1,,,41.0,23.6,46.7,26.3,,,29.8,15.4,,,41.7,20.5,50.0,28.6,39.5,21.3,31.8,17.2,57.8,34.0,31.4,16.5,33.1,18.2,60.1,33.7,,,53.8,30.3,52.6,30.0,36.2,18.8,,,,,,,,,68.9,41.4,39.7,22.8,,,30.2,17.1,56.7,31.4,55.4,34.4,23.3,11.4,45.3,26.0,31.2,15.4,68.5,41.6,44.1,24.3,31.0,17.5,45.4,23.7,25.9,15.0,70.1,41.9,,,,,44.4,24.5,39.2,23.0,,,,,45.3,23.8,,,32.7,16.5,42.9,23.0,69.1,42.2,,',
'precip_1996' : '23.5,10.8,,,41.5,24.1,,,32.0,18.3,,,50.1,30.2,40.7,25.5,,,,,26.7,16.3,,,31.8,21.0,34.7,21.2,27.8,17.4,26.9,13.6,27.3,13.8,,,,,50.5,33.1,26.9,14.9,39.9,20.8,31.3,18.8,35.2,21.7,33.2,21.2,21.8,10.4,31.5,17.2,37.2,22.7,40.1,25.8,,,25.0,14.1,33.9,21.9,,,,,,,29.7,19.1,,,,,40.5,24.9,,,,,31.1,18.3,,,30.6,17.8,33.9,20.8,37.8,23.1,,,51.7,32.7,,,29.0,17.6,37.8,22.1,40.2,24.3,24.5,12.9,26.6,14.2,27.6,14.4,,,,,41.8,25.5,25.8,15.8,24.7,12.4,30.2,17.0,,,22.1,10.0,35.1,21.1,,,29.8,14.6,,,26.8,14.8,28.7,16.4,,,24.8,14.8,,,37.3,21.5,32.4,19.8,28.2,14.4,23.2,13.8,34.8,20.5,30.2,17.9,27.6,17.0,56.9,37.3,,,37.7,22.6,48.5,31.7,38.2,22.8,,,,,,,,,54.6,33.9,25.1,13.5,,,20.9,12.0,28.9,14.0,40.0,22.3,20.1,12.2,27.1,12.8,28.7,18.3,69.3,47.3,38.0,25.0,16.7,8.0,47.3,29.0,13.7,6.1,37.9,20.8,,,,,42.7,26.9,23.9,11.7,,,,,30.4,14.6,,,26.5,15.0,42.4,25.8,36.1,19.9',
'precip_1997' : '33.4,16.5,,,42.3,24.2,,,55.5,33.8,,,47.0,27.1,57.4,34.5,,,,,29.5,17.0,,,40.7,22.6,45.5,25.5,33.3,21.1,50.7,28.2,47.5,27.2,,,,,53.8,31.4,45.9,28.8,70.7,42.2,35.1,20.1,31.8,19.6,38.5,20.3,30.6,16.1,48.5,29.6,37.4,20.4,55.4,32.4,,,49.0,30.2,44.3,25.8,,,,,,,30.9,19.1,,,,,35.8,21.9,,,,,35.5,20.5,,,41.4,25.6,34.8,21.3,37.8,23.7,,,55.8,31.9,,,28.8,17.9,38.3,21.4,42.3,24.1,39.8,23.4,44.0,26.7,43.5,28.3,,,,,39.9,23.7,30.3,16.3,43.5,24.3,45.9,26.5,,,34.2,17.2,43.7,25.4,,,50.1,30.1,,,41.8,25.1,45.3,26.5,,,27.0,16.4,,,39.7,21.7,43.6,26.8,39.8,22.1,27.1,15.9,55.3,33.1,31.3,16.6,32.2,19.2,65.5,39.0,,,55.5,34.5,53.6,31.4,41.5,23.4,,,,,,,,,62.1,39.3,42.4,26.8,,,33.3,19.8,53.7,27.9,63.8,38.4,23.1,13.4,52.2,28.1,29.2,17.2,77.6,49.0,48.5,27.5,27.0,14.2,48.8,28.5,28.2,16.2,67.1,40.6,,,,,44.0,27.4,44.1,24.8,,,,,40.7,21.7,,,33.5,17.6,46.5,27.3,66.1,40.2',
'precip_1998' : '32.9,17.0,,,33.9,18.7,,,35.5,20.0,,,37.2,21.3,44.4,26.5,,,,,24.0,13.6,,,24.5,16.9,38.7,22.6,22.3,13.6,31.3,17.8,29.9,17.5,,,,,35.2,21.7,34.3,21.8,39.2,23.8,27.0,14.0,27.5,15.0,26.7,15.6,28.2,14.9,40.4,24.0,27.0,15.3,38.1,23.7,,,31.4,18.9,33.3,19.2,,,,,,,26.3,14.4,,,,,29.6,16.8,,,,,28.8,15.1,,,30.8,18.9,28.4,16.5,35.2,20.4,,,42.9,24.6,,,27.9,14.6,32.7,18.2,34.7,19.8,30.7,18.3,27.5,15.0,35.4,19.9,,,,,28.9,17.4,19.8,12.0,26.9,15.8,38.3,24.4,,,32.5,17.6,33.9,21.1,,,40.3,24.1,,,27.1,16.2,30.0,17.4,,,23.8,12.0,,,35.0,18.9,36.1,21.9,31.0,17.6,16.7,10.1,39.8,25.5,23.3,12.8,25.3,14.5,45.4,28.3,,,38.1,23.9,41.6,25.1,29.7,17.6,,,,,,,,,43.6,27.1,26.1,15.2,,,26.0,14.4,44.3,24.6,42.0,25.7,16.8,9.1,35.4,18.7,20.2,11.3,59.5,37.7,35.6,20.9,24.6,14.6,37.5,20.3,20.5,10.8,45.8,30.2,,,,,33.3,18.9,30.2,17.0,,,,,33.9,17.4,,,21.0,10.4,35.1,20.0,47.1,30.2',
'precip_1999' : '39.1,19.9,,,36.6,21.0,,,54.0,28.5,,,43.7,23.0,39.5,22.8,,,,,29.3,14.2,,,30.2,17.7,36.5,21.4,30.8,17.0,46.5,24.4,47.4,24.4,,,,,37.1,22.7,34.1,19.1,58.2,30.8,35.3,17.2,32.5,17.7,29.4,16.7,32.2,16.6,42.3,24.2,32.6,19.4,40.0,24.6,34.7,15.4,39.4,22.3,39.2,23.5,,,,,,,31.9,17.2,,,,,38.7,20.5,,,,,33.3,18.4,,,40.5,21.9,33.9,18.4,39.0,20.9,36.8,19.2,45.2,27.6,,,26.3,14.5,38.8,18.5,37.4,21.9,38.0,22.4,41.2,20.6,41.0,22.1,,,40.7,25.8,39.5,21.5,26.2,15.2,39.9,20.4,33.7,17.8,,,30.2,16.2,35.9,19.4,37.4,19.3,50.5,27.6,,,41.2,21.2,44.4,23.1,,,23.8,12.8,,,38.5,17.9,37.0,20.2,35.4,17.6,25.2,13.5,43.6,23.5,27.5,15.9,26.5,15.3,47.4,30.4,,,53.9,29.4,37.6,23.6,34.8,21.0,23.2,11.9,,,,,,,52.6,30.1,39.7,22.0,,,34.5,18.6,47.4,24.5,58.8,31.9,19.9,11.6,46.6,23.5,24.2,12.9,59.4,38.3,36.3,20.8,27.4,14.1,44.1,23.2,33.1,16.6,61.6,35.1,,,,,35.9,20.2,47.7,22.8,,,,,44.0,22.0,,,27.3,15.1,42.2,24.1,64.5,35.7',
'precip_2000' : '27.1,15.6,,,35.6,18.3,,,32.8,16.3,,,40.6,21.6,37.7,20.7,,,,,23.0,12.1,28.6,13.8,29.8,16.2,28.7,16.4,22.8,12.9,21.9,11.2,19.6,10.2,,,,,39.6,22.8,27.1,15.5,38.4,18.8,26.3,13.5,31.0,16.3,27.6,13.8,20.6,12.4,22.2,11.7,28.5,15.4,36.7,21.6,26.2,12.9,24.4,13.1,29.5,16.7,,,,,,,27.4,14.4,,,,,32.1,16.7,,,,,25.6,14.2,,,26.0,13.8,27.5,15.2,35.4,19.1,28.1,15.5,44.8,24.7,34.7,17.7,24.2,13.0,28.4,15.4,35.2,19.0,22.5,11.5,25.5,12.2,28.7,14.3,,,36.0,20.8,35.5,18.8,20.8,10.7,27.2,13.1,25.7,12.8,,,23.8,11.6,28.1,15.2,27.4,14.9,27.3,13.2,,,23.8,12.0,23.4,12.2,,,23.5,12.2,,,27.0,14.8,31.0,16.1,30.7,13.2,18.0,9.2,30.7,16.4,26.5,13.8,29.1,14.2,47.2,28.5,,,35.5,19.3,36.8,22.0,30.6,17.3,15.9,8.5,,,,,,,43.7,23.0,20.9,11.6,,,23.0,11.5,34.7,16.1,29.9,16.3,18.9,10.2,26.0,12.8,25.3,13.4,58.9,35.2,33.8,18.7,19.1,10.5,33.6,18.8,13.1,6.3,30.3,16.6,,,,,36.7,20.1,18.7,9.9,,,,,27.6,14.7,,,27.2,14.5,37.4,20.6,30.7,16.2,,',
'precip_2001' : '17.2,9.7,,,28.0,14.8,,,44.5,27.1,,,34.8,19.4,35.2,21.2,,,,,26.2,13.3,30.2,16.5,22.8,13.2,28.9,16.8,24.1,12.9,35.7,22.0,31.4,20.5,,,,,32.5,20.5,31.3,19.7,48.3,30.5,20.4,10.1,28.2,14.9,23.7,13.3,27.6,15.0,38.0,24.4,25.5,13.7,32.1,19.8,26.4,11.6,26.2,15.8,26.4,16.0,,,,,,,28.5,14.8,,,,,27.9,15.0,,,,,29.4,15.6,,,28.6,17.1,30.0,16.0,31.2,16.7,31.4,16.4,35.4,20.1,32.7,17.2,22.3,11.9,28.5,14.7,30.4,17.4,33.8,20.7,26.5,15.9,28.5,16.4,,,29.1,18.5,31.2,16.8,19.4,10.6,30.0,17.2,30.1,16.7,,,28.0,13.4,28.8,17.7,31.0,15.9,41.9,26.6,,,26.5,16.9,30.5,18.8,,,17.3,9.4,,,29.0,13.6,28.9,15.1,25.8,14.4,15.5,8.3,30.8,17.9,20.7,11.8,24.2,12.2,36.1,23.1,,,41.4,25.4,33.6,20.1,27.1,15.2,19.8,9.6,,,,,,,46.4,25.9,21.0,15.1,,,27.7,16.2,46.0,24.3,51.3,32.3,15.1,8.0,40.0,23.7,20.0,11.3,47.5,31.0,30.5,17.8,21.0,12.2,33.6,17.5,23.2,14.8,53.3,34.6,,,27.7,15.6,31.9,18.8,35.3,21.0,,,,,31.5,16.8,,,23.1,13.1,33.1,18.6,50.7,32.8,,',
'precip_2002' : '16.9,7.0,,,19.2,11.5,,,25.8,13.1,,,22.9,14.2,29.1,16.8,,,,,15.9,9.5,16.8,8.1,16.9,9.6,18.6,12.5,19.2,10.9,17.8,9.0,16.5,8.0,,,,,27.5,17.0,17.8,11.8,19.9,11.2,18.6,9.3,20.7,11.6,15.8,9.6,14.5,6.6,19.5,10.3,20.8,11.8,27.0,17.6,19.2,8.1,22.1,12.2,21.6,13.5,,,,,,,17.9,10.0,,,,,19.4,10.2,,,,,18.3,9.4,,,22.7,11.8,21.2,11.5,22.8,12.9,19.7,10.1,31.4,18.3,22.8,13.3,16.2,8.9,20.5,11.1,22.4,13.4,14.6,9.3,19.8,9.7,24.0,12.0,,,28.2,17.1,21.0,11.2,16.6,9.2,18.8,9.3,24.0,14.5,,,12.3,6.5,23.5,14.2,19.8,10.0,20.3,9.5,18.9,10.6,16.7,8.8,23.6,11.7,,,15.3,7.7,,,23.1,10.9,26.3,14.4,19.4,10.0,14.3,7.6,27.3,15.1,18.9,10.2,14.8,7.6,32.3,21.0,,,27.2,15.5,24.1,15.4,22.4,12.0,9.9,4.3,,,,,,,34.7,20.4,18.9,10.2,,,14.1,7.0,24.3,11.8,27.4,14.8,12.0,6.4,15.6,7.6,16.6,9.0,40.4,25.4,23.4,14.3,13.2,6.6,26.2,14.4,11.5,5.2,24.3,14.0,,,19.0,9.5,26.7,15.9,17.0,7.9,,,,,17.5,9.7,,,16.5,9.3,26.8,15.4,20.4,12.1,,',
'precip_2003' : '28.6,14.2,36.0,20.6,36.8,21.4,,,35.6,19.5,,,43.2,23.9,41.3,24.5,,,,,20.7,11.3,26.2,13.5,22.3,14.3,32.7,19.1,25.0,14.1,29.8,16.4,25.7,14.5,,,,,37.5,23.1,30.5,19.4,38.8,20.8,27.8,14.9,30.5,17.3,31.1,18.3,29.5,13.6,33.9,20.3,34.6,18.7,43.5,26.9,30.2,15.3,28.1,15.9,31.2,18.7,,,,,,,27.7,16.1,,,,,39.5,19.9,,,,,28.4,15.2,,,27.7,15.3,27.9,16.2,35.4,19.4,33.0,18.4,51.1,29.2,39.0,22.0,22.4,13.4,31.6,18.1,40.0,23.8,23.4,12.6,27.2,15.2,34.5,18.7,,,38.5,23.9,39.5,21.5,23.5,12.6,31.1,16.3,31.4,18.4,31.6,18.7,26.1,13.0,30.6,18.0,28.2,16.4,29.7,16.7,31.0,15.8,25.7,14.2,30.0,16.4,,,20.5,11.8,39.2,22.4,31.4,17.3,34.8,19.6,29.8,16.5,18.6,9.7,37.4,23.0,33.8,19.5,25.4,14.3,48.0,30.1,30.0,17.2,34.5,20.1,43.3,26.5,31.9,18.6,17.2,9.9,,,,,,,46.4,27.0,26.9,14.1,,,23.7,11.7,39.2,20.0,40.0,23.8,24.7,13.1,29.3,15.7,30.3,15.7,61.8,39.4,34.4,20.9,25.4,12.0,35.6,20.1,13.4,6.1,42.1,26.9,,,36.6,19.5,43.7,24.5,30.2,15.4,,,,,33.2,15.3,,,28.1,15.7,37.6,21.6,38.9,24.7,39.7,25.0',
'precip_2004' : '28.6,13.6,39.5,20.0,35.6,18.7,,,41.6,23.2,22.0,12.3,34.5,18.7,42.4,24.2,,,,,20.4,10.4,23.1,11.2,23.4,12.4,30.7,17.3,22.0,13.0,32.6,17.7,32.1,17.1,,,,,36.9,22.0,31.7,18.8,43.9,23.7,29.2,13.4,21.3,11.7,22.4,12.3,26.2,13.7,35.5,21.0,32.0,16.4,38.1,21.8,26.1,11.6,30.3,18.5,32.4,19.1,,,,,,,23.2,12.9,,,,,24.1,12.8,,,,,25.0,12.7,,,32.6,17.2,26.0,14.8,29.6,16.9,21.4,11.1,37.0,19.5,28.4,15.9,20.7,11.8,28.6,14.0,32.4,16.0,32.8,20.3,25.8,12.6,34.0,18.2,,,38.1,21.7,26.1,13.5,21.4,9.8,30.1,15.0,28.5,16.4,24.6,13.9,28.0,15.3,30.1,18.4,22.8,11.6,40.1,22.5,24.4,11.9,31.1,16.9,35.2,19.3,,,17.2,9.6,34.7,16.1,33.6,15.6,30.7,18.6,32.1,16.4,18.3,10.2,43.6,24.7,24.1,11.4,22.3,13.2,43.4,25.5,26.4,12.1,41.4,23.1,37.3,23.9,40.8,19.2,21.6,9.0,,,,,,,44.8,27.5,28.4,16.4,,,20.9,11.6,36.9,20.2,47.1,27.2,18.8,8.7,30.2,18.8,20.4,11.4,58.7,35.8,29.2,16.7,17.3,9.6,36.4,18.2,15.4,8.6,50.9,30.2,,,36.3,17.6,31.3,17.7,33.9,18.8,,,,,36.4,17.6,,,24.6,10.8,37.2,19.5,48.6,28.3,45.1,26.3',
'precip_2005' : '28.9,17.2,35.6,21.3,33.7,18.7,16.2,8.3,48.1,30.7,27.0,14.6,39.5,22.8,50.3,30.7,,,,,19.6,10.5,23.4,12.4,24.9,14.8,32.7,19.1,28.8,17.4,41.0,25.4,36.4,23.6,,,17.2,9.4,35.1,21.1,42.5,28.8,61.8,38.6,26.3,14.5,24.5,13.7,23.6,11.8,27.9,16.1,48.5,30.9,28.4,16.0,39.1,23.5,26.1,14.8,34.6,21.5,34.1,21.1,,,,,,,22.2,12.2,30.6,15.6,34.8,21.1,24.6,13.7,,,,,24.3,13.9,,,32.5,19.2,28.4,16.4,34.1,19.3,23.7,13.9,37.3,22.1,33.5,18.2,23.8,13.1,29.2,17.0,31.7,18.7,34.8,22.5,32.5,18.6,34.6,20.6,,,36.2,23.2,25.4,14.6,21.9,12.0,38.4,21.8,38.1,23.4,29.8,17.1,22.4,11.8,41.0,26.0,22.5,12.4,44.9,29.1,27.6,14.2,34.4,20.6,36.7,23.0,,,20.0,10.8,34.1,18.3,29.7,17.2,40.7,24.9,35.2,20.6,20.0,11.0,60.7,39.8,23.9,13.1,27.1,16.1,44.2,27.3,25.9,13.6,45.5,27.8,38.7,24.1,31.5,18.7,14.8,7.4,,,,,,,57.4,34.3,32.6,20.6,50.0,29.2,24.4,15.4,36.3,22.1,53.0,36.5,17.1,9.6,49.0,28.7,23.9,13.6,58.2,36.6,33.0,18.6,27.4,15.5,34.6,19.5,25.8,15.2,70.3,46.3,,,35.2,20.5,35.7,21.1,40.6,25.2,,,,,35.6,19.6,,,26.4,14.8,34.3,20.1,64.0,42.4,39.8,24.4',
'precip_2006' : '19.9,8.4,39.6,24.7,28.1,18.3,25.8,14.9,38.5,20.5,27.5,16.1,42.5,26.8,47.7,29.6,,,,,26.1,15.4,28.9,14.6,28.8,18.4,37.2,22.7,28.4,16.1,35.0,17.3,32.0,16.4,,,15.3,7.4,49.8,31.3,35.9,16.9,38.0,19.4,26.4,14.3,34.0,20.8,29.4,17.9,25.3,10.2,38.9,19.1,29.0,17.5,44.7,27.4,28.3,13.1,33.0,16.7,32.8,19.8,,,,,,,29.9,18.1,32.2,12.8,35.8,18.0,35.9,21.3,,,,,33.6,18.6,,,34.9,19.1,33.7,19.8,39.7,25.3,34.3,19.2,45.2,26.2,37.3,23.0,25.1,16.4,29.2,17.7,33.2,20.7,33.1,16.7,30.9,14.8,35.2,17.6,,,39.8,25.1,30.1,17.1,23.1,14.5,30.7,14.1,37.2,22.4,31.4,18.4,15.5,7.9,32.5,18.5,34.4,19.0,40.7,20.7,27.9,16.7,28.8,15.1,33.5,17.6,,,23.8,15.1,32.5,17.7,28.7,16.1,36.2,21.4,28.1,16.1,22.4,12.5,38.1,22.8,21.9,13.5,27.6,14.4,53.2,35.1,26.6,15.4,43.8,24.4,42.3,27.2,31.2,18.9,23.4,10.0,,,,,,,49.6,30.0,27.0,13.9,41.2,19.6,25.5,13.5,39.9,17.2,43.9,22.5,17.8,10.4,34.9,15.7,25.7,16.3,70.4,46.5,35.1,22.9,18.8,9.1,37.1,22.7,19.4,9.7,47.8,24.4,,,26.1,11.6,41.7,26.2,30.8,15.2,,,,,30.7,12.6,30.4,16.8,22.4,13.3,37.4,22.0,48.7,25.4,50.1,31.7',
'precip_2007' : '32.2,17.1,35.4,20.4,33.1,20.4,23.5,13.4,51.0,28.3,25.9,13.8,40.7,24.1,38.7,22.6,,,,,27.9,14.7,28.8,14.4,24.8,14.4,29.6,17.7,22.0,12.7,37.8,21.9,37.3,21.4,,,20.2,9.2,32.0,19.7,35.4,22.4,49.7,27.7,30.2,16.9,29.4,16.9,23.9,13.8,32.5,15.4,36.9,22.7,29.7,17.7,35.1,21.0,33.4,19.2,33.7,18.7,30.5,17.2,,,,,,,30.2,16.1,39.4,20.3,37.0,19.7,34.1,18.9,,,,,31.9,18.1,,,37.5,21.4,33.4,18.2,34.7,20.3,34.3,20.3,39.1,22.2,36.3,20.4,23.3,14.1,32.9,19.3,33.7,20.3,35.8,20.6,34.3,17.9,37.7,21.3,,,37.1,21.3,29.9,17.7,23.4,13.1,36.2,18.3,39.7,22.8,28.2,15.5,26.5,14.1,34.7,21.0,28.4,16.9,43.5,25.2,25.0,14.4,34.2,18.3,36.9,21.5,,,20.5,11.9,31.4,17.1,29.5,18.7,37.1,22.3,34.3,18.6,17.1,9.9,39.7,23.7,23.6,13.4,26.6,14.3,38.1,24.8,30.2,16.7,45.5,26.3,34.4,21.8,34.9,20.0,22.6,11.0,,,,,,,42.4,26.2,34.7,18.1,40.9,21.2,31.1,16.5,43.8,23.6,53.7,32.1,19.5,10.7,39.7,21.9,24.1,13.0,50.1,30.6,28.4,17.4,29.0,14.8,36.7,21.7,22.6,12.9,55.0,33.7,,,36.7,18.0,32.4,19.1,34.8,18.6,,,,,38.1,18.7,30.7,17.2,24.0,13.1,36.8,22.2,50.1,31.7,41.6,23.9',
'precip_2008' : '29.8,14.9,38.7,23.9,30.8,16.5,25.7,15.4,41.9,26.9,29.7,16.6,44.0,26.5,45.6,29.1,,,,,28.9,17.1,28.9,15.0,27.8,17.6,37.9,23.1,31.4,19.8,35.6,22.3,37.4,22.4,37.5,22.9,18.2,8.6,40.8,26.1,34.1,23.4,48.6,30.4,26.2,13.4,32.1,18.8,30.7,19.3,22.0,12.0,50.4,33.7,32.3,19.3,40.8,26.3,28.4,13.6,35.3,22.4,35.1,21.9,,,,,,,30.9,18.7,27.5,13.4,32.8,19.8,34.9,20.0,,14.5,,,31.6,18.0,,,35.2,22.4,35.3,21.8,42.1,26.4,30.0,16.5,46.5,27.9,39.0,22.4,31.4,19.4,30.4,17.0,37.0,21.6,37.2,23.9,29.6,17.5,37.4,22.4,,,39.7,25.0,36.8,20.7,23.9,15.1,31.9,19.2,36.1,22.7,30.2,18.2,27.9,16.9,38.7,24.3,28.1,15.7,42.8,26.6,31.3,18.0,32.9,21.2,36.6,23.8,,,26.1,16.3,35.1,19.7,18.8,10.2,42.6,27.5,31.5,19.3,24.5,15.3,46.8,31.3,24.6,14.0,26.5,17.1,52.0,33.7,28.7,17.0,48.3,30.8,40.4,26.6,35.4,21.9,20.9,10.8,24.8,14.4,,,,,58.8,37.9,30.2,18.7,45.9,26.2,24.7,15.7,46.8,28.7,50.9,32.8,21.4,12.1,37.8,21.8,28.3,16.8,57.5,38.1,33.1,21.3,21.7,13.2,38.5,21.2,19.7,11.9,58.3,39.1,,,35.9,21.1,39.1,24.3,35.9,21.7,,,,,29.8,16.6,30.6,15.8,29.2,16.8,39.1,23.6,60.1,39.8,48.0,29.8',
'precip_2009' : '21.9,12.0,39.5,23.4,30.9,17.9,26.0,15.2,39.5,24.3,30.2,17.6,42.7,26.1,45.8,28.7,,,,,24.9,14.0,30.1,15.4,25.3,15.6,32.0,19.4,26.9,16.2,30.3,19.3,28.4,18.0,31.4,18.2,18.0,8.9,40.7,24.9,31.4,20.6,46.2,27.5,25.7,13.6,30.9,17.9,24.8,15.6,20.6,11.2,39.2,24.0,30.7,18.0,39.8,25.3,25.9,12.7,30.2,19.0,34.3,21.2,,,25.3,24.2,,,30.0,17.2,37.0,16.5,34.7,20.0,32.4,19.4,,13.1,,,30.3,16.9,23.1,12.1,34.2,20.2,33.4,20.4,37.7,22.9,31.0,17.9,46.4,28.1,36.8,21.9,26.4,15.9,29.7,17.1,35.6,21.7,36.4,22.0,27.6,16.6,32.8,19.6,,,40.5,25.7,33.1,20.0,23.8,14.2,33.2,19.1,32.6,21.0,33.4,20.0,19.1,11.1,34.0,21.2,30.8,17.2,40.5,25.9,25.6,15.6,32.1,17.7,35.2,22.2,20.3,10.7,18.8,11.1,35.0,19.2,29.0,15.5,37.1,23.3,27.9,16.5,20.5,12.0,41.3,27.2,23.8,14.0,26.3,15.1,46.5,30.2,28.4,16.5,42.7,26.5,40.0,25.6,33.8,19.5,20.1,10.1,24.5,14.1,23.8,13.1,,,53.3,34.5,26.4,16.5,37.8,22.5,23.9,13.6,43.0,23.5,45.1,28.8,20.3,11.7,30.6,18.5,25.3,15.1,62.5,39.5,33.6,21.3,24.1,13.4,35.6,20.5,17.9,10.6,51.0,33.7,,,28.4,17.0,38.4,23.6,27.9,17.0,,,,,27.8,15.1,30.8,16.6,24.9,13.9,37.0,22.1,50.3,33.3,48.0,29.3',
'precip_2010' : '24.5,14.2,36.0,20.3,32.7,19.1,24.7,13.3,36.0,21.3,22.7,12.5,38.3,22.4,40.5,24.2,,,,,23.9,13.9,25.8,12.9,23.7,13.4,31.5,18.4,20.2,12.1,30.5,17.7,30.2,17.5,28.5,15.1,13.9,7.1,37.1,22.5,37.2,22.9,42.6,23.9,27.5,15.4,24.7,13.8,22.7,13.1,24.9,13.6,36.9,23.2,33.3,19.8,37.7,22.5,26.8,13.3,29.6,18.3,33.5,19.9,,,35.6,20.1,,,23.8,13.7,32.5,16.6,30.4,17.4,25.9,13.6,,16.3,,,29.3,16.0,23.9,13.5,32.2,18.6,28.7,16.5,31.9,19.1,25.5,13.5,38.2,22.7,31.7,17.6,22.9,13.1,28.9,16.7,33.8,19.6,29.9,18.9,23.3,13.1,34.6,19.4,27.3,15.4,39.0,24.6,33.8,17.4,18.6,10.5,32.9,17.5,30.6,18.5,27.3,14.9,21.2,12.0,35.7,20.4,25.3,13.9,39.4,22.0,24.1,12.5,28.6,16.0,30.3,17.9,17.1,9.5,18.9,10.6,32.6,17.7,28.4,16.3,36.9,21.5,31.7,17.2,18.6,10.6,42.5,25.1,23.3,13.1,24.7,13.7,41.2,24.1,28.5,16.6,39.8,23.7,34.0,21.4,35.0,21.8,20.5,10.8,24.7,13.5,22.3,12.1,,,47.1,29.1,23.6,14.5,36.8,20.2,21.7,12.8,34.7,20.7,40.8,25.0,16.9,8.9,30.9,18.0,22.3,12.3,54.6,33.5,29.0,17.0,21.3,11.9,31.3,18.2,21.1,11.6,52.3,31.3,33.0,18.5,34.0,20.0,34.1,20.2,29.1,16.5,,,,,33.0,16.2,29.3,15.8,23.0,13.0,35.4,20.9,51.7,31.3,42.9,27.5',
'precip_2011' : '18.8,10.6,49.5,30.9,44.6,26.7,31.9,18.5,42.7,26.5,31.1,18.0,53.8,32.3,58.4,37.1,,,28.8,17.8,27.8,17.0,30.3,16.6,35.2,23.2,47.9,26.3,27.3,18.1,32.1,20.1,31.6,19.6,40.9,22.9,16.8,8.7,54.6,35.6,40.8,26.4,46.5,29.3,35.1,20.0,37.7,22.8,34.6,21.4,19.7,8.3,38.8,22.9,39.8,25.1,57.7,36.7,26.9,12.8,37.1,20.9,43.8,27.5,,,45.5,27.4,,,30.1,18.9,25.0,10.2,27.1,14.5,44.3,26.3,,8.2,,,32.4,19.0,30.4,17.7,37.5,21.9,34.5,21.3,42.8,26.5,39.3,22.9,64.4,39.5,45.9,27.6,30.6,18.6,39.9,22.3,54.0,34.0,27.3,15.5,26.4,14.8,34.2,19.5,43.9,26.5,53.0,33.9,46.8,27.5,32.5,19.0,33.4,20.3,37.1,22.8,36.0,20.2,17.6,9.3,44.8,27.0,36.9,20.5,34.6,21.1,31.4,18.2,34.1,20.6,35.9,22.4,18.3,8.8,27.1,16.4,50.3,29.0,35.2,20.0,42.3,26.7,32.1,19.1,23.8,15.4,47.2,30.9,40.0,23.6,25.0,15.7,66.9,43.6,40.8,24.7,49.2,30.1,58.0,37.1,41.9,26.3,16.5,7.8,25.9,15.1,24.6,14.2,,,62.1,41.0,29.8,17.8,41.2,25.4,23.8,14.8,30.3,16.6,51.8,32.9,27.7,16.4,32.9,20.0,32.0,18.9,85.3,55.2,44.2,27.6,17.6,9.2,49.7,29.2,15.8,9.5,51.0,33.2,36.8,23.2,25.6,13.6,42.1,26.2,30.0,17.9,,,35.8,21.6,23.4,11.6,40.6,23.9,37.3,21.8,55.9,34.4,51.5,33.1,65.0,41.9',
'precip_2012' : '22.6,13.8,25.5,16.5,28.9,17.2,20.9,11.2,33.5,21.0,20.3,10.5,31.3,18.3,33.7,20.7,,,20.3,12.8,18.1,10.2,23.3,11.1,18.5,11.5,23.8,14.6,18.5,10.1,25.7,16.7,23.9,15.6,23.5,12.1,16.0,6.6,28.4,18.3,28.6,17.4,40.5,25.4,25.9,14.0,21.9,12.4,19.0,11.2,22.1,12.2,29.5,19.4,24.9,15.8,22.9,15.8,25.1,12.0,29.0,18.0,21.8,14.1,,,28.0,16.4,26.5,15.1,21.6,12.0,25.8,13.0,26.3,14.9,23.9,12.5,,12.5,,,23.1,12.3,20.7,12.4,24.7,14.8,22.5,12.4,23.7,13.7,20.9,11.5,32.2,19.4,27.1,15.2,19.6,10.4,27.2,14.8,25.6,15.6,24.9,15.5,23.1,13.2,29.9,17.2,21.6,13.2,24.9,16.1,24.5,13.9,19.8,11.3,27.3,16.2,23.8,14.5,19.3,11.0,23.8,14.9,28.5,16.8,21.2,11.4,34.3,22.4,19.8,10.7,23.6,14.1,25.5,15.8,20.7,9.9,16.6,8.9,24.5,12.9,28.3,14.0,25.9,15.8,21.3,12.5,17.1,9.6,33.1,20.9,18.6,10.6,19.0,10.2,31.3,20.4,19.8,11.9,31.5,20.1,23.3,16.5,24.2,16.0,19.1,10.4,21.8,10.8,21.3,10.0,,,32.1,20.7,24.8,15.6,33.7,19.3,22.0,12.2,34.5,20.5,35.2,23.7,15.6,9.0,24.4,16.2,20.3,11.1,43.0,28.4,22.0,13.4,20.8,11.7,33.0,17.6,16.7,10.5,45.0,31.6,22.9,13.1,25.8,14.6,22.5,13.3,27.9,17.8,21.0,13.1,33.4,21.9,26.3,14.1,27.9,15.6,20.4,10.8,29.0,17.8,41.4,28.2,34.2,22.6',
'precip_2013' : '23.1,9.0,37.5,19.3,36.3,16.1,25.5,12.0,37.1,16.7,24.6,12.2,41.5,20.8,38.9,21.8,,17.7,29.8,12.8,22.0,10.0,32.0,12.7,28.7,14.5,28.2,14.7,27.0,12.0,29.6,13.1,27.9,12.2,32.0,14.1,15.9,6.1,37.6,20.7,34.4,17.2,39.7,17.5,34.4,12.8,28.1,13.8,28.9,15.0,26.2,10.7,31.0,16.2,30.4,15.1,32.0,19.1,33.4,11.4,32.0,14.6,27.2,15.2,,,37.1,19.7,33.3,16.4,31.6,15.6,29.5,11.0,26.3,12.1,31.3,14.4,,9.1,,,34.3,15.2,29.7,11.4,28.3,12.9,29.9,14.5,34.3,17.4,32.1,14.1,44.3,24.4,36.2,17.6,23.9,11.6,40.7,16.5,36.1,18.8,26.5,12.3,26.8,11.1,30.6,14.7,30.9,15.3,30.7,17.4,34.3,16.4,24.8,12.7,30.5,13.9,31.5,14.8,29.5,16.4,21.1,10.2,33.8,18.4,30.9,13.2,38.4,17.6,26.7,14.1,26.8,11.8,28.3,13.3,19.3,7.9,19.2,9.4,29.9,14.4,37.0,15.3,33.7,17.2,27.4,12.8,19.9,9.8,37.2,19.9,27.1,13.2,22.5,10.3,43.7,25.1,29.2,15.2,36.8,18.1,39.5,21.3,31.8,16.2,21.4,8.2,23.1,10.2,24.1,10.5,,,44.5,22.7,25.2,11.6,36.3,16.3,23.5,10.6,39.4,18.2,38.8,19.6,17.1,8.8,31.0,12.9,24.6,12.4,53.0,30.5,28.3,15.5,21.1,9.5,40.4,17.9,17.1,7.5,43.1,22.1,29.6,13.9,30.6,13.5,28.8,15.1,29.7,13.5,23.0,9.4,44.5,17.8,29.2,11.7,37.3,15.5,28.2,15.0,43.6,19.7,42.4,22.0,41.5,24.2',
'precip_2014' : '23.7,11.8,46.4,26.3,42.7,23.4,29.8,15.6,44.1,24.1,28.7,15.8,46.8,27.5,41.3,25.2,,19.2,31.1,15.7,21.8,12.2,30.5,15.5,34.6,20.6,36.7,20.8,27.2,15.8,31.4,16.4,30.0,15.6,34.3,18.4,17.9,8.9,50.5,31.8,35.1,20.1,39.9,20.7,29.8,15.9,34.2,20.2,32.6,17.7,23.9,12.8,23.9,15.5,41.2,23.8,43.7,26.8,26.2,12.8,35.1,18.6,36.1,21.7,,,41.9,25.4,38.9,21.8,32.8,18.7,26.6,12.0,32.5,17.0,37.9,21.7,,12.3,,20.7,35.3,19.6,27.3,14.8,35.9,18.7,32.4,18.5,37.7,21.5,35.6,19.8,56.7,31.9,41.1,22.1,28.0,15.5,36.4,20.7,50.7,29.0,26.1,15.3,32.4,16.5,36.2,18.4,39.2,21.9,41.3,24.8,40.1,21.9,27.8,15.7,30.0,13.6,33.2,18.9,30.0,17.0,24.2,12.4,33.8,18.6,32.2,17.7,34.1,18.8,29.0,15.8,34.2,17.7,37.0,20.4,17.8,8.7,21.6,11.8,43.9,22.4,30.9,17.1,36.8,21.0,29.8,15.6,24.7,12.9,43.4,25.1,33.4,17.4,27.9,15.1,57.8,35.1,36.5,19.7,43.9,24.4,41.9,25.2,43.1,24.3,19.4,9.5,27.8,14.0,24.1,12.8,,,50.4,29.9,30.2,15.6,33.7,16.6,25.8,14.7,43.8,23.1,48.9,27.4,21.5,11.4,34.8,17.3,27.1,15.6,72.5,46.0,35.1,19.5,22.1,12.2,42.2,25.0,15.5,7.3,42.1,25.6,34.1,18.6,29.8,15.8,31.8,18.3,30.3,15.8,27.4,14.4,39.9,17.8,32.6,15.6,37.7,20.1,32.5,17.0,45.5,28.6,37.1,23.4,58.8,36.9',
'precip_2015' : '23.3,12.8,31.0,19.1,33.4,19.7,22.8,13.8,40.4,22.1,28.9,15.7,37.8,22.7,37.0,20.0,,19.5,27.7,15.0,22.3,13.7,30.0,16.7,22.7,15.2,30.0,18.3,27.3,14.8,31.9,16.5,28.5,15.1,32.6,17.9,18.3,9.9,36.3,22.2,25.5,13.5,40.2,21.5,29.0,16.7,29.2,17.7,26.2,14.9,26.8,15.1,38.6,21.1,31.7,18.3,29.7,19.2,32.9,16.8,32.6,17.9,27.3,15.9,,,33.0,19.9,34.4,19.0,30.1,18.0,34.4,18.4,30.7,15.0,28.4,17.4,,17.4,,16.6,33.3,19.8,26.0,14.0,29.8,17.8,31.9,18.4,35.9,21.5,29.0,16.8,42.3,25.7,34.2,20.0,24.4,13.7,31.1,18.2,34.5,21.2,25.2,12.7,29.1,15.4,29.0,14.8,27.5,16.8,33.4,20.2,30.8,18.0,23.3,13.5,30.7,14.7,27.8,15.8,27.1,16.0,27.4,13.5,28.8,15.2,28.4,16.3,31.7,16.3,24.1,13.6,30.4,15.9,31.5,17.0,22.9,11.2,19.2,11.1,30.6,17.5,36.1,19.3,31.0,16.2,30.3,15.7,19.3,10.5,38.6,20.5,23.2,13.9,26.8,15.6,40.2,24.5,28.0,16.3,41.3,23.7,33.3,19.8,30.4,17.0,23.6,11.6,24.8,13.5,31.9,16.4,43.7,27.1,46.2,24.0,27.4,14.2,37.6,19.3,26.0,15.0,42.3,22.2,41.3,21.8,16.3,9.3,31.6,16.3,21.7,12.5,53.2,33.4,25.2,14.5,20.0,10.9,38.7,22.2,17.1,9.0,45.2,24.0,30.8,16.8,29.4,15.2,29.3,16.6,30.9,14.8,25.8,14.9,43.3,21.4,30.8,17.0,29.3,17.5,22.8,13.2,38.3,23.3,44.1,22.7,41.1,26.2'
}
allClean = []
for i in range(1992, 2016):
    x = f'precip_{i}'
    dictItem = data[x]
    removeNull = re.findall('[0-9]+\.[0-9]+', dictItem)
    # Isolates each number from original data excludes null values/pointless commas
    clean = []
    for i in removeNull:
        clean.append(float(i))
        # Changes string values to floats which can be used for calculations
    allClean.append(clean)
avgPrecip = []
for i in allClean:
    avg = stats.mean(i)
    avgPrecip.append(round(avg))


year = []
for i in range(1992, 2016):
    year.append(i)

df = pd.read_csv('fires_by_year.csv')
# Raw dataframe showing total wildfires in Colorrado by year, range 1992-2015
denRain = [0, 0, 0, 18.27, 10.25, 19.59, 15.93, 20.95, 14.55, 16.55, 7.48, 13.92, 14.67, 12.80, 8.64, 14.00, 10.23, 18.12, 12.86, 17.27, 10.11, 16.60, 18.77, 18.22]
# Rain data sourced from: 'http://www.globalwarmingdenver.com/tot_precip.html'

x = df['FIRE_YEAR']
y = df['COUNT(*)']
# Isoloating each dataframe column within a variable

yearsList = list(x)
fireList = list(y)
# Converting dataframes to lists for manipulation

rain = np.array(avgPrecip)
fires = np.array(fireList)
years = np.array(yearsList)
# Converting lists to numpy arrays for plotting compatibility

df2 = pd.read_csv('fire_types')
rolling_3 = []
for i in range(len(fires)):
    k = i + 3
    set = fires[i:k]
    tot = sum(set)
    fires_rolling_avg = int(round(tot/3))
    rolling_3.append(fires_rolling_avg)

r_rolling_3 = []
for i in range(len(rain)):
    k = i + 3
    set = rain[i:k]
    tot = sum(set)
    rain_rolling_avg = int(round(tot/3))
    r_rolling_3.append(rain_rolling_avg)


# Z SCORE ANALYSIS
zScoreRaw = sp.zscore(fires)
# Finds z-score

zScore = []
for i in zScoreRaw:
    a = i**2
    b = math.sqrt(a)
    zScore.append(b)
# Flips all negative list values to positive

tableData = [['# of Fires', 'Z-Score']]
for i in range(len(fires)):
        tableData.append([fires[i], zScore[i]])
print(tableData)