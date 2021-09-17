from io import BytesIO
import base64
import matplotlib.pyplot as plt


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image = buffer.getvalue()
    graph = base64.b64encode(image)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def plot_graph(x, y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 5))
    plt.title('power stats')
    plt.plot(x, y)
    plt.xticks(rotation=45)
    plt.xlabel('time')
    plt.ylabel('readings')
    plt.tight_layout()
    graph = get_graph()
    return graph