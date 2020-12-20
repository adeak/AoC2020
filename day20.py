from textwrap import dedent

import numpy as np
from numpy.lib.stride_tricks import as_strided

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
                # bool_ -> intp -> str
                bits = ''.join(arr.astype(int).astype(str))
                edgehash = int(bits, 2)
                hashes.append(edgehash)
        edgehashes[imgid] = np.array(hashes), set(hashes)
    m = img.shape[0]  # patch linear size

    # compare hashes to see who might match with whom
    corners, edges, middles = {}, {}, {}
    neighbours = {}
    for imgid, (hashes, set_hashes) in edgehashes.items():
        other_neighbours = {otherid for otherid, (_, other_hashes) in edgehashes.items()
                                    for other_hash in other_hashes
                                    if otherid != imgid and set_hashes & other_hashes
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

    # start filling in corners
    # there's legroom for an arbitrary global rotation/flipping
    # so we can put one of the corners anywhere in any configuration
    # without loss of generality

    # put the first corner in the top left
    cornerid, neighbourids = corners.popitem()
    neighbourids = list(neighbourids)
    img = imgs[cornerid]
    hashes, set_hashes = edgehashes[cornerid]

    # figure out which direction it should be in by matching to its two neighbours
    for neighbourid in neighbourids:
        # if the neighbour matches to the left or to the top, flip the corner image
        relevant_indices = [i for i, edgehash in enumerate(hashes) if edgehash in edgehashes[neighbourid][1]]

        # there will be duplication do to synchronised flips, so
        # only take the first index
        fixing_index = relevant_indices[0]
    
        # fixing index encodes one of the edges (should be bottom or right):
        # 0, 1 -> top, top flipped
        # 2, 3 -> bottom, bottom flipped
        # 4, 5 -> left, left flipped
        # 6, 7 -> right, right flipped

        fixing_div = fixing_index // 2
        if fixing_div == 0:
            # index was 0 or 1 (top)
            img[...] = img[::-1, :]
        elif fixing_div == 2:
            # index was 4 or 5 (left)
            img[...] = img[:, ::-1]

    # now we can finally but the corner image into the top left
    pos_indices = {}
    superimg = np.zeros((n, n, m, m), dtype=bool)
    pos_indices[cornerid] = np.array([0, 0])
    superimg[0, 0, ...] = img

    # make our neighbours corners
    for neighbourid in neighbourids:
        second_neighbourids = edges.pop(neighbourid)
        corners[neighbourid] = second_neighbourids

    found_imgids = {cornerid}
    to_visit = neighbourids & corners.keys()
    while to_visit:
        imgid = to_visit.pop()
        img = imgs[imgid]
        neighbourids = neighbours[imgid]

        # align this image to its already found neighbours
        fixed_neighbid = next(id for id in neighbourids if id in found_imgids)
        fixed_neighbpos = pos_indices[fixed_neighbid]

        # put this image in the superimage
        # can't be assed to update and decode hashes again,
        # so just brute force this part
        matching_hashes = edgehashes[imgid][1] & edgehashes[fixed_neighbid][1]
        edge_indices = [
            (0, ...),
            (-1, ...),
            (..., 0),
            (..., -1),
        ]
        deltas = [
            [-1, 0],
            [1, 0],
            [0, -1],
            [0, 1],
        ]
        for i_edge, edge_index in enumerate(edge_indices):
            neighbedge = imgs[fixed_neighbid][edge_index]
            bits = ''.join(neighbedge.astype(int).astype(str))
            edgehash = int(bits, 2)
            if edgehash in matching_hashes:
                delta = deltas[i_edge]
                if 0 <= i_edge <= 1:
                    i_edge_other_side = 0 if i_edge == 1 else 1
                else:
                    i_edge_other_side = 2 if i_edge == 3 else 3
                break
        this_edge_index = edge_indices[i_edge_other_side]
        this_pos = fixed_neighbpos + delta
        pos_indices[imgid] = this_pos
        found_orientation = False
        for i_flip in range(2):
            for rot_count in range(4):
                img[...] = np.rot90(img)
                if np.array_equal(img[this_edge_index], neighbedge):
                    found_orientation = True
                    break
            if found_orientation:
                break
            img[...] = img[::-1, :]
        else:
            raise Exception('Unmatched image found!')

        superimg[tuple(this_pos)] = img

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
                part2 = superimg.sum() - monster_count * monster_pixels

                return part1, part2

            superimg = np.rot90(superimg)

        superimg = superimg[::-1, :]


if __name__ == "__main__":
    testinp = open('day20.testinp').read()
    print(day20(testinp))
    #testinp2 = open('day20.testinp2').read()
    #print(day20(testinp2)[1])
    inp = open('day20.inp').read()
    print(day20(inp))
    # 1085 too low
