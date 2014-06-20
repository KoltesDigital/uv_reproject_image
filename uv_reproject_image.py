# The MIT License (MIT)
# 
# Copyright (c) 2014 Jonathan Giroux (Bloutiouf)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

bl_info = {
    "name": "Reproject image",
    "author": "Jonathan Giroux (Bloutiouf)",
    "version": (1, 0),
    "blender": (2, 70, 0),
    "location": "UV unwrap > Reproject image",
    "description": "Reproject UV coords based on image plane",
    "warning": "",
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/UV/Reproject_image",
    "category": "UV"
}

import bmesh, bpy, math, mathutils

class Reference:
    def __init__(self, co, uv):
        self.co = co
        self.uv = uv

class ReprojectImage(bpy.types.Operator):
    """Reproject UV coords based on image plane"""
    bl_idname = "uv.reproject_image"
    bl_label = "Reproject image"
    
    @classmethod
    def poll(cls, context):
        return (context.mode == "EDIT_MESH")
    
    def execute(self, context):
        obj = context.object
        if obj.mode == "EDIT":
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            
            uv_layer = bm.loops.layers.uv.verify()
            bm.faces.layers.tex.verify()
            
            references = []
            
            for f in bm.faces:
                for l in f.loops:
                    if l.vert.select and l[uv_layer].pin_uv:
                        references.append(Reference(l.vert.co, l[uv_layer].uv))
            
            if len(references) < 3:
                self.report({"ERROR"}, "Please pin the reference plane's vertices (in UV Editor) and add them to the selection (in 3D View).")
            else:
                if len(references) > 3:
                    self.report({"WARNING"}, "The reference plane is defined by more than 3 points, incoherencies may arise.")
                
                # x and y are not necessarily the horizontal and vertical axes
                base_co = references[0].co
                x = references[1].co - base_co
                y = references[2].co - base_co
                normal = x.cross(y)
                
                base_uv = references[0].uv
                u = references[1].uv - base_uv
                v = references[2].uv - base_uv
                
                to_uv = mathutils.Matrix([x, y, normal]).inverted() * mathutils.Matrix([u, v, [0, 0]])
                
                for f in bm.faces:
                    for l in f.loops:
                        luv = l[uv_layer]
                        if l.vert.select and not luv.pin_uv:
                            luv.uv = base_uv + (l.vert.co - base_co) * to_uv
        
                bmesh.update_edit_mesh(me)
        
        return {"FINISHED"}


def menu_match_image_plane(self, context):
    self.layout.operator(ReprojectImage.bl_idname)

def register():
    bpy.utils.register_class(ReprojectImage)
    bpy.types.VIEW3D_MT_uv_map.append(menu_match_image_plane)

def unregister():
    bpy.types.VIEW3D_MT_uv_map.remove(menu_match_image_plane)
    bpy.utils.unregister_class(ReprojectImage)

if __name__ == "__main__":
    register()
