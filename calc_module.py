import sectionproperties as sp
from sectionproperties.pre.geometry import Geometry, CompoundGeometry
from sectionproperties.pre.library import steel_sections as steel_geo
from sectionproperties.analysis.section import Section
from sectionproperties.pre import Material
from dataclasses import dataclass

from matplotlib import pyplot as plt


@dataclass
class steel:

    yield_strength:int
    elastic_modulus:int=200e3
    poissons_ratio:int=0.3
    density:int=7.85e-6

    def mat (self) -> Material:
        return Material(name="Steel",elastic_modulus=200e3,poissons_ratio=0.3,density=7.85e-6,yield_strength=500,color="grey")

@dataclass
class section:

    material:Material
  
@dataclass
class I_section(section):

    height:float
    width:float
    fl_thick:float
    web_thick:float
    radius:float = 0

    def geo(self):
        return steel_geo.i_section(self.height,self.width,self.fl_thick,self.web_thick, self.radius,self.material)    
   
@dataclass
class U_section(section):

    height:float
    width:float
    fl_thick:float
    web_thick:float
    radius:float = 0

    def geo(self):
        return steel_geo.channel_section(self.height,self.width,self.fl_thick,self.web_thick, self.radius,self.material)    

@dataclass
class T_section(section):

    height:float
    width:float
    fl_thick:float
    web_thick:float
    radius:float = 0

    def geo(self):
        return steel_geo.tee_section(self.height,self.width,self.fl_thick,self.web_thick, self.radius,self.material)    

@dataclass
class O_section(section):

    diameter:float
    thickness:float
    n:float = 180

    def geo(self):
        return steel_geo.circular_hollow_section(self.diameter,self.thickness,self.n,self.material)  

def str_to_float(s:str) -> float|str:
    """
    Turns a string to a float. If not possible retrns string.
    """
    try: 
        value = float(s)
    except:
        value = s
    return value

def mesh(section:Geometry,size:float=50):
    sec = section.geo()
    sec.create_mesh(size)
    return sec

def image_geo(section:Geometry):
    plt.plot(data = section.geo().plot_geometry())
    plt.savefig("section.png", bbox_inches='tight')

def analyze(section:Geometry,N:float,Vx:float,Vy:float,Mxx:float,Myy:float,Mzz:float,size:float=10)-> Section:
    sec = mesh(section,100)
    my_sec = Section(sec)
    my_sec.calculate_geometric_properties()
    my_sec.calculate_warping_properties()
    my_sec.calculate_plastic_properties()
    return my_sec.calculate_stress(N,Vx,Vy,0.,0.,Mxx,Myy,Mzz,)