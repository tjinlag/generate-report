from flask import Flask, send_from_directory
from flask_restful import Resource, Api
from flask_cors import cross_origin
from Data_Transformation import transform_data
from Data_Analysis import analyze_data
from PIL import Image
import os

app = Flask(__name__)
api = Api(app)

def run_python_script():
  transform_data()
  analyze_data()

def create_pdf_report():
  file_name = 'report.pdf'
  if os.path.exists(file_name):
    return file_name

  size = 1000, 600

  image1 = Image.open('./CC.png')
  image1.thumbnail(size)
  im1 = image1.convert('RGB')

  img_file_name_list = ['CC.png',
    'NC.png',
    'scatterplot1.png',
    'boxplot.png',
    'boxplotLogged.png',
    'Zone density from 8am to 11pm on 20 May stacked bars.png',
    'Frequency of Unauthorized Contact.png',
    'Frequency of High Risk Contact(above 30 mins).png',
    'Contacts in different zones.png',
  ]

  image_list = []
  for file_name in img_file_name_list:
    img = Image.open(file_name)
    img.thumbnail(size)
    img = img.convert('RGB')
    image_list.append(img)

  im1.save(file_name,save_all=True, append_images=image_list)
  return file_name

@app.route('/report')
@cross_origin()
def generate_report_api():
  file_name = create_pdf_report()

  return {
    'report': 'http://127.0.0.1:5000/assets/' + file_name,
  }

@app.route('/assets/<path:path>')
@cross_origin()
def send_asset(path):
  return send_from_directory('', path)

if __name__ == '__main__':
  run_python_script()
  app.run()
