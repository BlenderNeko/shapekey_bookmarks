# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import bpy
from bpy.props import BoolProperty, StringProperty
from .main_panel import SKBM_PT_MAIN_N
from .group_panel import SKBM_PT_GROUP_N
from .keys_panel import SKBM_PT_KEYS_N
from .details_panel import SKBM_PT_KEY_DETAILS_N
from .utils import rereg

class SKBM_Preferences(bpy.types.AddonPreferences):
    
    bl_idname = 'shapekey_bookmarks'

    def reload(self, context):
        rereg(SKBM_PT_MAIN_N.bl_idname)
        rereg(SKBM_PT_GROUP_N.bl_idname)
        rereg(SKBM_PT_KEYS_N.bl_idname)
        rereg(SKBM_PT_KEY_DETAILS_N.bl_idname)

    show_N_panel: BoolProperty(default=True, description='show in N-panel')
    N_panel_cat: StringProperty(default="Item", description='N-panel category to display in', update=reload)
    show_arm_data: BoolProperty(default=True, description='show in armature data panel')

    def draw(self, context):
        if not (False):
            layout = self.layout 
            col = layout.column(heading='', align=False)
            col.use_property_split = False
            col.use_property_decorate = False
            col.alignment = 'Expand'.upper()
            row = col.row()
            row.prop(bpy.context.preferences.addons['shapekey_bookmarks'].preferences, 'show_N_panel', text='show in N-panel')
            row = row.row()
            if not self.show_N_panel:
                row.enabled = False
                row.active = False
            row.prop(bpy.context.preferences.addons['shapekey_bookmarks'].preferences, 'N_panel_cat', text='N-panel category')
            
            col.prop(bpy.context.preferences.addons['shapekey_bookmarks'].preferences, 'show_arm_data', text='show in armature data panel')


def register():
    #operators
    bpy.utils.register_class(SKBM_Preferences)

def unregister():
    #operators
    bpy.utils.unregister_class(SKBM_Preferences)
