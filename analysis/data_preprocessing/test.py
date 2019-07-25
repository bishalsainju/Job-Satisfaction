import pandas as pd

a = [ ['My name is apple', 'My name is ball', 'My name is cat'],
      ['Hey, apple', 'Hey, ball', 'Hey, cat']]

# data_transposed = zip(a)
# df = pd.DataFrame(data_transposed, columns=["col1", "col2", "col3"])
# print(df.head())

df = pd.DataFrame.from_records(a)
df.columns = ['col1', 'col2', 'col3']
print(df.head())