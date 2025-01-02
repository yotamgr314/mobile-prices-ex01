# Yotam_LastName_ID

## Mobile Phone Price Analysis

### Prerequisites
```python
# Import necessary libraries
import pandas as pd
import numpy as np
```

### Task 1

#### 1. Load the data into a Pandas Dataframe
```python
# Load the dataset
file_path = "/content/mobile_price_1.csv"
data = pd.read_csv(file_path)
data.head()  # Display the first few rows
```

#### 2. Identify nominal and ordinal categorical features
Nominal: `bluetooth`, `screen`, `sim`, `wifi`, `cores`, `speed`
Ordinal: `gen`

#### 3. Add a column for total screen resolution
```python
data['resolution'] = data['px_width'] * data['px_height']
data.head()
```

#### 4. Add a column for DPI of screen width
```python
data['DPI_w'] = data['px_width'] / (data['sc_w'] if data['sc_w'] > 0 else 1)
data['DPI_w'].fillna(0, inplace=True)  # Handle NaN values
data['DPI_w'].replace([np.inf, -np.inf], 0, inplace=True)  # Handle infinite values
data.head()
```

#### 5. Add a column for call ratio
```python
data['call_ratio'] = data['battery_power'] / (data['talk_time'] if data['talk_time'] > 0 else 1)
data['call_ratio'].fillna(0, inplace=True)  # Handle NaN values
data['call_ratio'].replace([np.inf, -np.inf], 0, inplace=True)  # Handle infinite values
data.head()
```

#### 6. Convert memory to GB
```python
data['memory'] = data['memory'] / 1024  # Convert MB to GB
data.head()
```

#### 7. Include the output of the `describe()` function
```python
# Display statistics for the dataset
data.describe()
```

#### 8. Convert features to categorical series
```python
categorical_columns = ['speed', 'screen', 'cores']
for col in categorical_columns:
    data[col] = data[col].astype('category')
data.dtypes  # Verify the types
```

### Task 2

#### 1. Count phones with no camera
```python
no_camera_count = data[(data['f_camera'].isna()) & (data['camera'].isna())].shape[0]
no_camera_count
```

#### 2. Average battery power for single-sim phones with high-resolution cameras
```python
avg_battery_power = data[
    (data['sim'] == 'Single') & ((data['camera'] > 12) | (data['f_camera'] > 12))
]['battery_power'].mean()
avg_battery_power
```

#### 3. Most expensive phone meeting criteria
```python
criteria_phone = data[
    (data['wifi'] == 'none') & (data['screen'] == 'Touch') & (data['mobile_wt'] > 145)
].sort_values(by='price', ascending=False).iloc[0]
criteria_phone[['id', 'price']]
```

#### 4. Pivot table for Bluetooth per generation
```python
data['ram_quartile'] = pd.qcut(data['ram'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
bluetooth_pivot = pd.pivot_table(
    data,
    values='bluetooth',
    index='gen',
    columns='ram_quartile',
    aggfunc=lambda x: (x == 'Yes').mean() * 100
)
bluetooth_pivot
```

#### 5. Create new dataset from medium-speed phones
```python
medium_speed_phones = data[data['speed'] == 'medium'].sample(frac=0.5, random_state=42)
selected_columns = ['id', 'battery_power', 'ram', 'talk_time', 'bluetooth', 'cores', 'sim', 'memory', 'price']
new_dataset = medium_speed_phones[selected_columns]
new_dataset.head()
```

#### 6. Maximum talk time with 3 phones
```python
max_talk_phones = new_dataset.nlargest(3, 'talk_time')
max_talk_time = max_talk_phones['talk_time'].sum()
max_talk_phones[['id', 'talk_time']]
max_talk_time
```

### Notes
- Ensure clean and readable code.
- Remove unnecessary test code before submission.
- Save the notebook as `Yotam_LastName_ID_Mobile_Prices.ipynb`.
