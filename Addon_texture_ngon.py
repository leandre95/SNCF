import bpy
import bmesh
import os
import re

bl_info = {
    "name": "SNCF",
    "author": "Leandre Le Bizec",
    "version": (1, 0),
    "blender": (3, 20, 0),
    "location": "View3D > SNCF",
    "description": "Verifier le modèle avant l'export",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}
   
def docName():  
    path = bpy.data.filepath
    name = os.path.splitext(os.path.basename(path))[0]
    regex = re.compile(r"^(\w)*_(\w)*")
            
    if regex.match(name) is not None:          
        directory = os.path.dirname(path)
        dest = os.path.join(directory,  os.path.splitext(os.path.basename(path))[0]+".obj")
        bpy.ops.export_scene.obj(filepath = dest)
    else:
        print("le nom de du document n'est pas correct")                 
          
                   
def textureName(self):
    badTextureList = []
    goodTexture = re.compile(r"^[DNR]_.*")
    modele = re.compile(r"^modele_.*")
    for image in bpy.data.images:
        if not(image.name == "Render Result" or image.name == "Viewer Node" or modele.match(image.name)):
            if not(goodTexture.match(image.name)):
                badTextureList.append(image)
                msg = "Atention ! La texture : " + image.name + " est mal nommée"
                self.report({'ERROR'}, message = msg)
    if len(badTextureList) == 0 :
        self.report({'INFO'}, message = "Toutes les textures sont bien nommées")
    

def activateEditMode():
    if bpy.context.mode != 'EDIT_MESH' :
        bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action = 'DESELECT')
    
    
def activeWireframe():
    for area in bpy.context.screen.areas: 
            if area.type == 'VIEW_3D':
                space = area.spaces.active
                if space.type == 'VIEW_3D':
                    space.shading.type = 'WIREFRAME'
                    
    
def createNgonList():
    ngonList = []
    for p in bpy.context.active_object.data.polygons:
        if p.loop_total > 4 :
            ngonList.append(p)
    return ngonList
    
                               
def ngon(self):
    activateEditMode()
    ngonList = createNgonList()
    if len(ngonList) > 0 :
        activeWireframe()
        bpy.ops.mesh.select_face_by_sides(number=4, type='GREATER')
        if len(ngonList) == 1 :
            self.report({'ERROR'}, message = str(len(ngonList)) + " N-gone a été trouvé")
        else :
            self.report({'ERROR'}, message = str(len(ngonList)) + " N-gones ont été trouvés")
    else:
        self.report({'INFO'}, message = "Aucun N-gone n'a été trouvé")
        
    
    
#Operateur_Texture-----------------------------------------------------------------------------------------------

class TextureName(bpy.types.Operator):
    bl_idname="object.texture_name"
    bl_label="Vérifier le nom des textures"
    bl_description="Verifier que les textures respecte la nommenclature suivante : 'D_' ou 'N_' ou 'R_'"
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        textureName(self)
        return {"FINISHED"}
    
#Operateur_Ngone-------------------------------------------------------------------------------------------------

class Ngone(bpy.types.Operator):
    bl_idname="object.ngone"
    bl_label="Vérifier les N-gones"
    bl_description="Vérifier que le nombre de sommet des polygones est inférieure ou égale à 4"
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        ngon(self)
        return {"FINISHED"}
    

#UI-------------------------------------------------------------------------------------------------------------                    
                    
class MyPanel(bpy.types.Panel):
    bl_label = "Export"
    bl_idname = "VIEW_3D_PT_Export"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "SNCF"          
                    
    def draw(self, context):
        self.layout.label(text = "Nommenclature :")
        self.layout.label(text = "- Modèle : 'modele_...'")
        self.layout.label(text = "- Texture : ")
        self.layout.label(text = "    Diffuse : 'D_...'" )
        self.layout.label(text = "    Normal = 'N_...'" )
        self.layout.label(text = "    Rougthness = 'R_...'" )
        self.layout.column().operator(TextureName.bl_idname)
        self.layout.label(text = "N-gones")
        self.layout.column().operator(Ngone.bl_idname)
 
def register():
    bpy.utils.register_class(MyPanel)
    bpy.utils.register_class(TextureName)
    bpy.utils.register_class(Ngone)
    
def unregister():
    bpy.utils.unregister_class(MyPanel)
    bpy.utils.register_class(TextureName)
    bpy.utils.register_class(Ngone)
        
        
#Main-----------------------------------------------------------------------------------------------------------
    
    
if __name__ == "__main__":
    register()