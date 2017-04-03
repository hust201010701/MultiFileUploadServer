from flask import Flask,request,send_from_directory,jsonify
import os
from werkzeug import secure_filename

app = Flask(__name__)
app.config['IMAGE_FOLDER'] = os.path.abspath('.')+'\\images\\'
ALLOWED_EXTENSIONS=set(['png','jpg','jpeg','gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload',methods=['POST'])
def upload_file():
    if request.method=='POST':
        for k in request.files:
            file = request.files[k]
            print(file)
            image_urls = []
            if file and allowed_file(file.filename):
                filename=secure_filename(file.filename)
                file.save(os.path.join(app.config['IMAGE_FOLDER'],filename))
                image_urls.append("images/%s"%filename)
        return jsonify({"code":1,"image_urls":image_urls})

#让文件映射访问，否则默认只能访问static文件夹中的文件
@app.route("/images/<imgname>",methods=['GET'])
def images(imgname):
    return send_from_directory(app.config['IMAGE_FOLDER'],imgname)

if __name__ == "__main__":
    # 检测 IMAGE_FOLDER 是否存在
    if not os.path.exists(app.config['IMAGE_FOLDER']):
        os.mkdir(app.config['IMAGE_FOLDER'])
    app.run("192.168.1.102",debug=True)