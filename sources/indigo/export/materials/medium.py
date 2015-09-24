# -*- coding: utf8 -*-
#
# ***** BEGIN GPL LICENSE BLOCK *****
#
# --------------------------------------------------------------------------
# Blender 2.5 Indigo Add-On
# --------------------------------------------------------------------------
#
# Authors:
# Doug Hammond, Marco Goebel
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
#
# ***** END GPL LICENCE BLOCK *****
#
from indigo.export import xml_builder
from indigo.export.materials.Base        import MaterialBase
from indigo.export.materials.spectra    import rgb, uniform

class medium_xml(xml_builder):
    
     def build_xml_element(self, scene,medium_name, medium_data ):
        xml = self.Element('medium')
        self.build_subelements(scene, self.get_format(), xml)
        return xml
    
     def __init__(self, scene,medium_name, medium_index, medium_data):
        self.medium_name = medium_name
        self.medium_index = medium_index
        self.medium_data = medium_data
    
     def get_format(self):
        medium_data = self.medium_data.medium_type
        
        fmt = {
            'name': [self.medium_name + '_medium']}
        if self.medium_index != -1:
                fmt.update( {'uid': [self.medium_index + 10 ],})  # indigo uid starts at 10
        fmt.update( {'precedence': [self.medium_data.precedence],
            self.medium_data.medium_type: {}
        })
        
        if self.medium_data.medium_type == 'basic':
            fmt[self.medium_data.medium_type] = {
                'ior': [self.medium_data.medium_ior],
                'cauchy_b_coeff': [self.medium_data.medium_cauchy_b],
                'max_extinction_coeff': [self.medium_data.max_extinction_coeff]
            }
            if self.medium_data.medium_type_SP_type == 'rgb':
                SP = rgb([(1.0-i)*self.medium_data.medium_type_SP_rgb_gain for i in self.medium_data.medium_type_SP_rgb])
            elif self.medium_data.medium_type_SP_type == 'uniform':
                SP = uniform([
                    self.medium_data.medium_type_SP_uniform_val * \
                    10**self.medium_data.medium_type_SP_uniform_exp
                ])
            
            fmt[self.medium_data.medium_type]['absorption_coefficient'] = { 'constant': SP }
            
            if self.medium_data.sss:
                 if self.medium_data.sss_scatter_SP_type == 'rgb':
                    SCS = rgb([i*self.medium_data.sss_scatter_SP_rgb_gain for i in self.medium_data.sss_scatter_SP_rgb])
                 elif self.medium_data.sss_scatter_SP_type == 'uniform':
                    SCS = uniform([
                        self.medium_data.sss_scatter_SP_uniform_val * \
                        10**self.medium_data.sss_scatter_SP_uniform_exp
                    ])
                
                 if self.medium_data.sss_phase_function == 'uniform':
                    PF = { 'uniform': {} }
                 elif self.medium_data.sss_phase_function == 'hg':
                    if self.medium_data.sss_phase_hg_SP_type == 'rgb':
                        PF_HG_GS = rgb([i*self.medium_data.sss_phase_hg_SP_rgb_gain for i in self.medium_data.sss_phase_hg_SP_rgb])
                    elif self.medium_data.sss_phase_hg_SP_type == 'uniform':
                        PF_HG_GS = uniform([
                            self.medium_data.sss_phase_hg_SP_uniform_val * \
                            10**self.medium_data.sss_phase_hg_SP_uniform_exp
                        ])
                    PF = {
                        'henyey_greenstein': {
                            'g_spectrum': PF_HG_GS
                        }
                    }
                 fmt[self.medium_data.medium_type]['subsurface_scattering'] = {
                    'scattering_coefficient_spectrum': SCS,
                    'phase_function': PF,
                }
         
        elif self.medium_data.medium_type == 'dermis':
            fmt[self.medium_data.medium_type] = {
                'hemoglobin_fraction': [self.medium_data.medium_haemoglobin],
            }
        elif self.medium_data.medium_type == 'epidermis':
            fmt[self.medium_data.medium_type] = {
                'melanin_fraction': [self.medium_data.medium_melanin],
                'melanin_type_blend': [self.medium_data.medium_eumelanin],
            }
        return fmt


