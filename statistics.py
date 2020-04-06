import pandas as pd
import scipy.stats
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