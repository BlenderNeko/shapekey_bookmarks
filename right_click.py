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

from .utils import make_name_unique

def do_check(context):
    # need an armature
    if len(bpy.data.armatures) == 0:
        return False
    # need active object
    if context.active_object is None:
        return False
    # has to be a mesh
    if context.active_object.type != "MESH":
        return False
    value = getattr(context, "button_pointer", None)
    if value is None:
        return False
    return type(value) is bpy.types.ShapeKey
    

class WM_OT_skbm_bookmark_key(bpy.types.Operator):
    bl_description = "Add shape key to bookmarks"
    bl_idname = "wm.skbm_bookmark_key"
    bl_label = "Bookmark shape key"
    bl_options = {"INTERNAL", "UNDO"}

    def armature_enum(self, context):
        return [(x.name, x.name, x.name) for x in bpy.data.armatures]

    def group_enum(self, context):
        armature = bpy.data.armatures[self.armature]
        return [(x.name, x.display_name, x.display_name) for x in armature.SKBM_groups.item_collection]

    armature: bpy.props.EnumProperty(items=armature_enum, name="Armature")
    create_new: bpy.props.BoolProperty(name="Create new group")
    new_name: bpy.props.StringProperty(name="Group name", default="Group")
    group: bpy.props.EnumProperty(items=group_enum, name="Group")
    display_name : bpy.props.StringProperty(default="Key", name="Bookmark name")
    shape_key_pointer_name : bpy.props.StringProperty()


    @classmethod
    def poll(cls, context):
        # need an armature
        if len(bpy.data.armatures) == 0:
            return False
        # need active object
        if context.active_object is None:
            return False
        # has to be a mesh
        if context.active_object.type != "MESH":
            return False
        return True
    
    def execute(self, context):
        obj = context.active_object
        sk_name = self.shape_key_pointer_name
        groups = bpy.data.armatures[self.armature].SKBM_groups
        if self.create_new or len(bpy.data.armatures[self.armature].SKBM_groups.item_collection) == 0:
            group = groups.item_collection.add()
            group.name = make_name_unique(groups.item_collection, 'name', 'Group')
            group.display_name = make_name_unique(groups.item_collection, 'display_name', self.new_name)
        else:
            group = groups.item_collection[self.group]
        key = group.keys.item_collection.add()
        key.name = make_name_unique(group.keys.item_collection, 'name', 'Key')
        key.display_name = make_name_unique(group.keys.item_collection, 'display_name', self.display_name)
        key.shapekey_object = obj
        key.shapekey_name = sk_name
        return {'FINISHED'}
    
    def draw(self, context):
        layout = self.layout
        col = layout.column()
        col.use_property_split = True
        col.prop(self, 'armature', text='Armature')
        if len(bpy.data.armatures[self.armature].SKBM_groups.item_collection) == 0:
            col.prop(self, 'new_name', text='Group name')
            col.prop(self, 'display_name', text='Bookmark name')
            return
        col.prop(self, 'create_new', text='Make new group')
        if self.create_new:
            col.prop(self, 'new_name', text='Group name')
        else:
            col.prop(self, 'group', text='Group')
        col.prop(self, 'display_name', text='Bookmark name')

    def invoke(self, context, event):
        value =  getattr(context, "button_pointer", None)
        print(value)
        if value is not None:
            self.shape_key_pointer_name = value.name
            self.display_name = value.name
        return context.window_manager.invoke_props_dialog(self, width=300)
    


def draw_menu(self, context):
    if do_check(context):
        layout = self.layout
        layout.separator()
        layout.operator(WM_OT_skbm_bookmark_key.bl_idname)


def register():
    bpy.utils.register_class(WM_OT_skbm_bookmark_key)
    bpy.types.UI_MT_button_context_menu.append(draw_menu)


def unregister():
    bpy.types.UI_MT_button_context_menu.remove(draw_menu)
    bpy.utils.unregister_class(WM_OT_skbm_bookmark_key)