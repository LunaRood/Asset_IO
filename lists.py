# ##### BEGIN GPL LICENSE BLOCK #####
#
# Part of the Asset_IO package.
# Lists: Definition of all the custom UILists used by Asset_IO.
# Copyright (C) 2016  Luca Rood
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

import bpy

class EXPORT_UL_cycles_mat(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, "state", text=item.name, toggle=True, icon_value=bpy.data.materials[item.name].preview.icon_id)

class EXPORT_UL_cycles_grp(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.prop(item, "state", text=item.name, toggle=True, icon='NODETREE')

lists = [
    EXPORT_UL_cycles_mat,
    EXPORT_UL_cycles_grp
]
