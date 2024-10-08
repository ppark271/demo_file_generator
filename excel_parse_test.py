import pandas as pd

d = pd.read_excel("Cap Event Shell.xlsx", skiprows=10)

fc = d["Fund Code"]
for i in fc:
    print(i)

ipg = d["Investment Proceeds Gross"]
for i in ipg:
    print(i)

