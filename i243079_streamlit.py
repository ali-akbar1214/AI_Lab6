import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from i243079_search import (
    hospital_graph,
    locations,
    gbfs,
    a_star
)

st.set_page_config(
    page_title="Hospital Robot Path Finder",
    page_icon="🏥",
    layout="wide"
)

st.title("Emergency Supply Robot: Informed Search Visualizer")
st.write(
    "Choose a start node, a goal node and a search algorithm (GBFS or A*). "
    "The app runs the search on the hospital corridor graph and highlights the "
    "solution path using NetworkX."
)

nodes = list(hospital_graph.keys())

col1, col2, col3 = st.columns(3)

with col1:
    start = st.selectbox(
        "Select Initial Node",
        nodes,
        index=nodes.index("Pharmacy")
    )

with col2:
    goal = st.selectbox(
        "Select Goal Node",
        nodes,
        index=nodes.index("Emergency_Ward")
    )

with col3:
    algorithm = st.selectbox(
        "Select Search Algorithm",
        ["GBFS", "A*"]
    )

if st.button("Run Search"):

    if algorithm == "GBFS":
        path, cost, expansion_order = gbfs(start, goal, hospital_graph)
    else:
        path, cost, expansion_order = a_star(start, goal, hospital_graph)

    if path is None:
        st.error(f"No path found from {start} to {goal}.")

    else:
        G = nx.DiGraph()

        for node, neighbors in hospital_graph.items():
            G.add_node(node)
            for neighbor, weight in neighbors.items():
                G.add_edge(node, neighbor, weight=weight)

        pos = locations
        path_edges = list(zip(path, path[1:]))
        node_colors = [
            "orange" if n in path else "lightblue" for n in G.nodes()
        ]
        edge_colors = [
            "red" if e in path_edges else "gray" for e in G.edges()
        ]
        edge_widths = [
            4 if e in path_edges else 1.5 for e in G.edges()
        ]

        fig, ax = plt.subplots(figsize=(10, 6))

        nx.draw_networkx_nodes(
            G, pos, node_color=node_colors, node_size=2400, ax=ax
        )
        nx.draw_networkx_labels(G, pos, font_size=8, ax=ax)
        nx.draw_networkx_edges(
            G, pos,
            edge_color=edge_colors,
            width=edge_widths,
            arrows=True,
            arrowsize=22,
            node_size=2400,
            ax=ax
        )
        nx.draw_networkx_edge_labels(
            G, pos,
            edge_labels=nx.get_edge_attributes(G, "weight"),
            ax=ax
        )

        ax.set_title(f"{algorithm} Solution Path")
        ax.axis("off")

        st.pyplot(fig)

        st.subheader("Search Result")

        st.write(f"**Algorithm:** {algorithm}")
        st.write(f"**Solution Path:** {' → '.join(path)}")
        st.write(f"**Total Path Cost:** {cost:.2f}")
        st.write(f"**Node Expansion Order:** {' → '.join(expansion_order)}")
