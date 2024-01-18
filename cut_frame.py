import csv
file_csv = 'Kento_MOMOTA_CHOU_Tien_Chen_Fuzhou_Open_2019_Finals.mp4groundtruth.csv'
remained_lines = 15000
target = "break"
def process_csv(file_path):
    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = list(csv.reader(file))

        if len(reader) < 15000:
            print("lines less than 15000.")
            return

        if reader[remained_lines-1][0] == target:
            new_content = reader[:remained_lines]
        else:
            # 往上和往下搜索最近的 "break" 行
            upper_index = lower_index = remained_lines - 1
            while upper_index >= 0 and reader[upper_index][0] != target:
                upper_index -= 1
            while lower_index < len(reader) and reader[lower_index][0] != target:
                lower_index += 1

            # 確定要保留的行數
            if (remained_lines-1 - upper_index) <= (lower_index - remained_lines-1):
                nearest_index = upper_index
                print("nearest index is upper_index: ", upper_index)
                print(reader[upper_index][0]+1)
            else:
                nearest_index = lower_index
                print("nearest index is lower_index: ", lower_index)
                print(reader[lower_index][0]+1)
            new_content = reader[:nearest_index + 1]

        # 寫入新檔案
        with open('processed_' + file_path, 'w', newline='', encoding='utf-8') as new_file:
            writer = csv.writer(new_file)
            writer.writerows(new_content)

process_csv(file_csv)
