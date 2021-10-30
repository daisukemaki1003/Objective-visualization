from datetime import datetime
import cv2
from jinja2 import Environment, FileSystemLoader
import json
import pdfkit
from pdf2image import convert_from_path
import os
import sys

wkhtmltopdf = '/usr/local/bin/wkhtmltopdf'  # wkhtmltopdf library path

# ファイルパス
# template_dir = '../templates'
# template_html = 'template.tpl'
# temp_file = '../templates/__tmp.html'
# output_path = '../output'
# output_pdf_file = '../output/output.pdf'
# css_file = '../templates/styles.css'
# img_path = '../image'
# output_img_file = 'output_pic'
# desktop_image = '../image/desktop_picture.jpg'


def error_print(error_text):
    with open('../error.log', 'a') as f:
        f.write(error_text)


def error_output(func):
    def _wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            date = str(datetime.now().strftime('%Y/%m/%d %H:%M'))
            error_print(date + '  ' + str(e) + '\n')
            sys.exit()
    return _wrapper
    

class SaveImage:
    def __init__(self):
        json_open_setting = open('../settings/setting.json', 'r')
        json_setting = json.load(json_open_setting)
        
        self.DESKTOP_IMG_PATH = json_setting['desktop_img_path']
        self.DESKTOP_BASE_IMG = json_setting['desktop_base_img']
        self.ACCUMULATED_FILE = json_setting['accumulated_file']
        self.TEMPLATE_DIR = json_setting['template_dir']
        self.TEMPLATE_HTML = json_setting['template']['html']
        self.TEMPLATE_CSS = json_setting['template']['css']
        self.OUTPUT_DIR = json_setting['output_dir']
        self.OUTPUT_PDF_PATH = os.path.join(self.OUTPUT_DIR, 'output.pdf')
        
        json_data_path = os.path.join(json_setting['data_dir'], json_setting['accumulated_file'] + '.json')
        json_open = open(json_data_path)
        self.json_data = json.load(json_open)
    
        # 改行コードを改行タグに変換
        contents_list = []
        for content in self.json_data['Contents']:
            c_item = dict()
            c_item['content_title'] = str(content['content_title']).replace('\n', '</p><p>')
            c_item['content_value'] = str(content['content_value']).replace('\n', '</p><p>')
            contents_list.append(c_item)
        self.json_data['Contents'] = contents_list
        
        self.conversion_html_to_pdf()
        self.conversion_pdf_to_jpg()
        self.concat_jpg()
        
    @error_output
    def conversion_html_to_pdf(self):
        env = Environment(loader=FileSystemLoader(self.TEMPLATE_DIR))
        template = env.get_template(self.TEMPLATE_HTML)
        temporary_save_html = os.path.join(self.OUTPUT_DIR, '__tmp.html')
        
        with open(temporary_save_html, 'wt', encoding='utf-8') as fp:
            fp.write(template.render(self.json_data))
        
        conf = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf)
        options = {'page-size': 'A4', 'encoding': "UTF-8"}
        pdfkit.from_file(temporary_save_html, self.OUTPUT_PDF_PATH, css=os.path.join(self.TEMPLATE_DIR, self.TEMPLATE_CSS), options=options, configuration=conf)
        print("ok")
    
    @error_output
    def conversion_pdf_to_jpg(self, fmt='jpeg'):
        back_img = cv2.imread(self.DESKTOP_BASE_IMG)
        convert_image = convert_from_path(self.OUTPUT_PDF_PATH, size=back_img.shape[0] - 200)
        convert_image[0].save(str(os.path.join(self.OUTPUT_DIR, self.ACCUMULATED_FILE + '.jpg')), fmt)
    
    @error_output
    def concat_jpg(self):
        fore_img = cv2.imread(str(os.path.join(self.OUTPUT_DIR, self.ACCUMULATED_FILE + '.jpg')))
        back_img = cv2.imread(self.DESKTOP_BASE_IMG)
    
        dx = 100  # 横方向の移動距離
        dy = 100  # 縦方向の移動距離
        h, w = fore_img.shape[:2]
    
        back_img[dy:dy + h, dx:dx + w] = fore_img
        cv2.imwrite(self.DESKTOP_IMG_PATH, back_img)






