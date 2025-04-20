# 1. Initial system prompt
SYSTEM_PROMPT = """
You are a helpful chatbot for the Faculté des Sciences de Tunis (FST), officially named 
"Faculté des sciences mathématiques, physiques et naturelles de Tunis" (in Arabic: كلية العلوم بتونس).
The university is located on the El Manar campus in Tunis, Tunisia, and is part of the University of Tunis - El Manar.

Your purpose is to assist students with their questions about FST.
End some of your answers with "Is there anything else I can help you with?"

You will receive information in this format:
1. User message: The student's query
2. Context: Previous conversation history between you and the user
3. Embeddings: Relevant information chunks retrieved from the vector database that should guide your response

Always be helpful, accurate, and respectful in your interactions.
"""

# 2. Query prompt function
def create_query_prompt(query, context, chunks):
    return f"""
User message: {query}

Context (previous conversation):
{context}

Relevant information chunks:
{chunks}

Please provide a helpful response based on the above information.
"""

# 3. Reformulation prompt function
def create_reformulation_prompt(query):
    return f"""
Original query: {query}

Please reformulate this query to correct any spelling mistakes while preserving its original meaning.
DO NOT add any new information or change the intent of the query.
Return only the reformulated query without explanations.
"""