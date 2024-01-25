import threading

import rosparam
import rospy
from flask import Flask, flash, redirect, render_template, request

root_path = rosparam.get_param("/flask_server/flask_root_path") # ここでパスを指定する
if root_path != "":
    app = Flask(__name__, root_path=root_path)
else:
    app = Flask(__name__)    
    
threading.Thread(target=lambda: rospy.init_node('ros_flask_test', disable_signals=True)).start()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return redirect('/some_page')

@app.route('/some_page')
def some_page():
    location = 'bed'
    # id=bed のボタンが押されたとき
    if request.method == 'POST' and request.form['id'] == 'bed':
        # ここで ROS の処理を行う
        location = 'bed'

        print("bed")
    # id=sofa のボタンが押されたとき
    elif request.method == 'POST' and request.form['id'] == 'sofa':
        # ここで ROS の処理を行う
        location = 'sofa'
        print("sofa")
    # それ以外のとき
    else:
        # 何もしない
        location = ''
        pass
    # sm_main.py に location を渡す
    # ここの処理を考えてください
    rospy.set_param('/flask_server/location', location) # ここでパラメータを設定する


    return render_template('some_page.html')    

if __name__ == '__main__':    
  app.run(debug=True, port=11000)
