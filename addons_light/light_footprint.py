import math
import os

import bpy
import bmesh
import mathutils


class MeshAlignVerts(bpy.types.Operator):
    """ tooltip"""
    bl_label = "Align verts pos"
    bl_idname = "mesh.align_verts"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        ...
        return {'FINISHED'}


class LayoutDemoPanel(bpy.types.Panel):
    """ tooltip"""
    bl_label = "Layout Demo"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text=" Simple Row:")
        row = layout.row()
        row.prop(scene, "frame_start")
        row = layout.row(align=True)
        row.operator("render.render")


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_class(__name__)


if __name__ == "__main__":
    register()
