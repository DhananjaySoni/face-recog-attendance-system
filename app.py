import os
from sqlalchemy.orm.session import Session
import streamlit as st
from PIL import Image
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import *
import db
import attendance as ap
import pandas as pd


def open_db():
    engine = create_engine("sqlite:///db.sqlite3")
    Session = sessionmaker(bind=engine)
    return Session()

if not os.path.exists(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)

st.set_page_config(
   page_title="Attendance System",
   page_icon="🧊",
   layout="wide",
   initial_sidebar_state="expanded",
)
st.title(TITLE)
choice = st.sidebar.selectbox("Select an option",MENU)


if choice =='Add data':
    imgdata = st.file_uploader("select an image",type=['jpg','png', 'jpeg'])
    name =st.text_input("enter name of student")
    roll_no=st.text_input("enter roll number")
    section=st.text_input("enter section")
    button=st.button('save')

    if imgdata and name and roll_no and section and button:
        
        im = Image.open(imgdata)
        path = os.path.join(UPLOAD_FOLDER,f"{name}_{roll_no}.{imgdata.name.split('.')[1]}")
        im.save(path,format=imgdata.type.split('/')[1])
        sess = open_db()
        student = db.Student(path=path,name=name,roll_no=roll_no,section=section)
        sess.add(student)
        sess.commit()
        sess.close()
        st.success('student details uploaded successfully')

if choice == 'Remove data':
    sess = open_db()
    students = sess.query(db.Student).all()
    print(students)
    sess.close()
    student=st.selectbox('Select a student to remove',students)
    if os.path.exists(student.path):
        image = st.image(student.path, width=100)
        print(image)

    if st.button("delete"): 
        try:
            print('try')
            sess = open_db()
            sess.query(db.Student).filter(db.Student.id == student.id).delete()
            if os.path.exists(student.path):
                os.unlink(student.path)
                image.empty()
            sess.commit()
            sess.close()
            st.info("student data deleted")
        except Exception as e:
            print("error",e)
            st.error("student data  not deleted")
            st.error(e)

      
    


if choice == 'Take attendance':
    btn=st.button('launch webcam')
    
    if btn:
        sess=open_db()
        ap.webcam(sess)
        sess.close()





if choice =='View attendance':
    engine = create_engine("sqlite:///db.sqlite3")  # Creating the engine
    query = "SELECT id,student,taken_on FROM Attendance "   # String containing the SQL query
    query2 = "SELECT id,name,roll_no,section FROM STUDENTS"
    df = pd.read_sql_query(query, engine, index_col="id")
    sdf= pd.read_sql_query(query2, engine, index_col="id")
    st.write(df)
    st.write(sdf)
        