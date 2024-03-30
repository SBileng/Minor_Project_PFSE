import streamlit as st
import calc_module as cm
import matplotlib as mp
from matplotlib import pyplot as plt

st.header("Section Designer")

materials = ["S235","S355","S460"]
sections = ["I","U","T","O"]
run = False
col1, col2 = st.columns(2)

with col1:
    material = st.selectbox("Material",materials)
    selection = st.selectbox("Section",sections)

    if material == "S235":
        i = 235
    elif material == "S355":
        i = 355
    elif material == "S460":
        i = 460   
    else:
        i = 235

    steel = cm.steel(i).mat

    section = cm.section

    if selection == "I":
        height = st.number_input("height",10,1000,200)
        width = st.number_input("width",10,1000,200)
        fl_thick = st.number_input("flange thickness",1,40,10)
        web_thick = st.number_input("web thickness",1,40,10)
        section = cm.I_section(steel,height,width,fl_thick,web_thick)
    elif selection == "U":
        height = st.number_input("height",10,1000,200)
        width = st.number_input("width",10,1000,200)
        fl_thick = st.number_input("flange thickness",1,40,10)
        web_thick = st.number_input("web thickness",1,40,10)
        section = cm.U_section(steel,height,width,fl_thick,web_thick)
    elif selection == "T":
        height = st.number_input("height",10,1000,200)
        width = st.number_input("width",10,1000,200)
        fl_thick = st.number_input("flange thickness",10,40,10)
        web_thick = st.number_input("web thickness",10,40,10)
        section = cm.T_section(steel,height,width,fl_thick,web_thick)
    elif selection == "O":
        diameter = st.number_input("diameter",10,1000,200)
        thickness = st.number_input("thickness",1,40,10)
        section = cm.O_section(steel,diameter,thickness)
    #cm.image_geo(section)
    #st.image("section.png")

with col2:
    N = st.number_input("Axial load",0)
    Vy = st.number_input("Shear Major",0)
    Vx = st.number_input("Shear Minor",0)
    Mzz = st.number_input("Torsional Moment",0)
    Mxx = st.number_input("Moment Major",0)
    Myy = st.number_input("Moment Minor",0)

results = cm.analyze(section,N,Vx,Vy,Mxx,Myy,Mzz)
st.set_option('deprecation.showPyplotGlobalUse', False)
fig = plt.plot(data = results.plot_stress("vm"))
st.pyplot(fig)