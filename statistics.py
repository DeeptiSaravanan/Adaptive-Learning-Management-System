import pandas as pd
import scipy.stats
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(color_codes=True)


basics = pd.read_csv('C:\\Users\\shwet\\Desktop\\E-learner-Shwetha\\basicsdata.csv')
mm = pd.read_csv('C:\\Users\\shwet\\Desktop\\E-learner-Shwetha\\mmdata.csv')
hr = pd.read_csv('C:\\Users\\shwet\\Desktop\\E-learner-Shwetha\\hrdata.csv')
print(scipy.stats.describe(basics["Time"], ddof=1, bias=False))
print(scipy.stats.describe(basics["Mode"], ddof=1, bias=False))
print(scipy.stats.describe(basics["Level"], ddof=1, bias=False))
print(scipy.stats.describe(mm["Time"], ddof=1, bias=False))
print(scipy.stats.describe(mm["Mode"], ddof=1, bias=False))
print(scipy.stats.describe(mm["Level"], ddof=1, bias=False))
print(scipy.stats.describe(hr["Time"], ddof=1, bias=False))
print(scipy.stats.describe(hr["Mode"], ddof=1, bias=False))
print(scipy.stats.describe(hr["Level"], ddof=1, bias=False))

x=np.array(basics["Time"])
sns.distplot(x,color='g');
plt.xlabel('Time')
plt.ylabel('Normalized Count')
plt.title('Basics of Management')
plt.show()

x=np.array(mm["Time"])
sns.distplot(x,color='r');
plt.xlabel('Time')
plt.ylabel('Normalized Count')
plt.title('Marketing Management')
plt.show()

x=np.array(hr["Time"])
sns.distplot(x,color='b');
plt.xlabel('Time')
plt.ylabel('Normalized Count')
plt.title('Human Resource Management')
plt.show()
