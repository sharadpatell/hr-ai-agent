from agent.retriever import retrieve
from agent.llm import (
    decide_with_context,
    generate_answer,
    general_answer,
    solve_math
)


def run_agent(query, chat_history):

    print("\n========================")
    print(f"🟡 USER QUERY: {query}")
    print("========================")

    # 🔥 STEP 1: RETRIEVE
    context_list = retrieve(query)

    context = "\n\n".join(context_list)

    # 🔥 STEP 2: DECISION
    decision = decide_with_context(query, context)

    print(f"\n🧠 Decision: {decision}")

    # 🔥 STEP 3: ROUTING
    if "use_context" in decision:

        if not context.strip():
            print("⚠️ No context found")
            return "Not found in knowledge base"

        return generate_answer(query, context)

    elif "calculator" in decision:
        return solve_math(query)

    else:
        return general_answer(query)