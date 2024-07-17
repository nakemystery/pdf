import os
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def images_to_pdf(input_folder, output_pdf):
    # 获取文件夹中的所有文件夹
    subfolders = [f.path for f in os.scandir(input_folder) if f.is_dir()]

    for folder in subfolders:
        pdf_filename = os.path.join(output_pdf, os.path.basename(folder) + '.pdf')
        # 获取文件夹内的所有图片文件
        image_files = [f.path for f in os.scandir(folder) if f.is_file() and f.name.endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        # 判断当前子文件夹是否有子文件夹
        su_subfolders = [f.path for f in os.scandir(folder) if f.is_dir()]
        # 有则递归调用函数
        if su_subfolders:
            images_to_pdf(folder, output_pdf)
            continue

        if not image_files:
            continue

        # 创建PDF并将图片添加到PDF中
        c = canvas.Canvas(pdf_filename, pagesize=letter)
        for image_file in image_files:
            img = Image.open(image_file)
            img_width, img_height = img.size
            aspect_ratio = img_width / img_height
            c.setPageSize((letter[0], letter[1]))
            c.drawImage(image_file, 0, 0, width=letter[0], height=letter[0] / aspect_ratio)
            c.showPage()
            img.close()
        c.save()

if __name__ == "__main__":
    input_folder = "dataset"  # 输入文件夹路径
    output_pdf = "pdf"  # 输出PDF文件夹路径
    images_to_pdf(input_folder, output_pdf)
