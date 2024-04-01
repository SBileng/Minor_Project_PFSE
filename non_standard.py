import sectionproperties as sp
from sectionproperties.pre.geometry import Geometry, CompoundGeometry
from sectionproperties.pre.library import steel_sections as steel_geo
from sectionproperties.analysis.section import Section
from sectionproperties.pre import Material
from dataclasses import dataclass

from matplotlib import pyplot as plt


def create_material(yield_strength:int=355, elastic_modulus:int=210e3,poissons_ratio:int=0.3,density:int=7.85e-6) -> Material:
        return Material("non Standard",elastic_modulus,poissons_ratio,yield_strength,density,color="grey")

@dataclass
class section:

    material:Material
    height:float
    width:float
    fl_thick:float
    web_thick:float
    radius:float = 0

@dataclass
class I_section(section):

    def geo(self):
        return steel_geo.i_section(self.height,self.width,self.fl_thick,self.web_thick, self.radius,10,self.material)    
   
@dataclass
class U_section(section):

    def geo(self):
        return steel_geo.channel_section(self.height,self.width,self.fl_thick,self.web_thick, self.radius,10,self.material)    

@dataclass
class T_section(section):

    def geo(self):
        return steel_geo.tee_section(self.height,self.width,self.fl_thick,self.web_thick, self.radius,10,self.material)    

def mesh(section:Geometry,size:float=100):
    sec = section.geo()
    sec.create_mesh(sec.calculate_area()/100)
    return Section(sec)
