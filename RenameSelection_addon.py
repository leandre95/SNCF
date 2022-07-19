import bpy

bl_info = {
    "name": "SNCF rename full selection",
    "author": "Leandre Le Bizec",
    "version": (1,0),
    "blender": (3, 20, 0),
    "location": "View3D > SNCF Tools",
    "description": "Renommer une sélection d'objet entière",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

#Classe----------------------------------------------------------------------------------------

class Proporties(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name='')
    
    
class Rename(bpy.types.Operator):
    bl_idname="object.rename"
    bl_label="Renommer la sélection"
    bl_description="Permet de renommer toute la sélection par un nom unique qui s'incrémente"
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        i = 0    
        for obj in bpy.context.selected_objects :
            obj.name = context.scene.mytool.name + str(i)
            i = i+1
       
        return {"FINISHED"}
    
#UI-------------------------------------------------------------------------------------------

class RenameSelection_PT_Panel(bpy.types.Panel):
    bl_label = "Renommer toute une sélection"
    bl_idname = "VIEW_3D_PT_RenameSelection"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SNCF Tools"       
                    
    def draw(self, context):
        mytool = context.scene.mytool
        self.layout.prop(mytool, "name")
        self.layout.operator(Rename.bl_idname)
        
    
classes = [RenameSelection_PT_Panel, Rename, Proporties]

def register():    
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.mytool = bpy.props.PointerProperty(type=Proporties)
    
def unregister():    
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    
if __name__ == "__main__":
    register()