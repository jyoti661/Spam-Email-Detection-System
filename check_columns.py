import pandas as pd

df = pd.read_csv("spam.csv", encoding="latin-1")
print("Columns found in CSV:", df.columns.tolist())
