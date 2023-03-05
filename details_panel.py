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
from .props import SKBM_key

class SKBM_PT_KEY_DETAILS(bpy.types.Panel):
    bl_label = 'Details'
    bl_order = 2

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        pass

    def draw(self, context):
        layout = self.layout
        active_group_ind = context.active_object.data.SKBM_groups.active_ind
        if active_group_ind < 0:
            layout.label(text="no group selected", icon='ERROR')
            return

        active_group = context.active_object.data.SKBM_groups.item_collection[active_group_ind]
        active_key_ind = active_group.keys.active_ind
        layout = layout.column()
        if active_key_ind < 0:
            layout.label(text="no key selected", icon='ERROR')
            return
        active_key = active_group.keys.item_collection[active_key_ind]

        layout.use_property_decorate= False
        layout = layout.column(align=True)
        layout.use_property_split = True
        layout.prop(data=active_key , property="display_name", text="Bookmark name")
        layout.prop(data=active_key , property="shapekey_object", text="Object")
        search_data = active_key.shapekey_object.data.shape_keys if active_key.shapekey_object else None
        if search_data:
            layout.prop_search(data = active_key, property="shapekey_name", search_data=search_data, search_property="key_blocks", text="Shape key name")
            

class SKBM_PT_KEY_DETAILS_N(SKBM_PT_KEY_DETAILS):
    bl_idname = 'SKBM_PT_KEY_DETAILS_N'
    bl_parent_id = 'SKBM_PT_MAIN_N'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"

class SKBM_PT_KEY_DETAILS_D(SKBM_PT_KEY_DETAILS):
    bl_idname = 'SKBM_PT_KEY_DETAILS_D'
    bl_parent_id = 'SKBM_PT_MAIN_D'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'


def register():
    bpy.utils.register_class(SKBM_PT_KEY_DETAILS_N)
    bpy.utils.register_class(SKBM_PT_KEY_DETAILS_D)


def unregister():
    bpy.utils.unregister_class(SKBM_PT_KEY_DETAILS_N)
    bpy.utils.unregister_class(SKBM_PT_KEY_DETAILS_D)
    