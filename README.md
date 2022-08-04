# Installer un add-on

Télécharger les add-ons

Dans Blender :

Edit -> Preferences -> Add-ons -> Install 

et choisir les add-ons que vous venez de télécharger puis les activer.

# Documentation technique

## add-on Nomenclature

`createBadTextureList` : créer la liste des textures mal nommées du projet

`TextureName` : Opérateur qui vérifie le nom des textures du projet

`DialogBoxTexture` : Opérateur gérant la pop-up

`createBadMaterialList` : créer la liste des materiaux mal nommés du projet

`MaterialName` : Opérateur qui vérifie le nom des materiaux du projet

`DialogBoxMaterial` : Opérateur gérant la pop-up


## add-on Ngon

`createNgonDict` : Créer un dictionnaire de Ngone sous la forme { id du polygone qui a plus de 4 sommets : objet de type mesh qui contient ce polygone }.

`hideOff` : Forcer la vu non caché sur tous les objets du projet.

`activeWireframe` : Transformer le mesh séléctionné. Seulement les bords sont conservés.

`environnement` : Placer la scène dans un environnement par défaut ( Tous les objets non caché, en mode EDIT sur le premier Mesh ayant un Ngon, dont rien n'est sélectionné et avec la vu Wireframe activé ).

`ngon` : Vérifier s'il existe des N-gones dans la scènes et les affiches sur la View3D.

`selectNgon` : Sélectionner le premier Ngon du dictionnaire et centrer la caméra dessus.

`Ngon` : Opérateur permettant de créer l'opérateur "Vérifier les N-gones".

`FindNgone` : Opérateur pour créer l'opérateur "Trouver le N-gone".

`DialogBoxNgon` : Opérateur qui gère la pop-up.

## add-on Export

`Export` : Opérateur qui gère l'export du projet.

`filePath` : Choisir le dossier ou sera enregistrer l'export.

`exportLimit` : Choisir la limitation d'export (selection ou collection).

`exportTemplate` : Choisir l'export pré-enregistré.

`export` : Gérer l'export en fonction de ce que l'utilisateur a choisit.

`OpenFolder` : Opérateur qui gère l'ouverture du dosssier d'export 

`Proporties` : Classes des propriétés

name : nom du fichier d'export 

bpy.types.Scene.export_folder : dossier d'export

export_selection : enumeration des choix possible pour les limites d'export

export_template : enumeration des choix possible pour les templates d'exports

  
## UI

`MyPanel` : Classe héritante du type panel de blender -> permet de créer un nouveau panel sur l'interface de blender.

`draw` : méthode dans la classe MyPanel permettant de renseigner le panel créer.

`register` / `unregister` : méthode de l'API blender à appeler dans le Main.



