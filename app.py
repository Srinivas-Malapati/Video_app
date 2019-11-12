from flask import Flask, request, jsonify, render_template, url_for, redirect
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy



file_name = 'VideoList.db'

app1 = Flask(__name__)
app1.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{file_name}"
db = SQLAlchemy(app1)


class VideoList(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    thumn_nail = db.Column(db.String)
    title = db.Column(db.String) 
    created_on = db.Column(db.Integer)
    duration = db.Column(db.Integer)



@app1.route('/loginpage',methods = ['GET','POST'])
def loginpage():
	return render_template('login.html')

@app1.route('/homepage',methods = ['GET','POST'])
def homepage():
	return render_template('home.html')

@app1.route('/resultpage',methods = ['GET','POST'])
def resultpage():
        return render_template('result.html')
	


@app1.route('/upload_new_video', methods=['GET','POST'])
def upload_new_video():
    if request.method == 'GET':
        return render_template('video_list.html')
    else:
        data_fields = ["thumn_nail",
                       "title",
                       "created_on",
                       "duration"]

        data_dict = {}

        for field in data_fields:
            data_dict[field] = request.form.get(field)

        video_list = VideoList(**data_dict)
        db.session.add(video_list)
        db.session.commit()

        return redirect(url_for('homepage'))


@app1.route('/list_of_videos', methods=['GET','POST'])
def list_of_videos():
    if request.method == "GET":
        return render_template('find_video.html')
    else:
        
        title = request.form.get('title')
        created_on = request.form.get('created_on')
        duration = request.form.get('duration')
        result = VideoList.query.\
                                filter_by(title=title).\
                                filter_by(created_on=created_on).\
                                filter_by(duration=duration).\
                                all()

        print(result)

        return render_template('result.html',video_lists=result)
    
		  

if __name__ == "__main__":
    app1.run(debug=True,port=8000)
