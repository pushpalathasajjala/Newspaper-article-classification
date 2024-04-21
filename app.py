from flask import Flask
from flask import render_template,url_for,request,redirect
import numpy as np
import predictions as p
import mysql.connector


app = Flask(__name__)

database = mysql.connector.connect(
    host='localhost', user='root', password='', database='newspaper')
db = database.cursor()

home_page = 'index.html'
upload_page = 'upload.html'
view_data_page = 'view_data.html'
model_page = 'model.html'
predict_page = 'predict.html'
graph_page = 'graph.html'
about_page = 'home.html'
preprocess_page = 'preprocess.html'

@app.route('/')
def index():
    return render_template(home_page)

@app.route('/home')
def home():
    return render_template(about_page)


@app.route('/uploaddata')
def upload_data():
    return render_template(upload_page)


@app.route('/viewdata')
def view_data():
    p.show_data()
    return render_template(view_data_page)


@app.route("/preprocess")
def clean_data():
    p.preprocess()
    return render_template(preprocess_page)
    

@app.route('/trainmodel')
def model_data():
    p.split_data()
    return render_template(model_page)


@app.route('/predict')
def predict():
    return render_template(predict_page)


@app.route('/showgraph')
def show_graph():
    return render_template(graph_page)



@app.route('/getfile',methods=['POST','GET'])
def get_df_file():
    if request.method == 'POST':
        data_file = request.files.get('datafile')
        if data_file:
            p.read_data(data_file)
            if data_file is not None:
                return render_template(upload_page,msg='File uploaded successfully')
            else:
                return render_template(upload_page,msg='Please select a file')
    return render_template(upload_page,msg='Please select a file')
    


@app.route('/selectmodel',methods=['POST','GET'])
def return_score():
    if request.method == 'POST':
        form = request.form
        algo = form['algo']
        score = p.get_accuracy(algo)
        return render_template(model_page,score=f'Accuracy is : {round(score,2)}%')
    return render_template(model_page,score=f'Please try again')


@app.route('/getdata',methods=['POST','GET'])
def predict_binary():
    if request.method == 'POST':
        form = request.form
        oxygen = form['oxygen']
        temp = form['temp'] 
        humid = form['humid']

        oxygen = np.float64(oxygen) / 100
        temp = np.float64(temp) / 100
        humid = np.float64(humid) / 100
        msg = p.get_result(temp,humid,oxygen)
        return render_template(predict_page,msg=msg)
    

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        db.execute(
            f"select exists(select * from users where email='{email}' and password='{password}')")
        if db.fetchone()[0] > 0:
            return render_template(about_page)
        else:
            return render_template(home_page, msg='No user found please check credentials')
    


@app.route('/signup', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form.get('regname')
        email = request.form.get('regemail')
        password = request.form.get('regpassword')
        a = 'insert into users (name,email,password) values (%s,%s,%s)'
        b = (name, email, password)
        db.execute(a, b)
        database.commit()
    return render_template(home_page, msg='Registration Successful Please Login')



if __name__ == '__main__':
    app.run(debug=True)