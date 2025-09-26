from graph.compile_graph import app as graph_app
import os


def run(inputs:dict) -> dict:

    final_value = {}
    for output in graph_app.stream(inputs):
        for key, value in output.items():
            final_value = value
    return final_value