"""
Gneiss-Engine 文件操作示例

此脚本演示了 Gneiss-Engine 中文件工具的各种功能，包括：
- 图像查找和筛选
- 目录管理
- 文件命名和重命名
- 文件移动和删除
- 文件分析和统计
"""

import os
import sys
from pathlib import Path
import time

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

# Import Gneiss-Engine utilities
from gneiss.utils.file_utils import (
    apply_rename,
    batch_rename,
    generate_sequential_names,
    get_files_by_extension,
    find_images,
    ensure_directory_exists,
    get_unique_filename,
    generate_output_filename,
    move_files_with_progress,
    remove_files_with_progress,
    group_files_by_extension,
    get_file_size,
    filter_files_by_pattern,
)


def print_header(title: str) -> None:
    """打印带分隔线的标题"""
    print("\n" + "=" * 60)
    print(f" {title} ".center(60, "="))
    print("=" * 60)


def demo_find_images():
    """演示图像查找功能"""
    print_header("1. 图像查找功能演示")
    
    # 示例目录
    current_dir = Path(__file__).parent
    sample_dir = current_dir / "sample_images"
    
    if not sample_dir.exists():
        print(f"警告: 示例图像目录不存在: {sample_dir}")
        print("请先运行: python examples/create_sample_images.py")
        return
    
    print(f"\n在目录 {sample_dir} 中查找图像:")
    
    # 非递归查找所有图像
    print("\n1.1 非递归查找所有图像:")
    images = find_images(sample_dir, recursive=False)
    print(f"找到 {len(images)} 张图像")
    for img in images[:3]:  # 只显示前3个
        print(f"  - {Path(img).name}")
    if len(images) > 3:
        print(f"  - ...等 {len(images) - 3} 个文件")
    
    # 递归查找特定格式图像
    print("\n1.2 递归查找特定格式图像 (JPG):")
    jpg_images = find_images(sample_dir, recursive=True, extensions=[".jpg"])
    print(f"找到 {len(jpg_images)} 张 JPG 图像")
    for img in jpg_images[:3]:
        print(f"  - {Path(img).name}")
    
    # 使用通用文件扩展名搜索
    print("\n1.3 使用通用文件扩展名搜索:")
    png_files = get_files_by_extension(sample_dir, [".png"], recursive=True)
    print(f"找到 {len(png_files)} 个 PNG 文件")


def demo_directory_management():
    """演示目录管理功能"""
    print_header("2. 目录管理功能演示")
    
    current_dir = Path(__file__).parent
    test_base = current_dir / "test_operations"
    
    # 创建单级目录
    print("\n2.1 创建单级目录:")
    simple_dir = test_base / "simple_dir"
    ensure_directory_exists(simple_dir)
    print(f"创建目录: {simple_dir}")
    
    # 创建多级嵌套目录
    print("\n2.2 创建多级嵌套目录:")
    nested_dir = test_base / "level1" / "level2" / "level3"
    ensure_directory_exists(nested_dir)
    print(f"创建嵌套目录: {nested_dir}")
    
    # 验证目录存在
    print("\n2.3 验证目录存在:")
    if simple_dir.exists() and nested_dir.exists():
        print("✓ 所有目录创建成功")
    else:
        print("✗ 目录创建失败")
    
    print(f"\n测试目录路径: {test_base}")


def demo_file_naming():
    """演示文件命名功能"""
    print_header("3. 文件命名功能演示")
    
    current_dir = Path(__file__).parent
    test_base = current_dir / "test_operations"
    ensure_directory_exists(test_base)
    
    # 演示唯一文件名生成
    print("\n3.1 生成唯一文件名:")
    
    # 创建一个测试文件
    base_file = test_base / "test_image.jpg"
    with open(base_file, "w") as f:
        f.write("test")
    
    # 获取唯一文件名
    unique1 = get_unique_filename(base_file)
    print(f"原始文件名: {base_file.name}")
    print(f"唯一文件名: {unique1.name}")
    
    # 创建重复文件，再次测试
    with open(test_base / "test_image (1).jpg", "w") as f:
        f.write("test")
    
    unique2 = get_unique_filename(base_file)
    print(f"再次生成唯一文件名: {unique2.name}")
    
    # 演示输出文件名生成
    print("\n3.2 生成输出文件名:")
    input_file = test_base / "input_image.jpg"
    output_dir = test_base / "output"
    
    # 基本使用
    output1 = generate_output_filename(input_file, output_dir)
    print(f"基本输出文件名: {output1}")
    
    # 添加后缀
    output2 = generate_output_filename(input_file, output_dir, suffix="_processed")
    print(f"带后缀的输出文件名: {output2}")
    
    # 更改扩展名
    output3 = generate_output_filename(input_file, output_dir, extension=".png")
    print(f"更改扩展名的输出文件名: {output3}")
    
    # 同时添加后缀和更改扩展名
    output4 = generate_output_filename(input_file, output_dir, suffix="_resized", extension=".webp")
    print(f"带后缀和新扩展名的输出文件名: {output4}")


def demo_batch_rename():
    """演示批量重命名功能"""
    print_header("4. 批量重命名功能演示")
    
    current_dir = Path(__file__).parent
    test_base = current_dir / "test_operations"
    rename_dir = test_base / "rename_test"
    ensure_directory_exists(rename_dir)
    
    # 创建测试文件
    test_files = []
    for i in range(3):
        file_path = rename_dir / f"old_file_{i}.txt"
        with open(file_path, "w") as f:
            f.write(f"Test file {i}")
        test_files.append(str(file_path))
    
    print("\n4.1 创建的测试文件:")
    for file in test_files:
        print(f"  - {Path(file).name}")
    
    # 基本重命名（非正则）
    print("\n4.2 基本字符串替换重命名:")
    rename_map = batch_rename(
        files=test_files,
        pattern="old",
        replacement="new",
        use_regex=False
    )
    
    print("重命名映射:")
    for original, new in rename_map.items():
        print(f"  - {Path(original).name} → {Path(new).name}")
    
    # 应用重命名
    results = apply_rename(rename_map)
    
    # 检查结果
    print("\n4.3 重命名结果:")
    renamed_files = list(rename_dir.glob("*.txt"))
    for file in renamed_files:
        print(f"  - {file.name}")
    
    # 使用正则表达式重命名
    print("\n4.4 使用正则表达式重命名:")
    files_to_rename = [str(f) for f in renamed_files]
    regex_rename_map = batch_rename(
        files=files_to_rename,
        pattern=r"new_file_(\d+)",
        replacement=r"document_\1_v1",
        use_regex=True
    )
    
    print("正则重命名映射:")
    for original, new in regex_rename_map.items():
        print(f"  - {Path(original).name} → {Path(new).name}")
    
    # 应用正则重命名
    apply_rename(regex_rename_map)
    
    # 显示最终结果
    print("\n4.5 最终文件列表:")
    final_files = list(rename_dir.glob("*.txt"))
    for file in final_files:
        print(f"  - {file.name}")


def demo_file_operations():
    """演示文件移动和删除操作"""
    print_header("5. 文件移动和删除操作演示")
    
    current_dir = Path(__file__).parent
    test_base = current_dir / "test_operations"
    source_dir = test_base / "source"
    dest_dir = test_base / "destination"
    
    ensure_directory_exists(source_dir)
    ensure_directory_exists(dest_dir)
    
    # 创建测试文件
    test_files = []
    for i in range(3):
        file_path = source_dir / f"test_file_{i}.txt"
        with open(file_path, "w") as f:
            f.write(f"Content {i}")
        test_files.append(str(file_path))
    
    print("\n5.1 创建的源文件:")
    for file in test_files:
        print(f"  - {Path(file).name}")
    
    # 演示文件移动
    print("\n5.2 移动文件:")
    move_results = move_files_with_progress(test_files, str(dest_dir))
    
    # 检查移动结果
    success_count = sum(1 for success in move_results.values() if success)
    print(f"\n移动结果: 成功 {success_count}/{len(move_results)}")
    
    # 显示目标目录中的文件
    print("\n5.3 目标目录中的文件:")
    dest_files = list(dest_dir.glob("*.txt"))
    for file in dest_files:
        print(f"  - {file.name}")
    
    # 演示文件删除
    print("\n5.4 删除文件:")
    files_to_delete = [str(f) for f in dest_files[:2]]  # 只删除前两个文件
    delete_results = remove_files_with_progress(files_to_delete)
    
    # 检查删除结果
    deleted_count = sum(1 for success in delete_results.values() if success)
    print(f"\n删除结果: 成功 {deleted_count}/{len(delete_results)}")
    
    # 显示剩余文件
    print("\n5.5 剩余文件:")
    remaining_files = list(dest_dir.glob("*.txt"))
    for file in remaining_files:
        print(f"  - {file.name}")


def demo_file_analysis():
    """演示文件分析功能"""
    print_header("6. 文件分析功能演示")
    
    current_dir = Path(__file__).parent
    sample_dir = current_dir / "sample_images"
    
    if not sample_dir.exists():
        print(f"警告: 示例图像目录不存在: {sample_dir}")
        print("使用测试目录代替")
        
        # 创建一些不同类型的测试文件
        test_base = current_dir / "test_operations"
        test_dir = test_base / "analysis_test"
        ensure_directory_exists(test_dir)
        
        # 创建各种类型的测试文件
        file_types = [".jpg", ".png", ".txt", ".pdf", ".docx"]
        for ext in file_types:
            for i in range(2):
                file_path = test_dir / f"test_file_{i}{ext}"
                with open(file_path, "w") as f:
                    f.write(f"Test content for {ext}")
        
        sample_dir = test_dir
    
    # 获取所有文件
    all_files = [str(f) for f in sample_dir.glob("*.*")]
    
    print(f"\n分析目录: {sample_dir}")
    print(f"总文件数: {len(all_files)}")
    
    # 按扩展名分组
    print("\n6.1 按扩展名分组:")
    grouped = group_files_by_extension(all_files)
    
    for ext, files in grouped.items():
        print(f"  - {ext}: {len(files)} 个文件")
    
    # 获取文件大小
    print("\n6.2 文件大小信息:")
    for file_path in all_files[:3]:  # 只显示前3个
        size_bytes = get_file_size(file_path)
        size_human = get_file_size(file_path, human_readable=True)
        print(f"  - {Path(file_path).name}: {size_bytes} 字节 ({size_human})")
    
    # 筛选文件
    print("\n6.3 筛选文件:")
    # 基本筛选
    filtered = filter_files_by_pattern(all_files, "test")
    print(f"包含'test'的文件: {len(filtered)} 个")
    
    # 正则筛选
    if any(f.endswith('.jpg') or f.endswith('.png') for f in all_files):
        image_files = filter_files_by_pattern(all_files, r"\.(jpg|png)$", use_regex=True)
        print(f"JPG/PNG图像文件: {len(image_files)} 个")
    
    # 生成顺序文件名
    print("\n6.4 生成顺序文件名:")
    seq_names = generate_sequential_names(
        directory=sample_dir,
        base_name="image_",
        extension="jpg",
        start_number=100,
        padding=4
    )
    
    print("生成的前5个顺序文件名:")
    for name in seq_names[:5]:
        print(f"  - {name}")


def demo_real_world_workflow():
    """演示真实世界的工作流程"""
    print_header("7. 真实世界工作流程演示")
    
    current_dir = Path(__file__).parent
    sample_dir = current_dir / "sample_images"
    
    if not sample_dir.exists():
        print(f"警告: 示例图像目录不存在: {sample_dir}")
        print("请先运行: python examples/create_sample_images.py")
        return
    
    print("\n执行图像处理准备工作流程:")
    print("1. 查找所有图像...")
    images = find_images(sample_dir, recursive=True)
    print(f"   找到 {len(images)} 张图像")
    
    # 创建输出目录结构
    output_base = current_dir / "processed_images"
    print("\n2. 创建输出目录结构...")
    output_dirs = {
        "resized": output_base / "resized",
        "converted": output_base / "converted",
        "backups": output_base / "backups"
    }
    
    for dir_path in output_dirs.values():
        ensure_directory_exists(dir_path)
        print(f"   创建目录: {dir_path.relative_to(current_dir)}")
    
    # 按类型分组图像
    print("\n3. 按图像类型分组...")
    grouped = group_files_by_extension(images)
    for ext, files in grouped.items():
        print(f"   {ext}: {len(files)} 个文件")
    
    # 生成输出文件名示例
    print("\n4. 生成输出文件名示例:")
    if images:
        sample_image = Path(images[0])
        resized_path = generate_output_filename(
            sample_image,
            output_dirs["resized"],
            suffix="_800x600"
        )
        
        converted_path = generate_output_filename(
            sample_image,
            output_dirs["converted"],
            extension=".webp"
        )
        
        print(f"   原始文件名: {sample_image.name}")
        print(f"   调整大小后: {resized_path.relative_to(output_base)}")
        print(f"   格式转换后: {converted_path.relative_to(output_base)}")
    
    print("\n工作流程准备完成! 现在可以使用BatchProcessor处理这些图像了。")
    print("示例: python examples/batch_processing.py")


def cleanup_test_files():
    """清理测试文件"""
    current_dir = Path(__file__).parent
    test_base = current_dir / "test_operations"
    
    if test_base.exists():
        print("\n清理测试文件...")
        import shutil
        try:
            shutil.rmtree(test_base)
            print(f"✓ 已清理测试目录: {test_base}")
        except Exception as e:
            print(f"✗ 清理失败: {e}")


def main():
    """主函数"""
    print("Gneiss-Engine 文件操作示例")
    print("=========================")
    
    try:
        # 运行各个演示
        demo_find_images()
        demo_directory_management()
        demo_file_naming()
        demo_batch_rename()
        demo_file_operations()
        demo_file_analysis()
        demo_real_world_workflow()
        
        # 询问是否清理测试文件
        cleanup = input("\n是否清理测试文件? (y/n): ")
        if cleanup.lower() == 'y':
            cleanup_test_files()
        
        print("\n所有演示完成!")
        
    except KeyboardInterrupt:
        print("\n\n操作被用户中断")
    except Exception as e:
        print(f"\n发生错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n感谢使用 Gneiss-Engine!")


if __name__ == "__main__":
    main()