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
from .utils import draw_list, add_item, make_name_unique, remove_active_ind, move_item

class SKBM_UL_display_key_list(bpy.types.UIList):

    def draw_item(self, context, layout: bpy.types.UILayout, data, item :SKBM_key, icon, active_data, active_propname, index):
        row = layout.row()
        row.prop(item, 'display_name', text='', emboss=False, icon="SHAPEKEY_DATA")
        if item.is_shape_key_valid():
            prop = item.shapekey_object.data.shape_keys.key_blocks[item.shapekey_name]
            layout.prop(prop, "value", text='', emboss=False)
            layout.prop(prop, "mute", text='', emboss=False)



    def filter_items(self, context, data, propname):
        flt_flags = []
        for item in getattr(data, propname):
            if not self.filter_name or self.filter_name.lower() in item.display_name.lower():
                flt_flags.append(self.bitflag_filter_item)
            else:
                flt_flags.append(0)
        return flt_flags, []
    
class SKBM_OT_Add_Key(bpy.types.Operator):
    bl_idname = "skbm.add_key"
    bl_label = "SKBM_add_key"
    bl_description = "Add empty key to active group"
    bl_options = {"UNDO", "INTERNAL"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return True

    def execute(self, context):
        active_group_ind = context.active_object.data.SKBM_groups.active_ind
        active_group = context.active_object.data.SKBM_groups.item_collection[active_group_ind]
        item = add_item(active_group.keys)
        item.name = make_name_unique(active_group.keys.item_collection, 'name', 'Key')
        item.display_name = make_name_unique(active_group.keys.item_collection, 'display_name', 'Key')
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)
    
class SKBM_OT_Remove_Key(bpy.types.Operator):
    bl_idname = "skbm.remove_key"
    bl_label = "SKBM_remove_key"
    bl_description = "Remove active key from active group"
    bl_options = {"UNDO", "INTERNAL"}

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return len(context.active_object.data.SKBM_groups.item_collection) > 0

    def execute(self, context):
        active_group_ind = context.active_object.data.SKBM_groups.active_ind
        active_group = context.active_object.data.SKBM_groups.item_collection[active_group_ind]
        remove_active_ind(active_group.keys)
        return {"FINISHED"}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)


class SKBM_OT_Move_Key(bpy.types.Operator):
    bl_idname = "skbm.move_key"
    bl_label = "SKBM_move_key"
    bl_description = "Move active key up/down"
    bl_options = {"UNDO", "INTERNAL"}
    direction: bpy.props.IntProperty(name='direction', description='which way to move the active item', default=0, subtype='NONE')

    @classmethod
    def poll(cls, context):
        if bpy.app.version >= (3, 0, 0) and True:
            cls.poll_message_set('')
        return not False

    def execute(self, context):
        active_group_ind = context.active_object.data.SKBM_groups.active_ind
        active_group = context.active_object.data.SKBM_groups.item_collection[active_group_ind]
        move_item(active_group.keys, self.direction)
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

class SKBM_PT_KEYS(bpy.types.Panel):
    bl_label = 'Keys'
    bl_order = 1

    @classmethod
    def poll(cls, context):
        return True

    def draw_header(self, context):
        pass

    def set_add_op_args(self,op):
        op.input_type = "NONE"

    def draw(self, context):
        layout = self.layout
        active_group_ind = context.active_object.data.SKBM_groups.active_ind
        if active_group_ind < 0:
            layout.label(text="no group selected", icon='ERROR')
            return

        active_group = context.active_object.data.SKBM_groups.item_collection[active_group_ind]
        
        draw_list(layout, context,
                  "SKBM_UL_display_key_list",
                  "",
                  active_group.keys,
                  "item_collection",
                  "active_ind",
                  add_op="skbm.add_key",
                  remove_op="skbm.remove_key",
                  reorder_op="skbm.move_key")

class SKBM_PT_KEYS_N(SKBM_PT_KEYS):
    bl_idname = 'SKBM_PT_KEYS_N'
    bl_parent_id = 'SKBM_PT_MAIN_N'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"

class SKBM_PT_KEYS_D(SKBM_PT_KEYS):
    bl_idname = 'SKBM_PT_KEYS_D'
    bl_parent_id = 'SKBM_PT_MAIN_D'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'


def register():
    #operators
    bpy.utils.register_class(SKBM_OT_Add_Key)
    bpy.utils.register_class(SKBM_OT_Remove_Key)
    bpy.utils.register_class(SKBM_OT_Move_Key)

    #ui
    bpy.utils.register_class(SKBM_UL_display_key_list)
    bpy.utils.register_class(SKBM_PT_KEYS_N)
    bpy.utils.register_class(SKBM_PT_KEYS_D)


def unregister():
    #operators
    bpy.utils.unregister_class(SKBM_OT_Add_Key)
    bpy.utils.unregister_class(SKBM_OT_Remove_Key)
    bpy.utils.unregister_class(SKBM_OT_Move_Key)

    #ui
    bpy.utils.unregister_class(SKBM_UL_display_key_list)
    bpy.utils.unregister_class(SKBM_PT_KEYS_N)
    bpy.utils.unregister_class(SKBM_PT_KEYS_D)
    pass