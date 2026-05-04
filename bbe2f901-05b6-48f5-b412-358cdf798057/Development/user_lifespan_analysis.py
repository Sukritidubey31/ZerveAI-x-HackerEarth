import pandas as pd
print(user_stats['lifespan_days'].describe())
print("How many users by lifespan")
print(pd.cut(user_stats['lifespan_days'], bins=[0,1,3,7,14,30,999], 
             labels=['1d','1-3d','3-7d','7-14d','14-30d','30d+']).value_counts().sort_index())