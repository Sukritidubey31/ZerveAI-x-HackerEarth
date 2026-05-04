import pandas as pd 

data['timestamp'] = pd.to_datetime(data['timestamp'], format='ISO8601', utc=True)
data['created_at'] = pd.to_datetime(data['created_at'], format='ISO8601', utc=True)

data['date']  = data['timestamp'].dt.date
data['hour'] = data['timestamp'].dt.hour
data['day_of_week'] = data['timestamp'].dt.day_name()

keep_cols = [
    'person_id', 'event', 'timestamp', 'date', 'hour', 'day_of_week',
    'prop_session_id', 'prop_user_id', 'prop_userId',
    'prop_surface', 'prop_tool_name',
    'prop_credit_amount', 'prop_credits_used',
    'prop_$pathname', 'prop_$device_type',
    'prop_$browser', 'prop_$os',
    'prop_$geoip_country_name', 'prop_$referring_domain'
]

data_clean = data[keep_cols].copy()

print("Clean shape")
print(data_clean.shape)
print("Null counts")
print(data_clean.isnull().sum())