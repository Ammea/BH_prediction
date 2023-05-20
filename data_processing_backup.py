import pandas as pd
import os
from collections import defaultdict
root_path = '/Users/bytedance/Desktop/'
data_path = 'cars15/'  # 15辆车运行数据的文件夹
folder_path = root_path+data_path

# 按照先车辆再月份的顺序获取文件名，car_list按顺序保存了15辆车的每个月数据
# ------
car_dict = defaultdict(list)
file_names = sorted(os.listdir(folder_path))
for file_name in file_names:
    car_id, month = file_name.split('_')[:2]
    car_dict[car_id].append((month, file_name))
car_list = [[] for _ in range(15)]
for car_id, file_list in car_dict.items():
    sorted_file_list = sorted(file_list, key=lambda x: x[0][:6])
    car_list[int(car_id[2:])-1]=[x[1] for x in sorted_file_list]
# ------

file_names=car_list[0][:2]
df_list = []
for file_name in file_names:
    print('zaiduqu')
    df = pd.read_excel(folder_path+file_name)
    df_list.append(df)
df = pd.concat(df_list, ignore_index=True)
print(df.shape)

# df['charge_count'] = 0
#
# count = 0
#
# previous_status = None
#
# for index, row in df.iterrows():
#     status = row['充电状态']
#
#     if status == 1 and (previous_status != 1 or previous_status is None):
#         count += 1
#
#     df.loc[index, 'charge_count'] = count
#     previous_status = status
df['charge_count'] = ((df['充电状态'] == 1) & (df['充电状态'].shift(1) != 1)).cumsum()
df_soc = df.query('充电状态 == 1 and 40 <= SOC <= 80')

df_soc = df_soc.reset_index(drop=True)
# print(df_soc.index)
# print(df_soc['总电流'].groupby(df_soc['charge_count']).apply(lambda x: x.cumsum()).index)
# ak= df_soc['总电流'].groupby(df_soc['charge_count']).apply(lambda x: abs(x.cumsum())/180)

accumulated_current = df_soc['总电流'].groupby(df_soc['charge_count']).apply(lambda x: abs(x.cumsum())/180)

accumulated_current.index = df_soc.index  # 重置index

df_soc['accumulated_current'] = accumulated_current  # 然后加入df
# df_soc['ak']=ak

a=1

