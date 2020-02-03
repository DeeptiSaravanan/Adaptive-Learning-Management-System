from booky import bsearch
import pandas as pd

#dff = pd.DataFrame()
i = "Basics of Management"
df = bsearch(i)
print(df.head())
print("\n")
j = "Human Resource"
df1 = bsearch(j)
print(df1.head())
print("\n")
k = "Marketing Management"
df2 = bsearch(k)
print(df2.head())

