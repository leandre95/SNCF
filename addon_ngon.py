import bpy


bl_info = {
    "name": "SNCF",
    "author": "Leandre Le Bizec",
    "version": (1,0),
    "blender": (3, 20, 0),
    "location": "View3D > SNCF",
    "description": "Verifier le présence de N-gones",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}


def createNgonDict():
    ngonDict = {}
    for o in bpy.data.objects :
        if o.type == 'MESH' :
            for p in o.data.polygons:
                if p.loop_total > 4 :
                    ngonDict[p] = o     #{ polygone qui a plus de 4 sommets : objet de type mesh qui contient le polygone }
    return ngonDict

def hideOff():
    for o in bpy.data.objects :
        o.hide_set(False)
        
    
def activeWireframe():
    for area in bpy.context.screen.areas: 
            if area.type == 'VIEW_3D':
                space = area.spaces.active
                if space.type == 'VIEW_3D':
                    space.shading.type = 'WIREFRAME'
                                        

def environnement(ngonDict):
    hideOff() # s'assurer qu'aucun objet n'est cahcé  
    bpy.context.view_layer.objects.active = ngonDict[next(iter(ngonDict.keys()))]
    # Selectionner le premier mesh qui a un ngon dans la vue utilisatuer
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action = 'DESELECT')
    activeWireframe()
     
                               
def ngon(self):
    bpy.ops.object.mode_set(mode='OBJECT')
    ngonDict = createNgonDict()
    if len(ngonDict) > 0 :
        environnement(ngonDict)
        bpy.ops.mesh.select_face_by_sides(number=4, type='GREATER')
    bpy.ops.wm.dialog_box_ngon('INVOKE_DEFAULT')
    
    
def selectNgon():
    bpy.ops.mesh.select_all(action = 'DESELECT')
    bpy.ops.object.editmode_toggle()
    ngonDict = createNgonDict()
    list(ngonDict.keys())[0].select = True
    bpy.ops.object.editmode_toggle()
    bpy.ops.view3d.view_selected(use_all_regions=False)  


#Classe----------------------------------------------------------------------------------------

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


class FindNgone(bpy.types.Operator):
    bl_idname="object.find_ngone"
    bl_label="Trouver le N-gone"
    bl_description="Trouver le N-gone séléctionné dans la liste"
    
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        selectNgon()
        return {"FINISHED"}
    
#UI-------------------------------------------------------------------------------------------


class DialogBoxNgon(bpy.types.Operator):
    bl_idname = "wm.dialog_box_ngon"
    bl_label = "N-gones"
    
    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        ngonDict = createNgonDict()
        if len(ngonDict) == 0 :
            row = self.layout.row()
            row.box().label(icon='CHECKMARK')
            row.box().label(text="Aucun N-gone n'ont été trouvé")
        else:
            if len(ngonDict) == 1:
                row = self.layout.row()
                row.box().label(icon='ERROR')
                row.box().label(text = "ATTENTION, 1 N-gone a été trouvé")
            else :
                row = self.layout.row()
                row.box().label(icon='ERROR')
                row.box().label(text = "ATTENTION, " + str(len(ngonDict)) + " N-gones ont été trouvés")
            self.layout.label(text="Les N-gones apparaissent en surbrillance orange sur le mesh")
            self.layout.label(text="Si vous ne trouvez pas les Ngones, cliquez ici : ")
            self.layout.operator(FindNgone.bl_idname)
      


class Ngones(bpy.types.Panel):
    bl_label = "N-gones"
    bl_idname = "VIEW_3D_PT_Ngones"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Export Unity SNCF"       
                    
    def draw(self, context):
        self.layout.operator(Ngone.bl_idname)
        
    
classes = [Ngones, Ngone, DialogBoxNgon, FindNgone]

def register():    
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():    
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    
if __name__ == "__main__":
    register()