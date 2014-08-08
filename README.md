MinecraftPyOreGen
=================

This script is based on
    [repop.py by J. Gehrcke](http://gehrcke.de/2014/07/repopulate-a-minecraft-world-from-the-command-line/)

It uses the pymclevel library from 
    [pymclevel.](https://github.com/mcedit/pymclevel)

Ore Spawning is based on Galacticraft algorithm
    [OverworldGenerator.java](https://github.com/micdoodle8/Galacticraft/blob/master/src/main/java/micdoodle8/mods/galacticraft/core/world/gen/OverworldGenerator.java)



Install
=======

You don't need to install it. You can either copy the repository to your computer

    git clone --recursive https://github.com/EoD/MinecraftPyOreGen

Or you can just download the code

    https://github.com/EoD/MinecraftPyOreGen/archive/master.zip


Usage
=====

    regenerateOre.py path-to-your-savegame


If you want to change the type of Ore which is generated, edit the variable **oreBlock**
to the item ID you want it to replaced by.

__Further variables__

* amountPerChunk	specifies the amount of veins per chunk.
* amountPerVein	specifies the amount of ore in each vein.
* minGenerateLevel  specifies the minimal height of ore spawning.
* maxGenerateLevel  specifies the maximal height of ore spawning.
* stoneBlock	specifies the item ID of the block which is replaced by the ore.
