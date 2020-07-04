import os


def extract_image(image_path, page):
    os.system(
        f"convert {image_path}[{page}] {image_path[:-4]}_page{page+1}.jpg")
    return(image_path[:-4] + f"_page{page+1}.jpg")


def resize_image(image_path):
    new_name = str(image_path)[:-4] + "_small.jpg"
    os.system(
        f"convert {image_path} -resize 1000x1000! -quality 100 {new_name}")
    return(image_path)


def convert(image_path):
    for target_list in range(3):
        os.system(f"rm {resize_image(extract_image(image_path, target_list))}")


def resumen_extracto(filename):
    a = (os.system((f"pdftotext {os.getcwd()}/static/assets/library/{filename} - |grep -A 1 'RESUMO' ")))
    if(a == 0):
        return os.popen((f"pdftotext {os.getcwd()}/static/assets/library/{filename} - |grep -A 1 'RESUMO' ")).read()
    else:
        return "RESUMO não estar disponivel para esse trabalho."


if __name__ == "__main__":
    resumen_extracto("amplificador_operacidonal.pdf")
