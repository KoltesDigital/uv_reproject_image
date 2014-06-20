Reproject image
===============

This [Blender](http://blender.org/) addon reprojects UV coords based on a reference image plane. It is intended to work with [Import as planes](http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/Add_Mesh/Planes_from_Images) when you want to retopologize an image.

When your planes are axis-aligned and your retopologized mesh doesn't exceed the reference image, [UV unwrap > Project from view (Bounds)](http://wiki.blender.org/index.php/Doc:2.6/Manual/Textures/Mapping/UV/Unwrapping#Project_From_View) may suffice. Otherwise, this addon will help you.

[Blender Addon catalog entry](http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/UV/Reproject_image)

Installation
------------

Download [this file](https://raw.githubusercontent.com/Bloutiouf/uv_reproject_image/master/uv_reproject_image.py).

In *Blender*, go to *User Preferences* (`File > User Preferences...` or key `Ctrl+Alt+U`). Select the *Addons* section at the top, and click on *Install from File...* at the bottom. Browse to the downloaded file, selection it and click on *Install from File...*. It is now installed but not yet activated.

To activate it, check the box on the right of the addon. Then, you may want to *Save User Settings* in order for this addon to be automatically loaded on startup, otherwise you'll have to activate it again next time you want to use it.

[More information in the Blender wiki](http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python/Add-Ons#Installation_of_an_Add-On)

Usage
-----

[Watch the explanations on Youtube](http://youtu.be/GKWtmlR1Uak)

You have imported an image as a plane (**reference**) and you have retopologized it by creating a new mesh (**target**). They have to be in the same *mesh datablock*. The goal is to make the target vertices to use correct, interpolated UV coordinates. 

1. Switch to the *UV Editing* view at the top of the window, because you'll need a *3D View* and a *UV/Image Editor* together.
2. In the *3D View*, select the **reference** plane. In the *UV/Image Editor*, select the four vertices of the plane (key `A`) and pin them (`UVs > Pin` or key `P`).
3. In the *3D View*, select the **target** mesh (i.e. the vertices that you want to reassign interpolated UV). In the *UV/Image Editor*, you'll notice that they aren't linked with any texture, therefore select the correct texture in the dropdown.
4. In the *3D View*, select the **reference** and **target** meshes (key `A` twice), and execute *UV unwrap > Reproject image* (`Mesh > UV Unwrap...` or key `U`).

Your **target** mesh is now reprojected according to the **reference** plane!

Notes
-----

When you follow the previous steps, you'll see a warning message:

	The reference plane is defined by more than 3 points, incoherencies may arise.

Basically, this message is a reminder that you should keep your reference plane as a rectangle. Indeed, you have pinned 4 vertices, but only 3 are needed to define a plane. The algorithm will always reproject according to three vertices, and you usually don't know which ones they are. If you have kept it as a rectangle, this is good, ignore the message.

The **reference** and **target** meshes may have any position and rotation in space. You don't need to align the view to make it work.

Step 3. is theoretically optional. Blender has this strange behavior of differentiating the texture used in the 3D view and the texture used for the rendering. So even if you don't select an image to use, the **target** mesh will anyway render the proper texture. But you'll find yourself manipulating a gray mesh in the editor, which is not reasonable.

License
-------

MIT License