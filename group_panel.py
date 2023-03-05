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
from .utils import draw_list, add_item, make_name_unique, remove_active_ind, move_item

class SKBM_UL_display_group_list(bpy.types.UIList):

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout
        layout.prop(item, 'display_name', text='', icon_value=693, emboss=False)

    def filter_items(self, context, data, propname):
        flt_flags = []
        for item in getattr(data, propname):
            if not self.filter_name or self.filter_name.lower() in item.name.lower():
                flt_flags.append(self.bitflag_filter_item)
            else:
                flt_flags.append(0)
        return flt_flags, []
    
class SKBM_OT_Add_Group(bpy.types.Operator):
    bl_idname = "skbm.add_group"
    bl_label = "SKBM_add_group"
    bl_description = "Add empty group"
    bl_options = {"UNDO", "INTERNAL"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return True

    def execute(self, context):
        groups = context.active_object.data.SKBM_groups
        item = add_item(groups)
        item.name = make_name_unique(groups.item_collection, 'name', 'Group')
        item.display_name = make_name_unique(groups.item_collection, 'display_name', 'Group')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
    
class SKBM_OT_Remove_Group(bpy.types.Operator):
    bl_idname = "skbm.remove_group"
    bl_label = "SKBM_remove_group"
    bl_description = "Remove active group"
    bl_options = {"UNDO", "INTERNAL"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return len(context.active_object.data.SKBM_groups.item_collection) > 0

    def execute(self, context):
        remove_active_ind(context.active_object.data.SKBM_groups)
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class SKBM_OT_Move_Group(bpy.types.Operator):
    bl_idname = "skbm.move_group"
    bl_label = "SKBM_move_group"
    bl_description = "Move active group up/down"
    bl_options = {"UNDO", "INTERNAL"}
    direction: bpy.props.IntProperty(name='direction', description='which way to move the active item', default=0, subtype='NONE')

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        move_item(context.active_object.data.SKBM_groups, self.direction)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

class SKBM_PT_GROUP(bpy.types.Panel):
    bl_label = 'Group'
    
    
    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        pass

    def draw(self, context):
        layout = self.layout
        draw_list(layout, context,
                  "SKBM_UL_display_group_list",
                  "",
                  context.active_object.data.SKBM_groups,
                  "item_collection",
                  "active_ind",
                  "skbm.add_group",
                  "skbm.remove_group",
                  "skbm.move_group")

class SKBM_PT_GROUP_N(SKBM_PT_GROUP):
    bl_idname = 'SKBM_PT_GROUP_N'
    bl_parent_id = 'SKBM_PT_MAIN_N'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"

class SKBM_PT_GROUP_D(SKBM_PT_GROUP):
    bl_idname = 'SKBM_PT_GROUP_D'
    bl_parent_id = 'SKBM_PT_MAIN_D'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
        
def register():
    #operators
    bpy.utils.register_class(SKBM_OT_Add_Group)
    bpy.utils.register_class(SKBM_OT_Remove_Group)
    bpy.utils.register_class(SKBM_OT_Move_Group)

    #ui
    bpy.utils.register_class(SKBM_UL_display_group_list)
    bpy.utils.register_class(SKBM_PT_GROUP_N)
    bpy.utils.register_class(SKBM_PT_GROUP_D)


def unregister():
    #operators
    bpy.utils.unregister_class(SKBM_OT_Add_Group)
    bpy.utils.unregister_class(SKBM_OT_Remove_Group)
    bpy.utils.unregister_class(SKBM_OT_Move_Group)

    #ui
    bpy.utils.unregister_class(SKBM_UL_display_group_list)
    bpy.utils.unregister_class(SKBM_PT_GROUP_N)
    bpy.utils.unregister_class(SKBM_PT_GROUP_D)
    pass