import bpy
import os


bl_info = {
    "name": "SNCF",
    "author": "Leandre Le Bizec",
    "version": (1,0),
    "blender": (3, 20, 0),
    "location": "View3D > SNCF",
    "description": "Proposer des exports pré-enregisté",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

#Operator----------------------------------------------------------------------------------
    
class Export(bpy.types.Operator):
    bl_idname="export.fbx"
    bl_label="Exporter FBX"
    bl_description="Exporter le projet avec les réglage défini"
     
    
    @classmethod
    def poll(cls, context):
        return True
           
    def execute(self, context):
        #filepath
        self.__export_folder = context.scene.export_folder
        if self.__export_folder.startswith("//"):
            self.__export_folder = os.path.abspath(bpy.path.abspath(context.scene.export_folder))
            
        #export selection 
        selectedObjects = False
        activeCollection = False
        if context.scene.mytool.export_selection == 'CASE1' :
            Selected_Objects = True
        else:
            Active_Collection = True
        
        #export template 
        objectTypes={'ARMATURE', 'CAMERA', 'EMPTY', 'LIGHT', 'MESH', 'OTHER'}
        bakeSpaceTransform=False
        bakeAnim=True
        if context.scene.mytool.export_template == 'CASE1' :
            objectTypes={'MESH'}
            bakeSpaceTransform=True
            bakeAnim=False
        elif context.scene.mytool.export_template == 'CASE2' :
            objectTypes={'EMPTY', 'MESH', 'OTHER'}
        else :
            objectTypes={'ARMATURE', 'EMPTY', 'MESH', 'OTHER'}
        
        #export      
        bpy.ops.export_scene.fbx(
            filepath=self.__export_folder + "/" + context.scene.mytool.name + ".fbx", 
            check_existing=True, 
            filter_glob='*.fbx',
            path_mode='AUTO',
            batch_mode='OFF',
                #include
            use_selection=selectedObjects, 
            use_active_collection=activeCollection,
            object_types=objectTypes,
            use_custom_props=False,
                #Transform
            global_scale=1.0, 
            apply_scale_options='FBX_SCALE_NONE',
            axis_forward='-Z', 
            axis_up='Y',
            apply_unit_scale=True, 
            use_space_transform=True, 
            bake_space_transform=bakeSpaceTransform, 
                #Geometry
            mesh_smooth_type='OFF',
            use_subsurf=False,
            use_mesh_modifiers=True, 
            use_mesh_edges=False,
            use_tspace=False, 
                #Armature
            primary_bone_axis='Y', 
            secondary_bone_axis='X',
            armature_nodetype='NULL', 
            use_armature_deform_only=False,
            add_leaf_bones=True,
                #BakeAnimation
            bake_anim=True, 
            bake_anim_use_all_bones=True, 
            bake_anim_use_nla_strips=True, 
            bake_anim_use_all_actions=True, 
            bake_anim_force_startend_keying=True, 
            bake_anim_step=1.0, 
            bake_anim_simplify_factor=1.0,
                #unknown
            embed_textures=False,
            use_batch_own_dir=True, 
            use_metadata=True,
            use_mesh_modifiers_render=True) 
            
        self.report({'INFO'}, "Exported to " + context.scene.export_folder)
        
        return {"FINISHED"}
    

class OpenFolder(bpy.types.Operator):
  
  bl_idname = "wm.export_folder"
  bl_label = "Open folder"
  bl_description = "Open the export folder" 
  bl_options = {'REGISTER'}

  def execute(self, context):
    bpy.ops.wm.path_open(filepath=context.scene.export_folder)
    return {'FINISHED'}
    
#UI-------------------------------------------------------------------------------------------
    
    
class Proporties(bpy.types.PropertyGroup):
    name : bpy.props.StringProperty(name='', default = '')
    bpy.types.Scene.export_folder = bpy.props.StringProperty(name="Export folder", subtype="DIR_PATH", description="Directory to export the fbx files into")
    export_selection : bpy.props.EnumProperty(
        name = '',
        items = [
        ('CASE1','Selected Objects', ''),
        ('CASE2','Active Collection', '')]
    )
    export_template : bpy.props.EnumProperty(
        name = '',
        items = [
        ('CASE1','Objet Statique', ''),
        ('CASE2','Objet animé sans armature', ''),
        ('CASE3','Personnage animé','')]
    ) 

class Export_PT_Panel(bpy.types.Panel):
    bl_label = "Export Unity"
    bl_idname = "VIEW_3D_PT_Export"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Export Unity SNCF"
    
    
                    
    def draw(self, context):
        mytool = context.scene.mytool
        #Dossier de sauvegarde
        self.layout.label(text = "Choisir le dossier d'export : ")
        row = self.layout.row()
        col1 = row.column()
        col1.prop(context.scene, "export_folder", text="")
        col2 = row.column()
        col2.operator(OpenFolder.bl_idname, text='', icon='FILE_TICK')
        #Nom du fichier 
        self.layout.label(text = "Choisir le nom d'export : ")
        self.layout.prop(mytool, "name")
        #Type d'export
        self.layout.label(text = "Limit to : ")
        self.layout.prop(mytool, "export_selection")
        #Template d'export
        self.layout.label(text = "Choisir un réglage : ")
        self.layout.prop(mytool, "export_template")
        #Export
        self.layout.operator(Export.bl_idname)
        

    
classes = [Proporties, Export_PT_Panel, Export, OpenFolder]

def register():    
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.mytool = bpy.props.PointerProperty(type=Proporties)
    
def unregister():  
    del bpy.types.Scene.mytool  
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    
if __name__ == "__main__":
    register()