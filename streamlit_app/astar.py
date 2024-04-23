

import networkx as nx
import osmnx as ox
from heapq import heappush, heappop
from geopy.distance import great_circle
import requests
import json
import nest_asyncio
import asyncio
import aiohttp


async def fetch_traffic_data(session, url, node_id, traffic_data_dict):
    async with session.get(url) as response:
        if response.status == 200:
            traffic_data = await response.json()
            current_speed = traffic_data['flowSegmentData']['currentSpeed']
            current_travel_time = traffic_data['flowSegmentData']['freeFlowSpeed']
            free_flow_speed = traffic_data['flowSegmentData']['currentSpeed']
            free_flow_travel_time = traffic_data['flowSegmentData']['freeFlowTravelTime']
            roadClosure = traffic_data['flowSegmentData']['roadClosure']
            traffic_data_dict[node_id] = {
                'current_speed': current_speed,
                'current_travel_time': current_travel_time,
                'free_flow_speed': free_flow_speed,
                'free_flow_travel_time': free_flow_travel_time,
                'road_closure': roadClosure
            }
        else:
            pass


async def get_traffic_data(G, api_key='BVENUoESZDzQlUXqnDMN7mdZcoAtSdA7'):
    traffic_data_dict = {}
    async with aiohttp.ClientSession() as session:
        tasks = []
        for node_id, node_data in G.nodes(data=True):
            lat, lon = node_data['y'], node_data['x']
            url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json?point={
                lat}%2C{lon}&key={api_key}"
            task = asyncio.ensure_future(fetch_traffic_data(
                session, url, node_id, traffic_data_dict))
            tasks.append(task)
        await asyncio.gather(*tasks)
    return traffic_data_dict

# To run the async function in Jupyter, use:
nest_asyncio.apply()


def heuristic(node1, node2, G):
    """
    Compute the heuristic, i.e., the straight-line distance between two nodes.
    """
    lat1, lon1 = G.nodes[node1]['y'], G.nodes[node1]['x']
    lat2, lon2 = G.nodes[node2]['y'], G.nodes[node2]['x']
    return great_circle((lat1, lon1), (lat2, lon2)).meters


def adjust_edge_weights_with_traffic(G, traffic_data):
    """
    Adjust the edge weights in the graph based on traffic data, considering rush hours and road closures.
    """
    print("Adjusting edge weights based on traffic data...")
    for u, v, data in G.edges(data=True):
        u_data = traffic_data.get(u, {})
        v_data = traffic_data.get(v, {})
        if u_data.get('road_closure', False) or v_data.get('road_closure', False):
            data['weight'] = float('inf')
            continue

        # Default to 1 to avoid division by zero
        u_speed = u_data.get('current_speed', 1)
        v_speed = v_data.get('current_speed', 1)
        avg_speed = (u_speed + v_speed) / 2

        rush_hour_factor = 1.5 if any([
            u_data.get('current_travel_time', 0) > u_data.get(
                'free_flow_travel_time', 0) * 1.2,
            v_data.get('current_travel_time', 0) > v_data.get(
                'free_flow_travel_time', 0) * 1.2
        ]) else 1

        original_weight = data.get('weight', 1)
        adjusted_weight = ((original_weight / avg_speed)
                           * 60) * rush_hour_factor
        data['weight'] = adjusted_weight


def a_star_search_with_traffic(G, start, goal, weight='length'):
    """
    Perform A* search on a graph, considering traffic data.
    """
    
    traffic_data = asyncio.run(get_traffic_data(G))
    adjust_edge_weights_with_traffic(G, traffic_data)
    open_set = []
    heappush(open_set, (0, start))
    came_from = {}
    g_score = {node: float('inf') for node in G.nodes}
    g_score[start] = 0
    f_score = {node: float('inf') for node in G.nodes}
    f_score[start] = heuristic(start, goal, G)

    while open_set:
        current = heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for neighbor in G.neighbors(current):
            tentative_g_score = g_score[current] + \
                G[current][neighbor][0].get(weight, 1)

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + \
                    heuristic(neighbor, goal, G)

                if neighbor not in [i[1] for i in open_set]:
                    heappush(open_set, (f_score[neighbor], neighbor))

    return None 
