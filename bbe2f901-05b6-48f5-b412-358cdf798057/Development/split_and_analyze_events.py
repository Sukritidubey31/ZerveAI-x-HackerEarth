web_events = data_clean[data_clean['prop_session_id'].notna()].copy()
backend_events = data_clean[data_clean['prop_session_id'].isna()].copy()

print("Web events")
print(len(web_events))
print("Backend events")
print(len(backend_events))

print("Top backend events")
print(backend_events['event'].value_counts().head(10))

print("Top web events")
print(web_events['event'].value_counts().head(10))