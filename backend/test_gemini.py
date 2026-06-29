from backend.services.llm.gemini_client import GeminiClient

client = GeminiClient()

response = client.generate_json(

    system_prompt="""
You are a JSON API.

Return ONLY JSON.
""",

    user_prompt="""
Return

{
"name":"Praneeth",
"role":"Developer"
}
"""

)

print(response)