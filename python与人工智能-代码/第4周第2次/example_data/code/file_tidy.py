import os
import shutil

def organize_folder(folder):
    if not os.path.isdir(folder):
        print("错误：路径不存在或不是文件夹")
        return

    # 分类规则（扩展名 -> 目标子文件夹名）
    rule = {
        '.jpg': 'images', '.jpeg': 'images', '.png': 'images', '.gif': 'images',
        '.txt': 'docs', '.docx': 'docs', '.pdf': 'docs',
        '.py': 'code', '.java': 'code', '.js': 'code', '.html': 'code',
        '.zip': 'zips', '.rar': 'zips', '.7z': 'zips',
    }

    # 收集待移动的文件
    files_to_move = []  # 列表元素: (原路径, 目标文件夹名)
    ext_set = set()

    for item in os.listdir(folder):
        src = os.path.join(folder, item)
        if not os.path.isfile(src):
            continue
        _, ext = os.path.splitext(item)
        ext = ext.lower()
        ext_set.add(ext)

        # 确定分类，默认进入 'others'
        target_sub = rule.get(ext, 'others')
        files_to_move.append((src, target_sub))

    # 输出统计
    print(f"共扫描文件数：{len(files_to_move)}")
    print(f"出现的扩展名：{ext_set}\n")

    # 移动文件
    for src, target_sub in files_to_move:
        target_dir = os.path.join(folder, target_sub)
        os.makedirs(target_dir, exist_ok=True)

        filename = os.path.basename(src)
        dst = os.path.join(target_dir, filename)

        # 重名处理
        if os.path.exists(dst):
            base, ext = os.path.splitext(filename)
            count = 1
            while os.path.exists(os.path.join(target_dir, f"{base}({count}){ext}")):
                count += 1
            dst = os.path.join(target_dir, f"{base}({count}){ext}")

        os.rename(src, dst)
        #shutil.move(src, dst)
        print(f"移动：{src} -> {dst}")

    print("\n整理完成！")

if __name__ == "__main__":
    #path = input("请输入文件夹路径：").strip()
    path = "./example_data"
    organize_folder(path)