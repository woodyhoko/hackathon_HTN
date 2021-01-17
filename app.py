############################################################################################
########################################## IMPORTS #########################################
############################################################################################

# Classic libraries
import os
import numpy as np
from numpy.linalg import norm
import pandas as pd

# Dash imports
import dash
import dash_core_components as dcc
import dash_html_components as html
from flask import render_template, request, redirect
import imageio
import image_demp
import cv2

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


# Custom function
import pickle
def load_pickle(file_name):
    file_path = file_name
    with open(file_path, 'rb') as pfile:
        my_pickle = pickle.load(pfile)
    return my_pickle

############################################################################################
############################## PARAMETERS and PRE-COMPUTATION ##############################
############################################################################################

statte = [""]

# Load pre computed data
world = load_pickle('world_info.p')

# Deployment inforamtion
PORT = 8050

############################################################################################
########################################## APP #############################################
############################################################################################

# Creating app
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)


# Associating server
server = app.server
server.config["TEMPLATES_AUTO_RELOAD"] = True
app.title = 'COVID 19 - World cases'
app.config.suppress_callback_exceptions = True

score = []

@server.route('/view-video', methods = ["GET"])
def view_video():
    return render_template("public/view_video.html", values=score)

@server.route('/upload-video', methods = ["GET", "POST"])
def upload_video():

    if request.method == "POST":
        if request.files:

            video = request.files["video"].read()
            video2 = request.files["video2"].read()
            print(len(video))
            video_r = imageio.get_reader(video,  'ffmpeg')
            video_rm = video_r.get_meta_data()
            video_r2 = imageio.get_reader(video2,  'ffmpeg')
            video_rm2 = video_r2.get_meta_data()
            # print(video_r.get_data(10))
            print(video_rm)
            temp = video_r
            if video_rm["duration"] > video_rm2["duration"]:
                temp = video_r2
            data1 = []
            data2 = []
            print("reading... ")
            statte[0] = "reading video ... "
            for i, ii in enumerate(temp):
                data1 += [ii]
                data2 += [video_r2.get_data(i)]
            print("analysing... ")
            statte[0] = "analysing video 1 ... "
            data_p1, data_ps1 = image_demp.main(data1, statte)
            statte[0] = "analysing video 2 ... "
            data_p2, data_ps2 = image_demp.main(data2, statte)
            data_score = []
            print("calculating dance score ... ")
            statte[0] = "calculating dance score ... "
            for i, ii in enumerate(temp):
                if len(data_ps1[i])!=0 and len(data_ps2[i])!=0:
                    da = data_ps1[i][:34]
                    db = data_ps2[i][:34]
                    data_score += [np.inner(da, db/(norm(da)*norm(db)))]
            print("done!")
            statte[0] = "done!"
            print(np.array(data_ps2).shape)
            print(np.array(data_score).shape)
            
            # video_out = cv2.VideoWriter("static/out1.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 24, (video_rm["source_size"][0],video_rm["source_size"][1]))
            # for image in data_p1:
            #     video_out.write(image)

            # video_out2 = cv2.VideoWriter("static/out2.mp4", cv2.VideoWriter_fourcc(*"mp4v"), 24, (video_rm2["source_size"][0],video_rm2["source_size"][1]))
            # for image in data_p2:
            #     video_out2.write(image)

            video_out = cv2.VideoWriter("static/out1.avi", cv2.VideoWriter_fourcc(*"XVID"), 24, (video_rm["source_size"][0],video_rm["source_size"][1]))
            for image in data_p1:
                video_out.write(image)
            video_out.release()
            video_out2 = cv2.VideoWriter("static/out2.avi", cv2.VideoWriter_fourcc(*"XVID"), 24, (video_rm2["source_size"][0],video_rm2["source_size"][1]))
            for image in data_p2:
                video_out2.write(image)
            video_out2.release()
            
            os.system("ffmpeg -y -i static/out1.avi static/out1.mp4")
            os.system("ffmpeg -y -i static/out2.avi static/out2.mp4")
            
            score = data_score
            
            a = list(range(len(data_score)))

            plt.plot(a[:-1],data_score[:-1],a[1:],data_score[1:],linewidth=0.2)
            plt.ylim((0,1.1))
            plt.savefig('static/score.png')
            plt.close()
            
            # return redirect(request.url)
            
            return redirect("/view-video")

    return render_template("public/upload_video.html", statte = statte)

# def 

@server.route('/HTN1')
def hello():
    import HTN1.app as app1
    app1()

############################################################################################
######################################### LAYOUT ###########################################
############################################################################################

links = html.Div(
    id='platforms_links',
    children=[                   
        html.A(
            href='https://towardsdatascience.com/how-to-create-animated-scatter-maps-with-plotly-and-dash-f10bb82d357a',
            children=[
                html.Img(src=app.get_asset_url('medium.png'), width=20, height=20),
                html.Span("Map")
            ]
        ),
        html.A(
            href='https://medium.com/@thibaud.lamothe2/deploying-dash-or-flask-web-application-on-heroku-easy-ci-cd-4111da3170b8',
            children=[
                html.Img(src=app.get_asset_url('medium.png'), width=20, height=20),
                html.Span("Deploy")
            ]
        ),
        html.A(
            href='https://github.com/ThibaudLamothe/dash-mapbox',
            children=[
                html.Img(src=app.get_asset_url('github.png'), width=20, height=20),
                # "Application code"
                html.Span("Code")
            ]
        ),
        html.A(
            href='https://public.opendatasoft.com/explore/dataset/covid-19-pandemic-worldwide-data/information/?disjunctive.zone&disjunctive.category&sort=date',
            children=[
                html.Img(src=app.get_asset_url('database.png'), width=20, height=20),
                # "Original COVID dataset"
                html.Span("Data")
            ],
        ),
    ],
)


app.layout = html.Div(
    children=[

        # HEADER
        html.Div(
            className="header",
            children=[
                html.H1("COVID 19 🦠 - Day to day evolution all over the world", className="header__text"),
                html.Span('(Last update: {})'.format(world['last_date'])),
                # html.Hr(),
            ],
        ),

        # CONTENT
        html.Section([
            
            # Line 1 : KPIS - World
            html.Div(
                id='world_line_1',
                children = [ 
                    html.Div(children = ['🚨 Confirmed', html.Br(), world['total_confirmed']], id='confirmed_world_total', className='mini_container'),
                    html.Div(children = ['🏡 Recovered', html.Br(), world['total_recovered']], id='recovered_world_total', className='mini_container'),
                    html.Div(children = [' ⚰️ Victims',   html.Br(), world['total_deaths']],    id='deaths_world_total',    className='mini_container'),            
                ],
            ),
            # html.Br(),

            # links,

            # Line 2 : MAP - WORLD
            html.Div(
                id='world_line_2',
                children = [
                    dcc.Graph(id='world_map', figure=world['figure'], config={'scrollZoom': False}),         
                ],
            ),
            # html.Br(),
        ]),
    ],
)

############################################################################################
######################################### RUNNING ##########################################
############################################################################################

if __name__ == "__main__":
    
    # Display app start
    print('*' * 80)
    print('App initialisation')
    print('*' * 80)

    # Starting flask server
    app.run_server(debug=True, port=PORT)