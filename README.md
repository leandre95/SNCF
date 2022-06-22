# Documentation technique


## Classe = Operateur

`TextureName` : Classe permettant de créer l'operateur `textureName`.

`Ngon` : Classe permettant de créer l'opérateur ngon.

## Fonction 

`docName()` : Verifier la synthaxe du nom du document lors de l'export ( finalement pas utilisé ).

### Fonction sur les Textures

`createTextureDict()` : Créer un dictionnaire des textures.Renvoie le dictionnaire.

`missingTexture()` : Définir s'il manque des texture. En parcourant le dictionnaire créer précédement. Renvoie un booléen.

`findWrongTexture(self)` : Trouver les texture mal nommé du projet, s'il y en a et les afficher.

`allTexture(self)` : Vérfier le nom des textures du projets, fait appel au `self` appelé dans `execute(self)` de la classe `TextureName`.

### Fonction sur les N-gones

`activeEditMode` : Activer le mode edition et désélectionner tous les objets.

`activeWireframe` : Transformer le mesh séléctionné. Seulement les bords sont conservés.

`createNgonList` : Créer la liste des N-gones du mesh séléctionné.

`ngon` : Vérifier s'il existe des N-gones dans la scènes et les affiches sur la View3D.

## UI

`MyPanel` : Classe héritante du type panel de blender -> permet de créer un nouveau panel sur l'interface de blender.

`draw` : méthode dans la classe MyPanel permettant de renseigner le panel créer.

`register` / `unregister` : méthode de l'API blender à appeler dans le Main.



