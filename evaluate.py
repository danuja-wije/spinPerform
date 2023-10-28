import dash
from dash import html
from dash import dcc
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app
import pandas as pd
import base64
import shutil
import os
import models.legel_ball as lb_model
import models.front_foot as ff_model
import models.danger_model as dm_model
import models.arm_ball as ab_model
import plotly.graph_objects as go
import pymongo
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import Paragraph
import shutil
from reportlab.lib.styles import getSampleStyleSheet

UPLOAD_DIRECTORY = "uploads"  # Directory to store uploaded images
styles = getSampleStyleSheet()
# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://common:admin@cluster0.epwxvmc.mongodb.net/")
db = client["user_database"]
users_collection = db["users"]
# user1 = user.User("","")
history_collection = db["history"]

OUTPUT_DICT = dict()
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

outer_box = html.Div([
        dbc.Modal([
        dbc.ModalHeader("Modal Title"),
        dbc.ModalBody("This is the content of the modal."),
        dbc.ModalFooter(dbc.Button("Close", id="close-modal-button", className="ml-auto")),
    ], id="modal"),
        html.H1(["Evaluate"],style={'textAlign':'center'}),
    html.Div([
        html.Div([
            html.H2("No Ball"),
    dcc.Upload(     
        id='upload-image',
        children=html.Div([
            'Drag and Drop or Select an Image',
        ]),
        style={
            'width': '93%',
            'height': '150px',
            'lineHeight': '150px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False  # Allow only one image to be uploaded
    ),
        # html.Div(id='output-image-upload')
        ], className="inner-box", id="inner-box1"),

        html.Div([
            html.H2("Leg Angle"),
    dcc.Upload(
        id='upload-image-2',
        children=html.Div([
            'Drag and Drop or Select an Image',
        ]),
        style={
            'width': '93%',
            'height': '150px',
            'lineHeight': '150px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False  # Allow only one image to be uploaded
    ),
        # html.Div(id='output-image-upload-2')
        ], className="inner-box", id="inner-box2"),
        html.Div([
            html.H2("Danger Area"),
    dcc.Upload(
        id='upload-image-3',
        children=html.Div([
            'Drag and Drop or Select an Image',
        ]),
        style={
            'width': '93%',
            'height': '150px',
            'lineHeight': '150px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False  # Allow only one image to be uploaded
    ),
        html.Div(id='output-image-upload-3')
        ], className="inner-box", id="inner-box3"),
        html.Div([
            html.H2("Arm Alngle"),
    dcc.Upload(
        id='upload-image-4',
        children=html.Div([
            'Drag and Drop or Select an Image',
        ]),
        style={
            'width': '93%',
            'height': '150px',
            'lineHeight': '150px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False  # Allow only one image to be uploaded
    ),
        html.Div(id='output-image-upload-4')
        ], className="inner-box", id="inner-box4"),
    ], className="inner-mid-box", id="inner-box"),
    html.Div([
        html.Div([
            html.H2("Overall Result"),
            html.P("Please upload all the images to get the result"),
            html.Div([
                html.Div([
                    dbc.Row([
                      dbc.Col(html.H3("No Ball")),  
                      dbc.Col(dcc.Loading(
                        id="loading-2",
                        children=[html.Div([html.Div(id="noball-status")])],
                        type="circle",
                        )),
                    ]),
                    dbc.Row([
                      dbc.Col(html.H3("Leg Angle")),  
                      dbc.Col(dcc.Loading(
                        id="loading-2",
                        children=[html.Div([html.Div(id="legangle-status")])],
                        type="circle",
                        )),
                    ]),
                    dbc.Row([
                      dbc.Col(html.H3("Danger Area")),  
                      dbc.Col(dcc.Loading(
                        id="loading-2",
                        children=[html.Div([html.Div(id="danger-status")])],
                        type="circle",
                        )),
                    ]),
                    dbc.Row([
                      dbc.Col(html.H3("Arm Angle")),  
                      dbc.Col(dcc.Loading(
                        id="loading-2",
                        children=[html.Div([html.Div(id="arm-status")])],
                        type="circle",
                        )),
                    ])
                
                
                ],className="result-noball",id="result-noball"),
            ]),
        dbc.Button("Calculate",className="btn", id="calculate-button"),
        ],className="result-inner-box-1",id="result-inner-box-1"),
        html.Div([
            html.Img(src=app.get_asset_url('analys.gif'))
        ],className="result-inner-box-2",id="result-inner-box-2"),
    ],className="result-outer-box",id="result-outer-box"),
    html.Div(id="output-overall-result")
])
def create_heading(text, style):
    return Paragraph(text, style["Heading1"])

def create_table(data):
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ]))
    return table

def create_paragraph(text, style):
    return Paragraph(text, style["Normal"])

def generate_report(df, arm_angle_exceeded, danger_area_detected, foot_angle_violated, no_ball_detected, styles):
    elements = []
    
    # Heading
    elements.append(create_heading('<para alignment="center">Cricket Bowling Analysis Report</para>', styles))
    
    # Table
    data = [['Report Content'], [df]]
    elements.append(create_table(data))
    elements.append(create_paragraph("<br />\n", styles))
    
    # Sections
    if arm_angle_exceeded:
        arm_angle_section = (
            "ARM ANGLE<br />\n"
            "Standardized elbow angle exceeded! You are exceeding the 15 degrees angle during the ball releasing."
            " To avoid:<br />\n"
            "• Focus on maintaining a relaxed wrist and grip on the ball throughout the delivery stride.<br />\n"
            "• Focus on strengthening your shoulder, core, and leg muscles to improve stability and control during the bowling action.<br />\n"
            "• Consciously focus on maintaining a straight and smooth arm throughout the delivery stride.<br />\n"
            "• Keep your hand as straight as possible while delivering the ball.<br />\n<br />\n"
        )
        elements.append(create_paragraph(arm_angle_section, styles))
        elements.append(create_paragraph("<br />\n", styles))

    if danger_area_detected:
        danger_area_section = (
            "DANER AREA<br />\n"
            "Danger area detected! You are stepping on the danger area during your follow through."
            " To avoid:<br />\n"
            "• Shorten your stride during delivery and follow through.<br />\n"
            "• Maintain a straight line with correct alignment.<br />\n"
            "• Control and balance to maintain stability.<br /><br />\n"
        )
        elements.append(create_paragraph(danger_area_section, styles))
        elements.append(create_paragraph("<br />\n", styles))

    if foot_angle_violated:
        foot_angle_section = (
            "FOOT ANGLE<br />\n"
            "Standardized front foot angle violated! You are keeping your front foot in a wrong angle."
            " To avoid:<br />\n"
            "• Have a clear idea about the size of the correct angle for the foot to be kept which is from 30 to 60 degrees.<br />\n"
            "• Be focused before taking your startup run to deliver the ball.<br />\n"
            "• Be relaxed and mindful at the moment you keep your foot.<br /><br />\n"
        )
        elements.append(create_paragraph(foot_angle_section, styles))
        elements.append(create_paragraph("<br />\n", styles))

    if no_ball_detected:
        no_ball_section = (
            "NO BALL<br />\n"
            "No ball detected! You are overstepping the crease."
            " To avoid:<br />\n"
            "• Maintain a proper run-up: Practice your run-up regularly and make sure it is consistent. This will help you maintain your balance and avoid overstepping the crease.<br />\n"
            "• Focus on the crease: Keep your eyes on the crease while running in to bowl. This will help you judge the distance accurately and prevent overstepping.<br />\n"
            "• Mark your run-up: If needed, mark your run-up with a small marker or cone. This can act as a visual cue and help you stay behind the crease.<br />\n"
            "• Practice rhythm and timing: Work on your timing during the run-up so that your front foot lands comfortably behind the popping crease. This will reduce the chances of overstepping.<br />\n"
            "• Develop body awareness: Pay attention to your body position and movements during the delivery stride. Practice maintaining control and balance throughout your action.<br /><br />\n"
        )
        elements.append(create_paragraph(no_ball_section, styles))
        elements.append(create_paragraph("<br />\n", styles))
    # Build the PDF document
    pdf_buffer = BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    doc.build(elements)
    pdf_buffer.seek(0)
    
    return pdf_buffer
@app.callback(Output('output-overall-result', 'children'),[Input("calculate-button", "n_clicks"),Input('intermediate-value', 'data')])
def calculate(n_clicks,curr_user):
    if n_clicks is None:
        raise PreventUpdate
    print("OUTPUT_DICT",OUTPUT_DICT)
    if len(OUTPUT_DICT) == 7:

        query = {"user": curr_user}
        count = history_collection.count_documents(query)
        print("count",count)
        if count < 5:
            arm_angle_exceeded = True
            danger_area_detected = True
            foot_angle_violated = True
            no_ball_detected = True
            print("OUTPUT_DICT",OUTPUT_DICT)
            df = pd.DataFrame(OUTPUT_DICT.items(),columns=['Name','Predicted Outputs'])
            print("df",df)
            fig1 = go.Figure(data=[go.Table(
                header=dict(values=list(df.columns),
                            fill_color='paleturquoise',
                            align='left'),
                cells=dict(values=[df.Name, df["Predicted Outputs"]],
                        fill_color='lavender',
                        align='left'))
            ])
            SCORE = 0
            if OUTPUT_DICT['no_ball'] == "Legal Ball":
                SCORE += 25
                no_ball_detected = False

            if OUTPUT_DICT['leg_ball'] == "Correct Position":
                SCORE += 25
                foot_angle_violated = False


            if OUTPUT_DICT['danger_ball'] == "non_danger_area":
                SCORE += 25
                danger_area_detected = False

            if OUTPUT_DICT['arm-_ball'] == "Correct Position": 
                SCORE += 25
                arm_angle_exceeded = False
        
            fig = go.Figure(go.Indicator(
            domain = {'x': [0, 1], 'y': [0, 1]},
            value = SCORE,
            mode = "gauge+number",
            title = {'text': "Score"},
            delta = {'reference': 60},
            gauge = {'axis': {'range': [None, 100]},
                    'steps' : [
                        {'range': [0, 60], 'color': "lightgray"},
                        {'range': [60, 100], 'color': "gray"}],
                    'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 40}}))
            hist = dict()
            hist=OUTPUT_DICT.copy()
            hist['score'] = SCORE
            hist['user'] = curr_user
            history_collection.insert_one(hist)
            df = df.reset_index(drop=True)
            # Generate the PDF report
            pdf_buffer = generate_report(df, arm_angle_exceeded, danger_area_detected, foot_angle_violated, no_ball_detected, styles)
            # Convert the PDF content to base64 for embedding in a link
            pdf_base64 = base64.b64encode(pdf_buffer.read()).decode('utf-8')
            
            # Display the download link
            download_link = html.Div([
                html.A(
                'Download PDF Report',
                href=f'data:application/pdf;base64,{pdf_base64}',
                download='report.pdf',
            )
            ],className="download-link")
            
            return html.Div([
                dcc.Graph(
                    id='example-graph',
                    figure=fig
                ),
                dcc.Graph(figure=fig1),
                download_link
            ],className="result-graph-box",id="result-graph-box")
        else:
            return html.Center(html.Div([
                html.P("Please make payments before continue"),
                dbc.Button("Make Payment",className="btn", id="open-modal-button",href="/payment")
            ],className="card payment-card",id="payment-card")) 
    else:
        return html.Div([
                html.P("Please upload all the images to get the result")
            ])

@app.callback(
    Output('noball-status', 'children'),
    Input('upload-image', 'contents'),
    State('upload-image', 'filename')
)
def upload_image(contents,filename):
    if contents is None:
        raise PreventUpdate

    # _, content_string = contents.split(',')
    # # print("content_string",_)
    # image_data = content_string.encode('utf-8')
    # decoded_image = base64.b64decode(contents.split(',')[1])

    # # Generate a unique filename for the uploaded image
    # image_filename = os.path.join(UPLOAD_DIRECTORY, filename)

    # with open(image_filename, 'wb') as f:
    #     f.write(base64.b64encode(decoded_image).decode())

    # # Make a copy of the uploaded image and rename it
    # print("file name is -------------------- ",filename)
    # # copied_filename = os.path.join(UPLOAD_DIRECTORY, 'copied_image.jpg')
    # # shutil.copy(image_filename, copied_filename)

    decoded = base64.b64decode(contents.split(',')[1])
    filepath = os.path.join(UPLOAD_DIRECTORY, filename)
    with open(filepath, 'wb') as f:
        f.write(decoded)

    try:
        OUTPUT_DICT['no_ball'] = lb_model.model(filepath)
        return [html.Img(src=app.get_asset_url('done.gif'),style={'width':'50px','height':'50px'})]
    except:
        return [html.Img(src=app.get_asset_url('not_done.gif'))]


@app.callback(
    Output('legangle-status', 'children'),
    Input('upload-image-2', 'contents'),
    State('upload-image-2', 'filename')
)
def upload_image(contents,filename):
    if contents is None:
        raise PreventUpdate

    # _, content_string = contents.split(',')
    # image_data = content_string.encode('utf-8')

    # # Generate a unique filename for the uploaded image
    # image_filename = os.path.join(UPLOAD_DIRECTORY, 'uploaded_image.jpg')

    # with open(image_filename, 'wb') as f:
    #     f.write(image_data)

    # # Make a copy of the uploaded image and rename it
    # print("file name is -------------------- ",image_filename)
    # copied_filename = os.path.join(UPLOAD_DIRECTORY, 'copied_image.jpg')
    # shutil.copy(image_filename, copied_filename)
    decoded = base64.b64decode(contents.split(',')[1])
    filepath = os.path.join(UPLOAD_DIRECTORY, filename)
    with open(filepath, 'wb') as f:
        f.write(decoded)
    try:
        OUTPUT_DICT['leg_ball'] = ff_model.model(filepath)
        return [html.Img(src=app.get_asset_url('done.gif'),style={'width':'50px','height':'50px'})]

    except:
        return [html.Img(src=app.get_asset_url('not_done.gif'))]


@app.callback(
    Output('danger-status', 'children'),
    Input('upload-image-3', 'contents'),
    State('upload-image-3', 'filename')
)
def upload_image(contents,filename):
    if contents is None:
        raise PreventUpdate

    # _, content_string = contents.split(',')
    # image_data = content_string.encode('utf-8')

    # # Generate a unique filename for the uploaded image
    # image_filename = os.path.join(UPLOAD_DIRECTORY, 'uploaded_image.jpg')

    # with open(image_filename, 'wb') as f:
    #     f.write(image_data)

    # # Make a copy of the uploaded image and rename it
    # print("file name is -------------------- ",image_filename)
    # copied_filename = os.path.join(UPLOAD_DIRECTORY, 'copied_image.jpg')
    # shutil.copy(image_filename, copied_filename)
    decoded = base64.b64decode(contents.split(',')[1])
    filepath = os.path.join(UPLOAD_DIRECTORY, filename)
    with open(filepath, 'wb') as f:
        f.write(decoded)
    try:
        OUTPUT_DICT['danger_ball'] = dm_model.model(filepath)
        return [html.Img(src=app.get_asset_url('done.gif'),style={'width':'50px','height':'50px'})]
    except:
        return [html.Img(src=app.get_asset_url('not_done.gif'))]


@app.callback(
Output('arm-status', 'children'),
Input('upload-image-4', 'contents'),
State('upload-image-4', 'filename')
)
def upload_image(contents,filename):
    if contents is None:
        raise PreventUpdate

    # _, content_string = contents.split(',')
    # image_data = content_string.encode('utf-8')

    # # Generate a unique filename for the uploaded image
    # image_filename = os.path.join(UPLOAD_DIRECTORY, 'uploaded_image.jpg')

    # with open(image_filename, 'wb') as f:
    #     f.write(image_data)

    # # Make a copy of the uploaded image and rename it
    # # print("file name is -------------------- ",image_filename)
    # copied_filename = os.path.join(UPLOAD_DIRECTORY, 'copied_image.jpg')
    # shutil.copy(image_filename, copied_filename)

    decoded = base64.b64decode(contents.split(',')[1])
    filepath = os.path.join(UPLOAD_DIRECTORY, filename)
    with open(filepath, 'wb') as f:
        f.write(decoded)
    try:
        OUTPUT_DICT['arm-_ball'] = ab_model.model(filepath)
        return [html.Img(src=app.get_asset_url('done.gif'),style={'width':'50px','height':'50px'})]
    except:
        return [html.Img(src=app.get_asset_url('not_done.gif'))]