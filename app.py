import streamlit as st
import non_standard as ns
from matplotlib import pyplot as plt
import sections as sec
import re
st.header("Section Designer")

materials = ["S235","S355","S460"]
sections = ["I","U","T","Catalogue"]
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

    if selection == "Catalogue":
        types = ["IPE","HE A","HE B","HE M"]
        type = st.selectbox("Type",types)
        if type =="IPE":
            names = sec.pfi_sections().loc[sec.pfi_sections()["Section"].str.contains(type)]
        else:
            x = type.split()
            idx = sec.pfi_sections().index[(sec.pfi_sections()["Section"].str.contains(x[0])) & (sec.pfi_sections()["Section"].str.contains(x[1]))]
            names = sec.pfi_sections().loc[idx]
        name = st.selectbox("Name",names)
        section = sec.pfi_sections().loc[sec.pfi_sections()["Section"]== name].squeeze()
        analytical = sec.analytical_section(section,i)
    else:
        height = st.number_input("height [mm]",10,1000,200)
        width = st.number_input("width [mm]",10,1000,200)
        fl_thick = st.number_input("flange thickness [mm]",10,40,10)
        web_thick = st.number_input("web thickness [mm]",10,40,10)
        radius = st.number_input("radius [mm]",0,40,0)
        steel = ns.create_material(i)
        if selection == "I":
            section = ns.I_section(steel,height,width,fl_thick,web_thick,radius)
        elif selection == "U":
            section = ns.U_section(steel,height,width,fl_thick,web_thick,radius)
        elif selection == "T":
            section = ns.T_section(steel,height,width,fl_thick,web_thick,radius)
        analytical = ns.mesh(section)

with col2:
    N = st.number_input("Axial load [N]",0)
    Vx = st.number_input("Shear Major [N]",0)
    Vy = st.number_input("Shear Minor [N]",0)
    Mzz = st.number_input("Torsional Moment [Nm]",0)
    Myy = st.number_input("Moment Major [Nm]",0)
    Mxx = st.number_input("Moment Minor [Nm]",0)

results = sec.analyze_visualize(analytical,N,Vx,Vy,Mxx,Myy,Mzz)

#analytical.calculate_stress(N,Vx,Vy,0.,0.,Mxx,Myy,Mzz).plot_stress("vm", cmap="inferno", normalize=False)
#results = cm.analyze(section,N,Vx,Vy,Mxx,Myy,Mzz)
st.set_option('deprecation.showPyplotGlobalUse', False)
fig = plt.plot(data = results)
st.pyplot(fig)
result = sec.analyze(analytical,N,Vx,Vy,Mxx,Myy,Mzz)
st.dataframe(result.to_frame().T,hide_index=True)