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
from bpy.types import PropertyGroup
from bpy.props import StringProperty, BoolProperty, CollectionProperty, PointerProperty

class SKBM_Collection(PropertyGroup):
    active_ind: bpy.props.IntProperty(description='active group', default=-1)

class SKBM_CollectionItem(PropertyGroup):
    display_name: bpy.props.StringProperty(name='item_ind', description='name', default='')

class SKBM_key(SKBM_CollectionItem):
    def check_for_keys(self, object):
        return object.type == "MESH" and object.data.shape_keys is not None and len(object.data.shape_keys.key_blocks) > 1
    
    def is_shape_key_valid(self):
        return (
            self.shapekey_object is not None and 
            self.shapekey_object.data.shape_keys is not None and 
            self.shapekey_name in self.shapekey_object.data.shape_keys.key_blocks)

    shapekey_object: PointerProperty(type=bpy.types.Object, poll=check_for_keys, description="Data block holding the shape key")
    shapekey_name: StringProperty( description="name of the shape key")

class SKBM_keys(SKBM_Collection):
    item_collection: CollectionProperty(type=SKBM_key)

class SKBM_group(SKBM_CollectionItem):
    keys: PointerProperty(type=SKBM_keys)

class SKBM_groups(SKBM_Collection):
    item_collection: CollectionProperty(type=SKBM_group)

def register():
    bpy.utils.register_class(SKBM_key)
    bpy.utils.register_class(SKBM_keys)
    bpy.utils.register_class(SKBM_group)
    bpy.utils.register_class(SKBM_groups)
    bpy.types.Armature.SKBM_groups = PointerProperty(type=SKBM_groups)

def unregister():
    del bpy.types.Armature.SKBM_groups
    bpy.utils.unregister_class(SKBM_groups)
    bpy.utils.unregister_class(SKBM_group)
    bpy.utils.unregister_class(SKBM_keys)
    bpy.utils.unregister_class(SKBM_key)