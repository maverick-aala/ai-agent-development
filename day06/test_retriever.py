"""Day 06 — Demo script for retrieve_based_on_embedding."""

from retriever import retrieve_based_on_embedding

retrieved_dict = retrieve_based_on_embedding("amazon")
print(retrieved_dict["filename"])
print()
print(retrieved_dict["content"])
