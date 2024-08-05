import os
from pdf2image import convert_from_path
from PIL import Image
import argparse

def convert_pdf_to_png(input_dir, output_dir, square_size=None):
    # 創建輸出資料夾如果它不存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 列出所有PDF檔案
    pdf_files = [f for f in os.listdir(input_dir) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file)
        images = convert_from_path(pdf_path)

        # 為每個PDF檔案創建一個資料夾
        pdf_output_dir = os.path.join(output_dir, os.path.splitext(pdf_file)[0])
        if not os.path.exists(pdf_output_dir):
            os.makedirs(pdf_output_dir)

        for i, image in enumerate(images):
            if square_size:
                # 擴展為正方形尺寸
                max_dimension = max(image.size)
                new_image = Image.new('RGB', (max_dimension, max_dimension), (255, 255, 255))
                new_image.paste(image, ((max_dimension - image.width) // 2, (max_dimension - image.height) // 2))
                image = new_image

                # 調整尺寸為square_size
                image = image.resize((square_size, square_size), Image.Resampling.LANCZOS)

            # 保存圖片
            image_path = os.path.join(pdf_output_dir, f'page_{i + 1}.png')
            image.save(image_path, 'PNG')

        print(f'Converted {pdf_file} to PNGs and saved in {pdf_output_dir}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert PDF to PNG')
    parser.add_argument('--square_size', type=int, help='Size to resize PNG images to (square)', default=None)

    args = parser.parse_args()

    input_dir = os.getcwd()  # 使用當前工作目錄
    output_dir = os.getcwd()  # 將輸出目錄設為當前工作目錄

    # 確認步驟
    confirm = input(f"請確認是否將目前所在目錄（{input_dir}）中所有PDF檔案轉為PNG？([yes]/no): ") # 如果不輸入 confirm 就是 yes
    confirm = confirm if confirm else 'yes'
    
    if confirm.lower() == 'yes':
        size_option = input("是否將圖片尺寸轉換為正方形尺寸？(yes/[no]): ") # 如果不輸入 size_option 就是 no
        size_option = size_option if size_option else 'no'
        if size_option.lower() == 'yes':
            if args.square_size is None:
                square_size = int(input("請輸入尺寸大小(e.g., 1080)([1080]): ")) # 如果不輸入 square_size 就是輸入 1080
                square_size = square_size if square_size else 1080
                convert_pdf_to_png(input_dir, output_dir, square_size)
            else:
                convert_pdf_to_png(input_dir, output_dir, args.square_size)
        else:
            convert_pdf_to_png(input_dir, output_dir)
    else:
        print("Operation cancelled.")
