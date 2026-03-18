from agent.retriever import retrieve
from agent.llm import generate_answer

while True:
    query = input("\nAsk: ")

    if query.lower() == "exit":
        break

    context = retrieve(query)

    answer = generate_answer(query, context)

    print("\n💡 Answer:\n")
    print(answer)