# Draw a title and some text to the app:

'''
# This is the document title

This is some _markdown_.  --> This is dot string that's why it will not show
'''

import pandas as pd
df = pd.DataFrame({'col1': [1,2,3]})
df  # 👈 Draw the dataframe

x = 10
'x', x  # 👈 Draw the string 'x' and then the value of x

# Also works with most supported chart types
import matplotlib.pyplot as plt
import numpy as np

arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
# ax.hist(arr, bins=20)
ax.hist(arr, bins=3)
fig  # 👈 Draw a Matplotlib chart

'# Pakistan zinda bad' # --> Idenetifies on its own that it is a markdown
# hello world