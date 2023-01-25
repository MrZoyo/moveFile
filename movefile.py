import os
import shutil
import PySimpleGUI as sg

sg.theme('DarkAmber')  # Add a touch of color
# All the stuff inside your window.
layout = [[sg.Text('选择源目录(例如：D:\\data\\images)')],

          [sg.InputText(), sg.FolderBrowse()],
          [sg.Text('选择输出目录(例如：D:\\data\\images)')],
          [sg.InputText(), sg.FolderBrowse()],
          [sg.Text('文件类型(例如：“.png”)'), sg.Button('全部类型'), sg.Button('输入类型')],
          [sg.InputText(default_text='.png', key='-IN-', use_readonly_for_disable=False)],
          [sg.Radio('复制', "RADIO1", default=True, key='复制'),
           sg.Radio('移动', "RADIO1", key='移动'),
           sg.InputText(default_text='True', visible=False, key='-OUT-')],
          [sg.Button('执行'), sg.Button('关闭')]]


# Event Loop to process "events" and get the "values" of the inputs
def move_files(src_dir, dest_dir, file_type, move_or_copy, all_type):
    count = 0
    # 遍历源目录中的所有文件和文件夹
    for root, dirs, files in os.walk(src_dir):
        # 遍历所有文件
        for file in files:
            # 如果文件是指定类型的文件 或者 全部类型
            if file.endswith(file_type) or all_type:
                # 获取文件的完整路径
                src_path = os.path.join(root, file)
                # 获取文件所在文件夹的名称
                folder_name = os.path.basename(root)
                # 构造新的文件名
                new_file_name = folder_name + '_' + file
                # 构造目标路径
                dest_path = os.path.join(dest_dir, new_file_name)
                # 如果原路径和目标路径不一样
                if src_path != dest_path:
                    # 移动文件
                    if move_or_copy == '移动':
                        shutil.move(src_path, dest_path)
                    # 复制文件
                    else:
                        shutil.copy(src_path, dest_path)
                    count += 1

    return count


# Create the Window
window = sg.Window('文件夹剥离 v0.0.4 by MrZoyo', layout)

while True:
    event, values = window.read()
    if event in (None, '关闭', sg.WIN_CLOSED):  # if user closes window or clicks cancel
        break
    if event == '执行':
        print(values)
        src_dir = values[0]
        dest_dir = values[1]
        file_type = values['-IN-']
        # 根据textout框内容判断是否是全部类型
        all_type = True if values['-OUT-'] == 'True' else False
        if values['复制']:
            # use copy
            count = move_files(src_dir, dest_dir, file_type, '复制', all_type)

        if values['移动']:
            # use move
            count = move_files(src_dir, dest_dir, file_type, '移动', all_type)

        sg.popup('成功处理了{}个文件'.format(count))
        print('已将', count, '个文件从', src_dir, '处理到', dest_dir)

    # 当选择全部类型时，禁用文件类型输入框
    if event == '全部类型':
        window['-IN-'].update(readonly=True)
        window['-OUT-'].update('True')
    # 当选择输入类型时，启用文件类型输入框
    if event == '输入类型':
        window['-IN-'].update(readonly=False)
        window['-OUT-'].update('False')

window.close()
