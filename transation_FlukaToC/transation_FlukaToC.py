import re
import numpy as np

def convert_fluka_to_c_array_advanced(input_filename, output_filename, array_name="heat_deposition", elements_per_line=6):
    """
    将FLUKA输出文件转换为C语言风格的三维数组格式（增强版）
    
    参数:
    input_filename: 输入文件名
    output_filename: 输出文件名
    array_name: 数组名称
    elements_per_line: 每行显示的元素数量
    """
    
    # 定义参数
    x_min, x_max = -10, 10
    y_min, y_max = -10, 10
    z_min, z_max = -14, 14
    
    nx, ny, nz = 20, 20, 28
    dx, dy, dz = 1, 1, 1
    
    # 初始化三维数组
    data_3d = np.zeros((nx, ny, nz))
    
    # 读取文件
    with open(input_filename, 'r') as f:
        lines = f.readlines()
    
    # 查找数据开始位置
    data_start_line = 0
    for i, line in enumerate(lines):
        if "Data follow in a matrix" in line:
            data_start_line = i + 1
            break
    
    # 如果没有找到标记，则从第16行开始
    if data_start_line == 0:
        data_start_line = 15
    
    # 提取数据行
    data_lines = lines[data_start_line:]
    
    # 提取所有数值数据
    all_values = []
    for line in data_lines:
        # 跳过空行
        if not line.strip():
            continue
            
        # 使用正则表达式提取科学计数法数值
        values = re.findall(r'[-]?\d\.\d+E[+-]\d+', line)
        all_values.extend(values)
    
    # 将字符串转换为浮点数
    all_values = [float(val) for val in all_values]
    
    print(f"总共提取了 {len(all_values)} 个数据点")
    print(f"期望的数据点数量: {nx * ny * nz} = {nx * ny * nz}")
    
    # 检查数据点数量是否匹配
    if len(all_values) != nx * ny * nz:
        print(f"警告: 数据点数量不匹配! 期望 {nx * ny * nz}, 实际 {len(all_values)}")
        # 如果数据点不够，用0填充
        if len(all_values) < nx * ny * nz:
            all_values.extend([0.0] * (nx * ny * nz - len(all_values)))
            print(f"已用0填充 {nx * ny * nz - len(all_values)} 个数据点")
        # 如果数据点太多，截断
        else:
            all_values = all_values[:nx * ny * nz]
            print(f"已截断 {len(all_values) - nx * ny * nz} 个数据点")
    
    # 将一维数据填充到三维数组
    # 顺序: 先改变x，后改变y，最后改变z
    idx = 0
    for iz in range(nz):
        for iy in range(ny):
            for ix in range(nx):
                data_3d[ix, iy, iz] = all_values[idx]
                idx += 1
    
    # 写入C语言风格的三维数组
    with open(output_filename, 'w') as f:
        # 写入数组声明
        f.write(f"real {array_name}[{nx}][{ny}][{nz}] = {{\n")
        
        # 遍历x维度
        for ix in range(nx):
            f.write(f"  {{ /* X index {ix} */\n")
            
            # 遍历y维度
            for iy in range(ny):
                f.write(f"    {{ /* Y index {iy} */\n")
                f.write("      ")
                
                # 遍历z维度，每行指定数量的元素
                for iz in range(nz):
                    # 格式化数值为科学计数法，保留6位小数
                    value = data_3d[ix, iy, iz]
                    formatted_value = "{:13.6e}".format(value)
                    
                    f.write(formatted_value)
                    
                    # 添加逗号（除了最后一个元素）
                    if iz < nz - 1:
                        f.write(", ")
                    
                    # 每指定数量的元素换行
                    if (iz + 1) % elements_per_line == 0 and iz < nz - 1:
                        f.write("\n      ")
                
                f.write("\n    }")
                
                # 添加逗号（除了最后一个y元素）
                if iy < ny - 1:
                    f.write(",")
                f.write("\n")
            
            f.write("  }")
            
            # 添加逗号（除了最后一个x元素）
            if ix < nx - 1:
                f.write(",")
            f.write("\n")
        
        # 结束数组
        f.write("};\n")
    
    print(f"C语言风格的三维数组已成功保存到 {output_filename}")
    print(f"数组维度: [{nx}][{ny}][{nz}]")
    print(f"每行显示元素数量: {elements_per_line}")

# 使用示例
if __name__ == "__main__":
    input_file = "pro001_fort_0.25.29"
    output_file = "heat_deposition_array_sf_2.5mm.c"
    
    # 可以调整每行显示的元素数量
    convert_fluka_to_c_array_advanced(input_file, output_file, array_name="heat_deposition", elements_per_line=6)