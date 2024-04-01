import pandas as pd
import pathlib

import sectionproperties as sp
from sectionproperties.pre.geometry import Geometry, CompoundGeometry
from sectionproperties.pre.library import steel_sections as steel_geo
from sectionproperties.analysis.section import Section
from sectionproperties.pre import Material

def pfi_sections() -> pd.DataFrame:
    """
    Returns a Pandas Dataframe with the section information for EU sections from Acelor Mittal.
    """
    file_directory = pathlib.Path().parent.resolve() / "acelor_mittal.csv"
    df = pd.read_csv(file_directory)

    return df

def sections_filter(df: pd.DataFrame, operator: str, **kwargs) -> pd.DataFrame:
    """
    Filter the values of the Dataframe with an operator.
    "ge" operator for greater than.
    "le" operator for lesser than.
    """
    if operator == "ge":
        for key, value in kwargs.items():
                    df_new = df[df[key]>=value]
    elif operator == "le":
            for key, value in kwargs.items():
                    df_new = df[df[key]<=value]
    else:
            raise Exception ("No operator chosen")

    return df_new

def sort_by_weight(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sort the DataFrame based on the weight in ascending order.
    """
    return df.sort_values(by="kg/m")

def analytical_section(series:pd.Series, yield_strength:int=355, elastic_modulus:int=210e3,poissons_ratio:int=0.3,density:int=7.85e-6)-> Section:
    """
    Returns an Analytical section for use with the sectionproperties library
    """
    steel = Material(series["Section"],elastic_modulus,poissons_ratio,yield_strength,density,color="grey")
    section = steel_geo.i_section(series["h"],series["b"],series["tf"],series["tw"],series["r"],10,steel)
    section.create_mesh(series["A"]/100)
    return Section(section)

def analyze(section:Section,N:float=0,Vx:float=0,Vy:float=0,Mxx:float=0,Myy:float=0,Mzz:float=0)-> pd.Series:
    """
    """
    section.calculate_geometric_properties()
    section.calculate_warping_properties()
    section.calculate_plastic_properties()

    mat = section.materials.pop(0)    
    result = max(section.calculate_stress(N,Vy,Vx,0.,0.,Myy,Mxx,Mzz).get_stress().pop(0)["sig_vm"])
    df_dict = {"Name":mat.name,"Steel yield strength":mat.yield_strength,"N":N,"Vx":Vx,"Vy":Vy,"Mzz":Mzz,"Mxx":Mxx,"Myy":Myy,"von Mises":result,"Utilisation":result/mat.yield_strength}
    return pd.Series(df_dict)


def run_analysis(df:pd.DataFrame,yield_strength:int=355,N:float=0,Vx:float=0,Vy:float=0,Mxx:float=0,Myy:float=0,Mzz:float=0)->pd.DataFrame:
    """
    """
    columns = ["Name","Steel yield strength","N","Vx","Vy","Mzz","Mxx","Myy","von Mises","Utilisation"]
    df_results = pd.DataFrame(columns=columns)
    for i in range(len(df)):
          section = analytical_section(df.loc[i],yield_strength)
          result = analyze(section,N,Vx,Vy,Mxx,Myy,Mzz)
          frame = [df_results,result.to_frame().T]
          df_results = pd.concat(frame)
    df_results.reset_index(drop=True,inplace=True)
    return df_results

def analyze_visualize(section:Section,N:float=0,Vx:float=0,Vy:float=0,Mxx:float=0,Myy:float=0,Mzz:float=0)-> pd.Series:
    """
    """
    section.calculate_geometric_properties()
    section.calculate_warping_properties()
    section.calculate_plastic_properties()

    return section.calculate_stress(N,Vy,Vx,0.,0.,Myy,Mxx,Mzz).plot_stress("vm", cmap="viridis", normalize=False)