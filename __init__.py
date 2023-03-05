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

from . import props, pref_panel, main_panel, group_panel, keys_panel, right_click, details_panel
from .utils import rereg
import bpy

bl_info = {
    "name" : "Shape Key Bookmarks",
    "author" : "Nekomata", 
    "description" : "This addon creates a panel attached to a rig that lets you bookmark shape keys.",
    "blender" : (3, 0, 0),
    "version" : (1, 0, 0),
    "location" : "N-panel and/or Armature data tab",
    "warning" : "",
    "doc_url": "", 
    "tracker_url": "", 
    "category" : "Animation"
}

def register():
    props.register()
    pref_panel.register()
    main_panel.register()
    group_panel.register()
    keys_panel.register()
    right_click.register()
    details_panel.register()
    
    rereg(main_panel.SKBM_PT_MAIN_N.bl_idname)
    rereg(group_panel.SKBM_PT_GROUP_N.bl_idname)
    rereg(keys_panel.SKBM_PT_KEYS_N.bl_idname)
    rereg(details_panel.SKBM_PT_KEY_DETAILS_N.bl_idname)

def unregister():
    details_panel.unregister()
    keys_panel.unregister()
    group_panel.unregister()
    main_panel.unregister()
    pref_panel.unregister()
    props.unregister()
    right_click.unregister()