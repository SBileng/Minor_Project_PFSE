import streamlit as st
import calc_module as cm
from matplotlib import pyplot as plt

st.header("Section Designer")

materials = ["S235","S355","S460"]
sections = ["I","U","T"]
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

    height = st.number_input("height [mm]",10,1000,200)
    width = st.number_input("width [mm]",10,1000,200)
    fl_thick = st.number_input("flange thickness [mm]",10,40,10)
    web_thick = st.number_input("web thickness [mm]",10,40,10)

    if selection == "I":
        section = cm.I_section(steel,height,width,fl_thick,web_thick)
    elif selection == "U":
        section = cm.U_section(steel,height,width,fl_thick,web_thick)
    elif selection == "T":
        section = cm.T_section(steel,height,width,fl_thick,web_thick)

with col2:
    N = st.number_input("Axial load [N]",0)
    Vy = st.number_input("Shear Major [N]",0)
    Vx = st.number_input("Shear Minor [N]",0)
    Mzz = st.number_input("Torsional Moment [Nm]",0)
    Mxx = st.number_input("Moment Major [Nm]",0)
    Myy = st.number_input("Moment Minor [Nm]",0)

results = cm.analyze(section,N,Vx,Vy,Mxx,Myy,Mzz)
st.set_option('deprecation.showPyplotGlobalUse', False)
fig = plt.plot(data = results.plot_stress("vm", cmap="inferno", normalize=False))
st.pyplot(fig)
