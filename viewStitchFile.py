import polyscope as ps
import numpy as np
import argparse


def load_st_file(path):
    positions = []
    yarns = []
    types = []
    ins = []
    outs = []

    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line == "" or line.startswith("#"):
                continue

            parts = line.split()
            if len(parts) != 10:
                print("Skipping malformed line:", line)
                continue

            yarn = int(parts[0])
            stype = parts[1]

            # direction is unused ('a', 'b', etc.)
            try: in0 = int(parts[3])
            except: in0 = -1
            try: in1 = int(parts[4])
            except: in1 = -1
            try: out0 = int(parts[5])
            except: out0 = -1
            try: out1 = int(parts[6])
            except: out1 = -1

            # Position may be nan
            try:
                x = float(parts[7])
                y = float(parts[8])
                z = float(parts[9])
            except:
                x, y, z = 0.0, 0.0, 0.0

            yarns.append(yarn)
            types.append(stype)
            ins.append((in0, in1))
            outs.append((out0, out1))
            positions.append([x, y, z])

    positions = np.array(positions)
    N = len(positions)

    # Wale edges
    wale_edges = set()
    for i in range(N):
        for j in ins[i]:
            if j != -1:
                wale_edges.add((i, j))
        for j in outs[i]:
            if j != -1:
                wale_edges.add((i, j))

    # Course edges
    course_edges = set()
    last_of_yarn = {}
    for i, yarn in enumerate(yarns):
        if yarn in last_of_yarn:
            prev = last_of_yarn[yarn]
            course_edges.add((prev, i))
        last_of_yarn[yarn] = i

    edges = np.array(list(wale_edges | course_edges))
    return positions, edges, yarns, types


def compute_edge_directions(pos, edges):
    midpoints = []
    vectors = []

    for (i, j) in edges:
        p_i = pos[i]
        p_j = pos[j]

        mid = 0.5 * (p_i + p_j)
        vec = p_j - p_i

        # normalize small arrows for visibility
        n = np.linalg.norm(vec)
        if n > 1e-12:
            vec = vec / n * 0.01

        midpoints.append(mid)
        vectors.append(vec)

    return np.array(midpoints), np.array(vectors)


def main():
    parser = argparse.ArgumentParser(description="Polyscope viewer for .st stitch graphs")
    parser.add_argument("stfile", type=str, help="Path to the .st file")
    args = parser.parse_args()

    pos, edges, yarns, types = load_st_file(args.stfile)
    print(f"Loaded {len(pos)} stitches and {len(edges)} edges")

    ps.init()

    # Curve network
    net = ps.register_curve_network(
        "knit graph",
        pos,
        edges[:, :2],
        radius=0.003
    )

    # Yarn ID coloring
    yarn_arr = np.array(yarns)
    net.add_scalar_quantity("yarn_id", yarn_arr, defined_on="nodes",
                            cmap="rainbow", enabled=True)

    # Per-stitch-type masks
    unique_types = sorted(set(types))
    type_arr = np.array(types)

    for stype in unique_types:
        mask = np.array([1.0 if t == stype else 0.0 for t in type_arr])
        net.add_scalar_quantity(
            f"{stype}_only",
            mask,
            defined_on="nodes",
            cmap="blues",
            enabled=False
        )

    # Categorical stitch type
    type_index = {t: i for i, t in enumerate(unique_types)}
    type_numeric = np.array([type_index[t] for t in types])
    net.add_scalar_quantity(
        "stitch_type",
        type_numeric,
        defined_on="nodes",
        cmap="tab10",
        enabled=False
    )

    # Directed arrows
    midpoints, vectors = compute_edge_directions(pos, edges)

    # pc = ps.register_point_cloud("edge_midpoints", midpoints, enabled=False)

    # # *** IMPORTANT: Only allowed arguments ***
    # pc.add_vector_quantity(
    #     "edge_directions",
    #     vectors,
    #     enabled=True
    # )

    ps.show()


if __name__ == "__main__":
    main()
