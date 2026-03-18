from agent.agent import run_agent

while True:
    query = input("\nAsk: ")

    if query.lower() == "exit":
        break

    response = run_agent(query)

    print("\n💡 Answer:\n")
    print(response)