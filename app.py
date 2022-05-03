from re import T
from flask import Flask, request, render_template, send_file, redirect
import logging, sys
import instagram
import youtube_dl
import webbrowser
import os

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
app = Flask(__name__)

resolutions = ['Auto', '144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2040p']


@app.route("/")
def home():
    return render_template('Home.html')


# YouTube

@app.route("/Download_MP4")
def Download_MP4():
    global resolutions
    return render_template('MP4.html', resolutions=resolutions)


@app.route("/Download_MP3")
def Download_MP3():
    return render_template('MP3.html')


@app.route('/download', methods=["POST", "GET"])
def download():
	url = request.form["url"]
	print("Someone just tried to download", url)
	with youtube_dl.YoutubeDL() as ydl:
		url = ydl.extract_info(url, download=False)
		print(url)
		try:
			download_link = url["entries"][-1]["formats"][-1]["url"]
		except:
			download_link = url["formats"][-1]["url"]
		return redirect(download_link+"&dl=1")

# Instagram
res=[]

@app.route("/Download_reel")
def Download_reel():
    global res
    try:
        if res[1].get("authenticated"):
            return render_template("Instagram_reel.html")
        else:
            return render_template('Instagram_login.html', login_info="Login Failed!!")
    except:
        return render_template('Instagram_login.html',login_info="Login Failed!!")

@app.route("/Instagram_Download",methods=['GET', 'POST'])
def Instagram_Download():
    global res
    try:
        username = request.form['username']
        password = request.form['password']
        res=instagram.authontication(username,password)
        if res[1].get("authenticated"):
            return render_template("Instagram_reel.html")
        else:
            return render_template('Instagram_login.html', login_info="Login Failed!!")
    except:
        return render_template('Instagram_login.html',login_info="Login Failed!!")

@app.route("/authorization")
def authorization():
    global res
    try:
        if res[1].get("authenticated"):
            return render_template("Instagram_reel.html")
        else:
            return render_template('Instagram_login.html')
    except:
        return render_template('Instagram_login.html')


@app.route("/Download_post")
def Download_post():
    global res
    try:
        if res[1].get("authenticated"):
            return render_template("Instagram_post.html")
        else:
            return render_template('Instagram_login.html',login_info="Login Failed!!")
    except:
        return render_template('Instagram_login.html',login_info="Login Failed!!")


@app.route("/download_insta_reel", methods=['GET', 'POST'])
def download_insta_reel():
    try:
        global res
        input_url = request.form['URL']

        filename = instagram.Download_reel(input_url,res[0],res[1])

        if filename == "None":
            logging.exception('Failed download')
            return "Instagram Reel download failed!"

        return send_file(f"{filename}.mp4", as_attachment=True)
    except:
        logging.exception('Failed download')
        return "Instagram Reel download failed!"


@app.route("/download_insta_post", methods=['GET', 'POST'])
def download_insta_post():

    try:
        global res
        input_url = request.form['URL']

        filename = instagram.Download_Post(input_url,res[0],res[1])

        if filename == "None":
            logging.exception('Failed download')
            return "Instagram Post download failed!"

        return send_file(f"{filename}.jpg", as_attachment=True)
    except:
        logging.exception('Failed download')
        return "Instagram Reel download failed!"


if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:5000/")
    app.run()
    try:
        os.remove("rishabh"+"_video"+".mp4")
    except:
        try:
            os.remove("rishabh"+"_post"+".jpg")
        except:
            print("not file found")        
    