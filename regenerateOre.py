#!/usr/bin/env python2
import os
import sys
import time
import logging
import random
import math

install_note = """
  $ virtualenv pyvenv
  $ source pyvenv/bin/activate
  $ pip install cython numpy pyyaml
  $ pip install git+git://github.com/mcedit/pymclevel.git
  """

try:
    from pymclevel import mclevel
except ImportError:
    sys.exit("Cannot import pymclevel. Consider setting it up via %s" %
             install_note)


oreBlock = 804
oreData = 7         #Metadata
amountPerChunk = 18
minGenerateLevel = 0
maxGenerateLevel = 45
amountPerVein = 7
stoneBlock = 1      #pymclevel.infiniteworld.MCLevel.materials.Stone.ID
chunkMAX = 16

logging.basicConfig(
    format='%(asctime)s,%(msecs)-6.1f - %(module)s:%(levelname)s: %(message)s',
    datefmt='%H:%M:%S')
log = logging.getLogger()
log.setLevel(logging.INFO)


def main():
    usage = "%s path/to/world/directory" % os.path.basename(sys.argv[0])
    if not len(sys.argv) == 2:
        sys.exit("One argument is required. Usage: %s" % usage)

    world_directory = sys.argv[1]

    if not os.path.isdir(world_directory):
        sys.exit("Not a directory: %s" % world_directory)

    log.info("Attempting to read world. This scans the directory "
             "for chunks. Might take a while.")
    world = mclevel.fromFile(world_directory)
    random.seed(world.RandomSeed)
    log.info("Resetting python seed to %d" % world.RandomSeed)

    idx, t0 = modifyWorld(world)

    duration = time.time() - t0
    chunks_per_sec = (idx + 1) / duration
    log.info("Total number of modified chunks: %s." % (idx + 1))
    log.info("Duration: %.2f s. Chunks per second: %.2f." % (
        duration, chunks_per_sec))


    # Save the level.dat and any chunks that have been marked for
    # writing to disk. This also compresses any chunks marked for
    # recompression.
    log.info("Save modified world to disk (might take a moment).")
    world.saveInPlace()
    log.info("Exiting.")


def modifyWorld(world):
    log.info("Get chunk positions iterator.")
    chunk_positions = list(world.allChunks)

    t0 = time.time()

    log.info(
        "Iterate through chunks, check if chunk contains Alu and if not generate it.")
    size = 4
    for idx, (x, z) in enumerate(chunk_positions):
        if (idx + 1) % 500 == 0:
            duration = time.time() - t0
            chunks_per_sec = (idx + 1) / duration

            log.info("Processed % 5d/%s chunks. Chunks per second: %.2f." %
                     (idx + 1, world.chunkCount, chunks_per_sec))

        # Retrieve an AnvilChunk object. This object will load and
        # decompress the chunk as needed, and remember whether it
        # needs to be saved or relighted.

        chunk = world.getChunk(x, z)

        # If chunk is not populated, skip addition of ores
        if not chunk.TerrainPopulated:
            continue
        # if chunk already contains wanted Block, skip chunk
        elif oreBlock in chunk.Blocks:
            oreBlocksMask = (chunk.Blocks == oreBlock)
            if oreData in chunk.Data[oreBlocksMask]:
                log.info("Found Aluminum in (%d, %d)" % (x, z))
                continue
        # if chunk has no stone blocks, skip chunk
        if not stoneBlock in chunk.Blocks:
            log.info("No Stone found in (%d, %d)" % (x, z))
            continue
        else:
            modifyChunk(chunk)

    return idx, t0


def modifyChunk(chunk):
    chunkModified = False
    for i in range(amountPerChunk):
        x = round(random.random() * 16, 0)
        z = round(random.random() * 16, 0)
        y = round(random.random() * max(
            maxGenerateLevel - minGenerateLevel, 0) + minGenerateLevel)

        oreGenerated = generateOre(chunk, random, x, y, z)
        if not chunkModified and oreGenerated:
            chunkModified = True

    if chunkModified:
        chunk.chunkChanged(calcLighting=False)
        return True
    else:
        return False

def generateOre(chunk, random, coord_x, coord_y, coord_z):
    oreGenerated = False

    var6 = random.random() * math.pi
    var7 = coord_x + 8 + math.sin(var6) * amountPerVein / 8.0
    var9 = coord_x + 8 - math.sin(var6) * amountPerVein / 8.0
    var11 = coord_z + 8 + math.cos(var6) * amountPerVein / 8.0
    var13 = coord_z + 8 - math.cos(var6) * amountPerVein / 8.0
    var15 = coord_y + random.random() * 3 - 2
    var17 = coord_y + random.random() * 3 - 2

    for var19 in range(amountPerVein + 1):
        var20 = var7 + (var9 - var7) * var19 / amountPerVein
        var22 = var15 + (var17 - var15) * var19 / amountPerVein
        var24 = var11 + (var13 - var11) * var19 / amountPerVein
        var26 = random.random() * amountPerVein / 16.0
        var28 = (math.sin(var19 * math.pi / amountPerVein) + 1.0) * \
            var26 + 1.0
        var30 = (math.sin(var19 * math.pi / amountPerVein) + 1.0) * \
            var26 + 1.0
        var32 = int(math.floor(var20 - var28 / 2.0))
        var33 = int(math.floor(var22 - var30 / 2.0))
        var34 = int(math.floor(var24 - var28 / 2.0))
        var35 = int(math.floor(var20 + var28 / 2.0))
        var36 = int(math.floor(var22 + var30 / 2.0))
        var37 = int(math.floor(var24 + var28 / 2.0))

        for var38 in range(var32, var35 + 1):
            var39 = (var38 + 0.5 - var20) / (var28 / 2.0)

            if (var39 * var39 < 1.0):

                for var41 in range(var33, var36 + 1):
                    var42 = (var41 + 0.5 - var22) / (var30 / 2.0)

                    if (var39 * var39 + var42 * var42 < 1.0):

                        for var44 in range(var34, var37 + 1):
                            var45 = (var44 + 0.5 - var24) / (var28 / 2.0)

                            if var38 >= chunkMAX or var44 >= chunkMAX:
                                # If variables exceed chunk border, reflect them on the border.
                                # This is NOT compatible with Galacticraft's algorithm
                                #log.error("(%d, %d) exceed chunk border of chunk %s" % (var38, var44, str(chunk.chunkPosition)))
                                var38 %= chunkMAX
                                var44 %= chunkMAX

                            #log.info("successfull generated new ore in chunk %s, (%d, %d, %d)" % (str(chunk.chunkPosition), var38, var41, var44))
                            # chunk.Blocks[x,z,y] has flipped ordering!
                            block = chunk.Blocks[var38, var44, var41]

                            if (var39 * var39 + var42 * var42 + var45 * var45 < 1.0 and block == stoneBlock):
                                # We lack metadata info here!
                                chunk.Blocks[var38, var44, var41] = oreBlock
                                chunk.Data[var38, var44, var41] = oreData
                                oreGenerated = True
    return oreGenerated

if __name__ == '__main__':
    main()
