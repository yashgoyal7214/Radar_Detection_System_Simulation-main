import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from IPython.display import HTML
import heapq

# Constants
GRID_SIZE = 1500
RADAR_POS = (0, 0)
DETECTION_RANGE = 1300
UAV_POS = (900, 700)

# Environment objects
OBJECTS = {
    "NODE_A1": (-400, 350),
    "NODE_A2": (-400, -300),
    "NODE_B1": (200, 200),
    "NODE_B2": (400, -200),
    "NODE_C1": (600, 300),
    "NODE_C2": (700, -100),
    "NODE_D1": (850, 500),
    "NODE_D2": (-300, 700),
}

# Graph nodes and edges
GRAPH_NODES = {
    0: RADAR_POS,
    1: (-400, 350),
    2: (-400, -300),
    3: (200, 200),
    4: (400, -200),
    5: (600, 300),
    6: (700, -100),
    7: (850, 500),
    8: (-300, 700),
    9: UAV_POS
}

def show_radar_environment():
    """Display the radar environment with nodes"""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlim(-GRID_SIZE, GRID_SIZE)
    ax.set_ylim(-GRID_SIZE, GRID_SIZE)
    ax.set_title("RADAR ENVIRONMENT REPRESENTATION (2D)")
    ax.set_xlabel("HORIZONTAL AXIS")
    ax.set_ylabel("VERTICAL AXIS")
    
    ax.plot(*RADAR_POS, 'ro', label='Radar')
    ax.text(RADAR_POS[0] + 10, RADAR_POS[1] + 10, "Radar", color='red')
    
    for name, pos in OBJECTS.items():
        ax.plot(*pos, 'kx')
        ax.text(pos[0] + 10, pos[1] + 10, name, fontsize=9, color='b')
    
    ax.legend()
    plt.close(fig)
    return fig

def show_gaussian_pulse():
    """Generate and display Gaussian modulated pulse"""
    sampling_freq = 10e6  # 10 MHz
    pulse_width = 5e-6    # 5 μs
    env_width = pulse_width / 3
    carrier_freq = 1e6    # 1 MHz
    
    time_vec = np.arange(-pulse_width, pulse_width, 1/sampling_freq)
    gauss_env = np.exp(-0.5*(time_vec/env_width)**2)
    carrier = np.cos(2*np.pi*carrier_freq*time_vec)
    modulated = gauss_env * carrier
    
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
    
    for ax, data, color, title in zip(
        [ax1, ax2, ax3],
        [gauss_env, carrier, modulated],
        ['g', 'b', 'r'],
        ["Gaussian Envelope", "Carrier Wave", "Modulated Signal"]
    ):
        ax.plot(time_vec*1e6, data, color)
        ax.set_ylabel("Amplitude")
        ax.set_title(title)
        ax.grid(True)
    
    plt.tight_layout()
    plt.close(fig)
    return fig
    
def simulate_wave_propagation():
    """Animate radar wave propagation stopping exactly at (950, 700)"""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-GRID_SIZE, GRID_SIZE)
    ax.set_ylim(-GRID_SIZE, GRID_SIZE)
    ax.set_aspect('equal')
    ax.grid(True)
    ax.set_title("--Gaussian Wave Propagation--")
    
    # Define exact target position
    TARGET_POS = np.array([950, 700])
    target_distance = np.linalg.norm(TARGET_POS)
    
    ax.plot(*RADAR_POS, 'go', label='Radar')
    uav_marker = ax.plot([], [], 'ro')[0]
    uav_marker.set_visible(False)
    
    outgoing = ax.plot([], [], 'b--', linewidth=1)[0]
    returning = ax.plot([], [], 'purple', linewidth=1)[0]
    
    def init():
        return outgoing, returning, uav_marker
    
    def update(frame):
        wave_speed = target_distance / 100  # Dynamic speed to reach target in 100 frames
        pause_frames = 15
        
        # Phase calculations
        outgoing_frames = 100
        returning_frames = 100
        total_frames = outgoing_frames + pause_frames + returning_frames
        
        if frame < outgoing_frames:  # Outgoing to target
            progress = min(frame / outgoing_frames, 1)
            radius = progress * target_distance
            theta = np.linspace(0, 2*np.pi, 200)
            outgoing.set_data(radius*np.cos(theta), radius*np.sin(theta))
            
            if progress >= 0.99:  # Detection threshold
                uav_marker.set_data([TARGET_POS[0]], [TARGET_POS[1]])
                uav_marker.set_visible(True)
                uav_marker.set_label("Target Detected")
                ax.legend()
        
        elif outgoing_frames <= frame < outgoing_frames + pause_frames:  # Pause
            pass
            
        else:  # Returning to radar
            return_progress = min((frame - outgoing_frames - pause_frames) / returning_frames, 1)
            radius = (1 - return_progress) * target_distance
            theta = np.linspace(0, 2*np.pi, 200)
            returning.set_data(radius*np.cos(theta), radius*np.sin(theta))
            
            if return_progress >= 0.99:  # Complete return
                returning.set_data([0], [0])
                
        return outgoing, returning, uav_marker
    
    # Animation parameters
    ani = animation.FuncAnimation(
        fig, update,
        frames=215,  # 100 outgoing + 15 pause + 100 returning
        init_func=init,
        interval=50,
        blit=True,
        repeat=False
    )
    plt.close(fig)
    return HTML(ani.to_jshtml())
    
    
def show_detection_range():
    """Show radar detection range with UAV"""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlim(-GRID_SIZE, GRID_SIZE)
    ax.set_ylim(-GRID_SIZE, GRID_SIZE)
    ax.set_title("RADAR ENVIRONMENT REPRESENTATION (2D) with Detection Range")
    ax.set_xlabel("HORIZONTAL AXIS")
    ax.set_ylabel("VERTICAL AXIS")
    
    circle = plt.Circle(RADAR_POS, DETECTION_RANGE, color='cyan', fill=False,
                       linestyle='--', linewidth=1.5, label="Detection Range")
    ax.add_patch(circle)
    
    ax.plot(*RADAR_POS, 'ro', label='Radar')
    ax.text(RADAR_POS[0] + 10, RADAR_POS[1] + 10, "Radar", color='red')
    
    for name, pos in OBJECTS.items():
        ax.plot(*pos, 'kx')
        ax.text(pos[0] + 10, pos[1] + 10, name, fontsize=9, color='b')
    
    ax.plot(*UAV_POS, marker='^', markersize=10, color='green', label="UAV detected")
    ax.text(UAV_POS[0] + 10, UAV_POS[1] + 10, "UAV DETECTED", 
            color='green', fontsize=10, fontweight='bold')
    
    ax.legend()
    plt.close(fig)
    return fig

def plot_raw_graph():
    """Plot the raw graph without edges"""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlim(-GRID_SIZE, GRID_SIZE)
    ax.set_ylim(-GRID_SIZE, GRID_SIZE)
    ax.set_title("RAW GRAPH FOR DIJKSTRA'S ALGORITHM")

    ax.plot(GRAPH_NODES[0][0], GRAPH_NODES[0][1], 'ro', label="Radar")
    ax.text(GRAPH_NODES[0][0] + 10, GRAPH_NODES[0][1] + 10, "0", color='red')

    for node, pos in GRAPH_NODES.items():
        if node != 0 and node != 9:
            ax.plot(*pos, 'kx')
            ax.text(pos[0] + 10, pos[1] + 10, str(node), fontsize=9, color='b')

    ax.plot(GRAPH_NODES[9][0], GRAPH_NODES[9][1], marker='^', markersize=10,
            color='green', label="UAV detected")
    ax.text(GRAPH_NODES[9][0] + 10, GRAPH_NODES[9][1] + 10,
            "9", color='green', fontsize=10, fontweight='bold')

    ax.legend()
    plt.close(fig)
    return fig

def get_altitude_and_edges():
    """Return altitude data and edge weights"""
    altitude = {
        0: 100, 1: 250, 2: 180, 3: 500, 4: 300,
        5: 200, 6: 310, 7: 650, 8: 320, 9: 900
    }

    edges = {
        (0, 3): altitude[3] - altitude[0],
        (3, 7): altitude[7] - altitude[3],
        (7, 9): altitude[9] - altitude[7],
        (0, 2): altitude[2] - altitude[0] + 50,
        (2, 5): altitude[5] - altitude[2] + 60,
        (5, 6): altitude[6] - altitude[5] + 80,
        (6, 8): altitude[8] - altitude[6] + 70,
        (8, 9): altitude[9] - altitude[8] + 90,
        (1, 4): altitude[4] - altitude[1] + 100,
        (4, 7): altitude[7] - altitude[4] + 110
    }

    return altitude, edges

def plot_graph_with_edges():
    """Plot graph with edges and weights"""
    altitude, edges = get_altitude_and_edges()
    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlim(-GRID_SIZE, GRID_SIZE)
    ax.set_ylim(-GRID_SIZE, GRID_SIZE)
    ax.set_title("Final Graph with Edges & Weights")

    ax.plot(*GRAPH_NODES[0], 'ro', label="Radar")
    ax.text(GRAPH_NODES[0][0] + 10, GRAPH_NODES[0][1] + 10, "0", color='red')
    ax.plot(GRAPH_NODES[9][0], GRAPH_NODES[9][1], marker='^',
            markersize=10, color='green', label="UAV detected")
    ax.text(GRAPH_NODES[9][0] + 10, GRAPH_NODES[9][1] + 10,
            "9", color='green', fontsize=10, fontweight='bold')

    for node, pos in GRAPH_NODES.items():
        if node != 0 and node != 9:
            ax.plot(*pos, 'kx')
            ax.text(pos[0] + 10, pos[1] + 10, str(node), fontsize=9, color='b')

    for (u, v), w in edges.items():
        x1, y1 = GRAPH_NODES[u]
        x2, y2 = GRAPH_NODES[v]
        ax.plot([x1, x2], [y1, y2], 'k--', alpha=0.6)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, str(w), 
                fontsize=10, color='red', ha='center')

    ax.legend()
    plt.close(fig)
    return fig

def run_dijkstra(graph, start, end):
    """Run Dijkstra's algorithm to find shortest path"""
    priority_queue = [(0, start)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    parent = {start: None}

    while priority_queue:
        cost, u = heapq.heappop(priority_queue)
        if u == end:
            break

        for w, v in graph.get(u, []):
            new_cost = cost + w
            if new_cost < distances.get(v, float('inf')):
                distances[v] = new_cost
                parent[v] = u
                heapq.heappush(priority_queue, (new_cost, v))

    path = []
    node = end
    while node is not None:
        path.append(node)
        node = parent.get(node)

    return path[::-1], distances

def plot_shortest_path(path):
    """Visualize the shortest path found by Dijkstra's algorithm"""
    altitude, edges = get_altitude_and_edges()
    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xlim(-GRID_SIZE, GRID_SIZE)
    ax.set_ylim(-GRID_SIZE, GRID_SIZE)
    ax.set_title("Dijkstra's Algorithm - Shortest Path")

    ax.plot(*GRAPH_NODES[0], 'ro', label="Radar")
    ax.text(GRAPH_NODES[0][0] + 10, GRAPH_NODES[0][1] + 10, "0", color='red')
    ax.plot(GRAPH_NODES[9][0], GRAPH_NODES[9][1], marker='^',
            markersize=10, color='green', label="UAV detected")
    ax.text(GRAPH_NODES[9][0] + 10, GRAPH_NODES[9][1] + 10,
            "9", color='green', fontsize=10, fontweight='bold')

    for node, pos in GRAPH_NODES.items():
        if node != 0 and node != 9:
            ax.plot(*pos, 'kx')
            ax.text(pos[0] + 10, pos[1] + 10, str(node), fontsize=9, color='b')

    for (u, v), w in edges.items():
        x1, y1 = GRAPH_NODES[u]
        x2, y2 = GRAPH_NODES[v]
        ax.plot([x1, x2], [y1, y2], 'k--', alpha=0.3)

    for i in range(len(path) - 1):
        u = path[i]
        v = path[i+1]
        x1, y1 = GRAPH_NODES[u]
        x2, y2 = GRAPH_NODES[v]
        ax.plot([x1, x2], [y1, y2], 'm-', linewidth=3, 
                label="Shortest Path" if i == 0 else "")

    total_weight = sum(edges.get((path[i], path[i+1]), 0) for i in range(len(path)-1))
    print("Total weight of shortest path:", total_weight)

    ax.legend()
    plt.close(fig)
    return fig

def run_full_dijkstra_demo():
    """Run complete Dijkstra's algorithm demonstration"""
    altitude, edges = get_altitude_and_edges()
    print("Final edges to be included in graph (u,v):weight:\n", edges)
    
    # Build graph structure
    graph = {}
    for (u, v), cost in edges.items():
        if u not in graph:
            graph[u] = []
        graph[u].append((cost, v))

    path, distances = run_dijkstra(graph, 0, 9)
    print("Path to reach UAV starting from radar:", path)
    return plot_shortest_path(path)