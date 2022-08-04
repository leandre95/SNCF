import bpy
import os
import re


bl_info = {
    "name": "SNCF",
    "author": "Leandre Le Bizec",
    "version": (1,0),
    "blender": (3, 20, 0),
    "location": "View3D > Export Unity SNC",
    "description": "Verifier le modèle avant l'export",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

#Texture--------------------------------------------------------------------------------------------------

def createBadTextureList():
    badTextureList = []
    goodTexture = re.compile(r"^[DNR]_.*")
    modele = re.compile(r"^modele_.*")
    for image in bpy.data.images:
        if not(image.name == "Render Result" or image.name == "Viewer Node" or modele.match(image.name)):
            if not(goodTexture.match(image.name)):
                badTextureList.append(image)
    return badTextureList



class TextureName(bpy.types.Operator):
    bl_idname="object.texture_name"
    bl_label="Vérifier le nom des textures"
    bl_description="Verifier que les textures respecte la nommenclature suivante : 'D_' ou 'N_' ou 'R_'"
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        bpy.ops.wm.dialog_box_texture('INVOKE_DEFAULT')
        return {"FINISHED"}
    

class DialogBoxTexture(bpy.types.Operator):
    bl_idname = "wm.dialog_box_texture"
    bl_label = "Textures"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    

    def draw(self, context):
        badTextureList = createBadTextureList()
        if (not badTextureList):
            self.layout.label(text = "Toutes les textures sont bien nommées")
        else :
            row = self.layout.row()
            row.box().label(icon='CANCEL')
            row.box().label(text = "ATTENTION, une ou plusieurs sont mal nommées")
            self.layout.label(text = "Nomenclature :")
            self.layout.label(text = "- Modèle : 'modele_...'")
            self.layout.label(text = "- Texture : ")
            self.layout.label(text = "    Diffuse : 'D_...'" )
            self.layout.label(text = "    Normal = 'N_...'" )
            self.layout.label(text = "    Rougthness = 'R_...'" )
            for texture in badTextureList:
                self.layout.box().label(text = "La texture " + texture.name + " est mal nommée")
                  
    
    
#Materiaux--------------------------------------------------------------------------------------------------

def createBadMaterialList():
    badMaterialList = []
    goodMaterial = re.compile(r"^M_.*")
    for material in bpy.data.materials:
        if (material.name != "Dots Stroke"):
            if not(goodMaterial.match(material.name)):
                badMaterialList.append(material)
    return badMaterialList



class MaterialName(bpy.types.Operator):
    bl_idname="object.material_name"
    bl_label="Vérifier le nom des matériaux"
    bl_description="Verifier que les matériaux respecte la nommenclature suivante : 'M_' "
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        bpy.ops.wm.dialog_box_texture('INVOKE_DEFAULT')
        return {"FINISHED"}
    

class DialogBoxMaterial(bpy.types.Operator):
    bl_idname = "wm.dialog_box_texture"
    bl_label = "Textures"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    

    def draw(self, context):
        badMaterialList = createBadMaterialList()
        if (not badMaterialList):
            self.layout.label(text = "Toutes les matériaux sont bien nommées")
        else :
            row = self.layout.row()
            row.box().label(icon='CANCEL')
            row.box().label(text = "ATTENTION, un ou plusieurs matériaux sont mal nommées")
            self.layout.label(text = "Nomenclature :")
            self.layout.label(text = "- Matériaux : 'M_...'")
            for material in badMaterialList:
                self.layout.box().label(text = "Le matériaux " + material.name + " est mal nommé")
                 
    
#Main-------------------------------------------------------------------------------------------------
 
class Nomenclature(bpy.types.Panel):
    bl_label = "Nomenclature"
    bl_idname = "VIEW_3D_PT_Texture"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Export Unity SNCF"       
                    
    def draw(self, context):
        self.layout.column().operator(TextureName.bl_idname) 
        self.layout.column().operator(MaterialName.bl_idname)  
       
classes = [Nomenclature, TextureName, DialogBoxTexture, MaterialName, DialogBoxMaterial]

def register():    
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():    
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    
if __name__ == "__main__":
    register()