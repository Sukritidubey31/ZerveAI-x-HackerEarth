data_clean['user_id'] = (data_clean['prop_user_id']
                        .fillna(data_clean['prop_userId'])
                        .fillna(data_clean['person_id']))

print("Unique Users")
print(data_clean['user_id'].nunique())
print("Unique Person ID")
print(data_clean['person_id'].nunique())