import time
from loguru import logger
import networkx as nx
import matplotlib.pyplot as plt


def build_graph(data: list[dict], max_depth: int | None = 4):
    G = nx.Graph()

    # Функция для добавления узлов и связей
    for entry in data:
        user_id = entry["id"]
        friend_ids = entry["friend_ids"]
        depth = entry["depth"]

        logger.info(f"adding {user_id=} with {len(friend_ids)=}")

        if depth <= max_depth:
            for friend_id in friend_ids:
                G.add_edge(user_id, friend_id)

    # Добавление перекрестных связей на глубине 2
    for entry in data:
        user_id = entry["id"]
        friend_ids = entry["friend_ids"]
        depth = entry["depth"]

        # Ищем перекрестные связи только для друзей с глубиной 2
        if depth == 2:
            for friend_id in friend_ids:
                # Проверяем, что friend_id есть в графе и его глубина равна 2
                if friend_id in [e["id"] for e in data]:
                    for mutual_friend_id in friend_ids:
                        # Проверяем общих друзей и добавляем перекрестные связи
                        if (
                            mutual_friend_id != friend_id
                            and mutual_friend_id in G[friend_id]
                        ):
                            G.add_edge(friend_id, mutual_friend_id)

    plt.figure(figsize=(100, 100))
    nx.draw(
        G,
        with_labels=True,
        node_size=50,
        node_color="lightblue",
        font_size=8,
        # font_weight="bold",
    )
    plt.savefig(f"graph_{int(time.time())}.png", format="png")
    plt.close()