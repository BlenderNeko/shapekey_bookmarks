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

'''Module containing util functions for addon'''
from typing import Protocol
import re
import bpy

class IsCollectionGroup(Protocol):
    '''Group Prop with a collection named item_collection, and an integerprop named active_ind'''
    item_collection: bpy.types.CollectionProperty
    active_ind: bpy.types.IntProperty

name_split = re.compile(r"\.\d{3}$")

def rereg(cls_name):
    cls = getattr(bpy.types, cls_name)
    bpy.utils.unregister_class(cls)
    cls.bl_category = bpy.context.preferences.addons['shapekey_bookmarks'].preferences.N_panel_cat
    bpy.utils.register_class(cls)

def split_name(name:str):
    '''splits a blender name in its name and duplicate number'''
    if name_split.search(name):
        return (name[:-4], int(name[-3:]))
    return (name, 0)

def make_name_unique(collection:bpy.types.CollectionProperty, name_loc:str, new_name:str):
    '''takes an item, its collection and a name, and makes sure that name is unique within the collection'''
    collisions = [split_name(getattr(x, name_loc)) for x in collection]
    collisions = [x[1] for x in collisions if x[0] == new_name]
    if not collisions:
        return new_name
    collisions = set(collisions)
    for i in range(len(collisions)+1):
        if i not in collisions:
            return f"{new_name}.{i:03d}"

def add_item(collection:IsCollectionGroup):
    '''adds an empty item to a collection and updates the active index'''
    item = collection.item_collection.add()
    collection.active_ind = len(collection.item_collection) - 1
    return item


def remove_active_ind(collection:IsCollectionGroup):
    '''remove the active item from the collection and updates the active index'''
    if len(collection.item_collection) > collection.active_ind:
        collection.item_collection.remove(collection.active_ind)
    if collection.active_ind == len(collection.item_collection):
        collection.active_ind = collection.active_ind - 1


def move_item(collection:IsCollectionGroup, direction:int):
    '''move item up or down in the collection'''
    new_ind = max(0, min(collection.active_ind + direction, len(collection.item_collection) - 1))
    collection.item_collection.move(collection.active_ind, new_ind)
    collection.active_ind = new_ind

def draw_list(layout, context, list_class, list_id,
              list_prop, collection_name :str, active_ind_name :str,
              add_op :str, remove_op: str, reorder_op:str,
              add_args=lambda x: None, remove_args=lambda x: None, reorder_args=lambda x: None):
    row = layout.row(heading='', align=False)
    row.template_list(
        list_class, 
        list_id,
        list_prop, collection_name, 
        list_prop, active_ind_name,
        rows=3)
    col_1 = row.column(heading='', align=False)
    col_2 = col_1.column(heading='', align=True)
    op = col_2.operator(add_op, text='', icon_value=31, emboss=True, depress=False)
    add_args(op)
    op = col_2.operator(remove_op, text='', icon_value=32, emboss=True, depress=False)
    remove_args(op)
    if len(getattr(list_prop, collection_name)) > 0:
        col_3 = col_1.column(heading='', align=True)
        op = col_3.operator(reorder_op, text='', icon_value=7, emboss=True, depress=False)
        reorder_args(op)
        op.direction = -1
        op = col_3.operator(reorder_op, text='', icon_value=5, emboss=True, depress=False)
        reorder_args(op)
        op.direction = 1
    return row
