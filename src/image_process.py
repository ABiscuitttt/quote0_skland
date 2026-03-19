from PIL import Image


def webp_add_white_background(input_path, output_path):
    # 打开WebP图片
    img = Image.open(input_path)

    # 创建白色背景图片
    white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))

    # 如果图片有透明通道，合成到白色背景上
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        # 合成图片
        composite = Image.alpha_composite(white_bg, img)
        # 转换为RGB模式（去掉透明通道）
        result = composite.convert("RGB")
    else:
        # 如果没有透明通道，直接转换
        result = img.convert("RGB")

    # 保存结果
    result.save(output_path, "PNG")  # 也可以保存为其他格式


def crop_to_ratio_pil(input_path, output_path, target_width=296, target_height=152):
    """
    将图片居中裁剪到目标比例，不进行缩放

    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        target_width: 目标宽度（用于计算比例）
        target_height: 目标高度（用于计算比例）
    """
    # 打开图片
    img = Image.open(input_path)

    original_w, original_h = img.size
    target_ratio = target_width / target_height
    original_ratio = original_w / original_h

    print(f"原始尺寸: {original_w}x{original_h}")
    print(f"原始比例: {original_ratio:.3f}")
    print(f"目标比例: {target_ratio:.3f}")

    if original_ratio > target_ratio:
        # 原图更宽：裁剪左右两侧
        new_width = int(original_h * target_ratio)
        new_height = original_h
        left = (original_w - new_width) // 2
        top = 0
        print(f"裁剪左右: 新尺寸 {new_width}x{new_height}")
    else:
        # 原图更高：裁剪上下两侧
        new_width = original_w
        new_height = int(original_w / target_ratio)
        left = 0
        top = (original_h - new_height) // 2
        print(f"裁剪上下: 新尺寸 {new_width}x{new_height}")

    # 裁剪图片
    img_cropped = img.crop((left, top, left + new_width, top + new_height))

    # 保存结果
    img_cropped.save(output_path, format="PNG")
    print(f"已保存到: {output_path}")
    print(f"最终尺寸: {new_width}x{new_height}")

    return img_cropped


def resize_image_fill_pil(input_path, output_path, target_size=(296, 152)):
    """
    将图片按填充方式缩放到目标尺寸（保持比例，裁剪多余部分）

    Args:
        input_path: 输入图片路径
        output_path: 输出图片路径
        target_size: 目标尺寸 (width, height)
    """
    # 打开图片
    img = Image.open(input_path)

    target_w, target_h = target_size
    original_w, original_h = img.size

    # 计算缩放比例，使图片完全覆盖目标区域
    scale = max(target_w / original_w, target_h / original_h)

    # 计算缩放后的尺寸
    new_w = int(original_w * scale)
    new_h = int(original_h * scale)

    # 先缩放到更大尺寸
    img_resized = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # 计算裁剪区域（居中裁剪）
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    right = left + target_w
    bottom = top + target_h

    # 裁剪到目标尺寸
    img_cropped = img_resized.crop((left, top, right, bottom))

    # 保存结果
    img_cropped.save(output_path, format="PNG")
    print(f"图片已保存到: {output_path}")
    print(f"原始尺寸: {original_w}x{original_h}")
    print(f"处理过程: 缩放至 {new_w}x{new_h}，然后裁剪至 {target_w}x{target_h}")
