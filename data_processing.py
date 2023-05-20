import pandas as pd
import os
from collections import defaultdict

# ps:你应该只需要修改root_path这一个参数
root_path = '/Users/bytedance/Desktop/'
data_path = 'cars15/'  # 15辆车运行数据的文件夹
folder_path = root_path + data_path

# 创建新目录存结果
data_dir = os.path.join(root_path, 'processed_files')
if not os.path.exists(data_dir):
    os.mkdir(data_dir)

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
    car_list[int(car_id[2:]) - 1] = [x[1] for x in sorted_file_list]
# ------
for idx, car_files in enumerate(car_list):
    print('正在处理第', idx, '辆车...')
    file_names = car_files
    df_list = []
    for month, file_name in enumerate(file_names):
        print('  --正在读取第', month, '月的数据...')
        df = pd.read_excel(folder_path + file_name)
        df_list.append(df)
    df = pd.concat(df_list, ignore_index=True)
    print('该车辆数据shape：', df.shape)
    print('该车辆所有月份数据已读取，开始计算label...')

    # 标记充电状态的改变
    df['charge_count'] = ((df['充电状态'] == 1) & (df['充电状态'].shift(1) != 1)).cumsum()

    # 提取待计算充电量区间
    df_soc = df.query('充电状态 == 1 and 40 <= SOC <= 80')

    # 计算充电量，df_soc就是最后的数据
    df_soc = df_soc.reset_index(drop=True)
    accumulated_current = df_soc['总电流'].groupby(df_soc['charge_count']).apply(lambda x: abs(x.cumsum()) / 180)
    accumulated_current.index = df_soc.index  # 重置index
    df_soc['accumulated_current'] = accumulated_current  #

    # 将DF存为CSV
    car_name = 'CL'+str(idx)+'.csv'
    df_soc.to_csv(os.path.join(data_dir, car_name), index=False)
    print('该车辆label已经计算完成，数据已保存')
print('所有车辆计算完成')





