from tkinter import E
from flask import *
from numpy import identity, prod, product
from pandas import value_counts
from database import *
from selenium_data import driverFunc
from flask_jwt_extended import *
from datetime import timedelta
import pandas as pd


app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = 'salman'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)


@app.route('/filteringTheData', methods = ["POST","GET"])
@jwt_required()
def filteringTheData():
    current_user_id = get_jwt_identity()
    user = session.query(UserDataInfo).get(current_user_id)
    if request.method == "GET":
        try:
            workbook = pd.read_csv("Products.csv")
            li = []
            for index,row in workbook.iterrows():
                Data = {
                    "Data" : row
                }
                datafunc = driverFunc(row)
                li.append(datafunc)
            # datafunc = driverFunc(li)
            return jsonify(
                data = user.first_name,
                message = "successfully searched the data",
                status = 200
            )
        except Exception as e:
            return jsonify(
                message = e,
                status = 500
            )

#reading the csv data and returning in jsonify
@app.route('/readingExcelData', methods = ["POS","GET"])
def readingExcelData():
    workbook = pd.read_csv("Products.csv")
    li = []
    for index,row in workbook.iterrows():
        Data = {
            f"ProductsData {index}" : row.to_dict()
        }
        li.append(Data)
    print(li)
    return jsonify(
        data = li
    )

#register form
@app.route('/register',methods = ["POST","GET"])
def register():
    if request.method == "POST":
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        email = request.form['email']
        password = request.form['password']
        register = UserDataInfo(first_name = f_name,
                                last_name = l_name,
                                user_email = email,
                                user_password = password)
        session.add(register)
        session.commit()
        return jsonify(
            message = "Successfully Register",
            status = 200
        )
    else:
        return jsonify(
            message = "The user not register",
            status = 500
        )
        

#login form
@app.route('/login',methods = ["POST","GET"])
def login():
    if request.method == "POST":
        try:
            username = request.form['first_name']
            password = request.form['user_password']
            result = session.query(UserDataInfo).filter_by(first_name=username,user_password=password).first()
            if result is None:
                return jsonify(
                message = "invalid paraeters",
                status = 200
            )
            else:
                access_token = create_access_token(identity = result.id)
                return jsonify({
                    "token" : access_token
                })
        except Exception as e:
            return jsonify(
                message = e,
                status = 500
            )
#adding the product data into the database
@app.route('/GetWeboc',methods = ["POST","GET"])
@jwt_required()   
def GetWeboc():
    url = request.form['product']
    current_user_id = get_jwt_identity()
    user = session.query(UserDataInfo).get(current_user_id)
    try:
        data = driverFunc(url)
        for entry in data:
            new_product = ProductData(product_description = entry['Product Description'],
                                  product_hs_code = entry['Product HS Code'],
                                  product_value_unit = entry['Product Value'])
            session.add(new_product)
            session.commit()
        return jsonify(
            data = user.first_name,
            message = "Succesfully scrape and added into the database",
            status = 200
        )
    except Exception as e:
        return jsonify(
            message = e,
            status = 500
        )
  
#showing all the data from the database  
  
@app.route('/getting_data',methods = ["POST","GET"])
@jwt_required()   
def getting_data():
    if request.method == "GET":
        current_user_id = get_jwt_identity()
        user = session.query(UserDataInfo).get(current_user_id)
        
        print(user.first_name)
        try:
            ProductDataList = []
            product_result = session.query(ProductData).all()
            for i in product_result:
                data = {
                    "Data" : i.to_dict()
                }
                ProductDataList.append(data)
            return jsonify(
                productinfo = ProductDataList,
                message = "Successfully show the data",
                status = 200
            )
        except Exception as e:
            return jsonify(
                message = e,
                status = 500
            )
@app.route('/SearchWeboc', methods = ["POST","GET"])
def SearchWeboc():
    if request.method == "GET":
        try:
            product = request.form['product']
            product_result = session.query(ProductData).filter(ProductData.product_description.contains(product)).all()
            product_data_list_by_searching = []
            for i in product_result:
                data = {
                    "Data" : i.to_dict()
                }
                product_data_list_by_searching.append(data)
            return jsonify(
                Product = product_data_list_by_searching,
                message = "Succesfully filter the data",
                status = 200
            )
        except Exception as e:
            return jsonify(
                message = "Unscuccesful",
                status = 500
            )
    

if(__name__ == '__main__'):
    app.run(debug = True)