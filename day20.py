from textwrap import dedent

import numpy as np
from numpy.lib.stride_tricks import as_strided

def edge2bin(edge):
    """Return a binary number from a 1d boolean array as bitmask."""
    edgehash = (2**np.arange(edge.size) * edge).sum()
    return edgehash


def day20(inp):
    blocks = inp.strip().split('\n\n')

    n = int(len(blocks)**0.5)  # number of patches

    imgs = {}
    edgehashes = {}  # ID -> (array of edge hashes, set of edge hashes)
    for block in blocks:
        first, *rest = block.splitlines()
        imgid = int(first[:-1].split()[-1])
        img = np.array(list(map(list, rest))) == '#'

        # store each image
        imgs[imgid] = img

        # also store edge values as binary numbers with both direction
        edge_indices = [
            (0, ...),
            (-1, ...),
            (..., 0),
            (..., -1),
        ]
        hashes = []
        for edge_index in edge_indices:
            edge = img[edge_index]
            for arr in edge, edge[::-1]:
                edgehash = edge2bin(arr)
                hashes.append(edgehash)
        edgehashes[imgid] = set(hashes)
    m = img.shape[0]  # patch linear size

    # compare hashes to see who might match with whom
    corners, edges, middles = {}, {}, {}
    neighbours = {}
    for imgid, hashes in edgehashes.items():
        other_neighbours = {otherid for otherid, other_hashes in edgehashes.items()
                                    for other_hash in other_hashes
                                    if otherid != imgid and hashes & other_hashes
                           }
        num_neighbours = len(other_neighbours)
        if num_neighbours == 2:
            bag = corners
        elif num_neighbours == 3:
            bag = edges
        else:
            bag = middles
        bag[imgid] = other_neighbours  # might be mostly needless
        neighbours[imgid] = other_neighbours

    # part 1 doesn't actually need us to assemple the map
    part1 = np.prod([*corners])

    # start filling in tiles from a corner
    # there's legroom for an arbitrary global rotation/flipping
    # so we can put one of the corners anywhere in any configuration
    # without loss of generality
    #
    # fill a corner -> some of its neighbours will be new corners -> repeat

    # slices for each edge (up, down, left, right):
    edge_indices = [
        (0, ...),
        (-1, ...),
        (..., 0),
        (..., -1),
    ]
    # corresponding index delta for a neighbour along the same edge:
    deltas = [
        [-1, 0],
        [1, 0],
        [0, -1],
        [0, 1],
    ]

    cornerid = next(iter(corners))
    pos_indices = {}
    pos = (0, 0)
    pos_indices[cornerid] = pos
    to_visit = neighbours[cornerid]
    found_imgids = {cornerid}
    while to_visit:
        imgid = to_visit.pop()
        img = imgs[imgid]
        neighbourids = neighbours[imgid]

        # align this image to its already found neighbour
        fixed_neighbid = next(id for id in neighbourids if id in found_imgids)
        fixed_neighbpos = np.array(pos_indices[fixed_neighbid])

        # put this image in the superimage
        # can't be assed to update and decode hashes again, so just brute force this part
        matching_hashes = edgehashes[imgid] & edgehashes[fixed_neighbid]
        for i_edge, edge_index in enumerate(edge_indices):
            # hash the edges again
            neighbedge = imgs[fixed_neighbid][edge_index]
            edgehash = edge2bin(neighbedge)
            if edgehash in matching_hashes:
                # we've found the two matching edges
                delta = deltas[i_edge]
                if 0 <= i_edge <= 1:
                    i_edge_other_side = 0 if i_edge == 1 else 1
                else:
                    i_edge_other_side = 2 if i_edge == 3 else 3
                break
        else:
            raise Exception('Unmatched edge found!')

        # delta gives the index offset of img compared to its known neighbour
        this_pos = tuple(fixed_neighbpos + delta)
        pos_indices[imgid] = this_pos
        # i_edge_other_side indexes the slice that corresponds to the overlapping edge on img
        # loop over every configuration in img until the two edges match in the right place
        this_edge_index = edge_indices[i_edge_other_side]
        found_orientation = False
        for i_flip in range(2):
            for rot_count in range(4):
                if np.array_equal(img[this_edge_index], neighbedge):
                    found_orientation = True
                    break
                img[...] = np.rot90(img)  # rotate
            if found_orientation:
                break
            img[...] = img[::-1, :]  # flip
        else:
            raise Exception('Unmatched image found!')

        # make our neighbours edges and corners if they weren't already
        # and add new corners to the TODO list
        for neighbourid in neighbourids:
            if neighbourid in edges:
                second_neighbourids = edges.pop(neighbourid)
                corners[neighbourid] = second_neighbourids
            elif neighbourid in middles:
                second_neighbourids = middles.pop(neighbourid)
                edges[neighbourid] = second_neighbourids
            if neighbourid in corners.keys() - found_imgids:
                to_visit.add(neighbourid)

        found_imgids.add(imgid)

    # now shift the indices in pos_indices to build the image array
    # (in whatever configuration it is)
    superimg = np.zeros((n, n, m, m), dtype=bool)
    min_i, min_j = min(pos_indices.values())
    for imgid, (i, j) in pos_indices.items():
        img = imgs[imgid]
        superimg[i - min_i, j - min_j, ...] = img

    # now the easy part: stitch the images and find the monsters

    # convert to a single image without inner borders
    superimg = superimg[..., 1:-1, 1:-1].transpose(0, 2, 1, 3).reshape(n*(m - 2), n*(m - 2))

    # define a monster pattern
    monster_str = dedent("""
                          # 
        #    ##    ##    ###
         #  #  #  #  #  #   
        """).strip('\n')
    monster = np.array(list(map(list, monster_str.splitlines()))) == '#'
    mshape = monster.shape
    monster_pixels = monster.sum()
    monster_x, monster_y = monster.nonzero()

    # at the end we still have 8 equivalent configurations to consider
    for flip_count in range(2):
        for rot_count in range(4):
            strides = superimg.strides
            shape = (n*(m-2) - mshape[0] + 1, n*(m-2) - mshape[1] + 1,) + mshape
            windowed = as_strided(superimg, shape=shape, strides=strides*2)

            monster_match = windowed[:, :, monster_x, monster_y].all(-1)
            monster_count = monster_match.sum()

            if monster_count:
                # we've got the right orientation; bail out
                # assume that monsters don't overlap
                # and that they are only visible in a single configuration as suggested by the description
                part2 = superimg.sum() - monster_count * monster_pixels

                return part1, part2

            superimg = np.rot90(superimg)

        superimg = superimg[::-1, :]


if __name__ == "__main__":
    testinp = open('day20.testinp').read()
    print(day20(testinp))
    inp = open('day20.inp').read()
    print(day20(inp))
