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

'''draws the main panel'''
import bpy

class SKBM_PT_MAIN_N(bpy.types.Panel):
    bl_label = 'Shape Key Bookmarks'
    bl_idname = 'SKBM_PT_MAIN_N'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"

    @classmethod
    def poll(cls, context):
        return (
            bpy.context.preferences.addons['shapekey_bookmarks'].preferences.show_N_panel and
            bpy.context.active_object.mode == "POSE")

    def draw_header(self, context):
        pass

    def draw(self, context):
        pass

class SKBM_PT_MAIN_D(bpy.types.Panel):
    bl_label = 'Shape Key Bookmarks'
    bl_idname = 'SKBM_PT_MAIN_D'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'

    @classmethod
    def poll(cls, context):
        return (
            bpy.context.preferences.addons['shapekey_bookmarks'].preferences.show_arm_data and
            bpy.context.active_object.type == "ARMATURE")

    def draw_header(self, context):
        pass

    def draw(self, context):
        pass

def register():
    bpy.utils.register_class(SKBM_PT_MAIN_N)
    bpy.utils.register_class(SKBM_PT_MAIN_D)

def unregister():
    bpy.utils.unregister_class(SKBM_PT_MAIN_N)
    bpy.utils.unregister_class(SKBM_PT_MAIN_D)