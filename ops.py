# ##### BEGIN GPL LICENSE BLOCK #####
#
# Part of the Asset_IO package.
# Operators: Extra operators used by Asset_IO.
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

class BLIB_OT_select_all(bpy.types.Operator):
    bl_idname = "blib.sel_all"
    bl_label = "Select All"
    bl_description = "Select all assets in the list"
    
    asset_type = bpy.props.StringProperty()
 
    def execute(self, context):
        assets = getattr(context.scene.blib.assets, self.asset_type).assets
        for asset in assets:
            asset.state = True
        return{'FINISHED'}

class BLIB_OT_select_none(bpy.types.Operator):
    bl_idname = "blib.sel_none"
    bl_label = "Select None"
    bl_description = "Deselect all assets in the list"
    
    asset_type = bpy.props.StringProperty()
 
    def execute(self, context):
        assets = getattr(context.scene.blib.assets, self.asset_type).assets
        for asset in assets:
            asset.state = False
        return{'FINISHED'}
