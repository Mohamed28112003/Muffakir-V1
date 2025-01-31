class PromptManager:
    """
    A centralized manager for all prompt templates used in the pipeline.
    """
    def __init__(self):

        self.prompts = {
            "query_rewrite": """
            You are an AI assistant specialized in enhancing user queries for retrieval-augmented generation (RAG) systems.
            Your task is to take the original, potentially vague or broad user query and reformulate it into a more specific,
            detailed, and contextually rich version that is likely to yield relevant and accurate results.

            **Instructions:**
            1. Analyze the original query for key concepts, intent, and context.
            2. Identify any ambiguous terms or phrases and replace them with more precise language.
            3. Expand on the query by adding relevant details that could guide the retrieval system to better understand the user's needs.
            4. Ensure the reformulated query maintains the original intent while enhancing specificity and clarity.
            5. Your answer should be in Arabic only.

            Original query: {original_query}

            Rewritten query:
            """,
            "summary_generation": """
            INSTRUCTIONS
            You are an expert at summarizing Arabic text.
            Create a concise but comprehensive summary that captures the main points.
            Focus on key concepts and important details.
            The summary should be in Arabic and self-contained.
            Text: {text}

            Summary:
            """,
            "question_generation": """
            You are a model that generates questions based on text content.
            Given the text below, generate a relevant question in Arabic.

            Text: {text}

            Question:
            """,
            "generation": "\n".join([
    "استخدم السياق التالي للإجابة على السؤال باللغة العربية  فقط، ",
    "[السياق]:{context}",

    "[السؤال]:{question}",

    "[التعليمات]:",
    "١. الإجابة يجب أن تكون باللغة العربية فقط",
 "   ٢. استخدام المعلومات من السياق المقدم حصريًا",
"    ٣. إذا كان السؤال غير مرتبط بالسياق، اذكر  إجابة",
"اذا لا يوجد اجابه في السياق اكتب لا يممكني الاجابه علي هذا السؤال فقط ",
    "[الإجابة]:",
    
            ]),
        }

    def get_prompt(self, key: str) -> str:

        if key not in self.prompts:
            raise ValueError(f"Prompt '{key}' not found in PromptManager.")
        return self.prompts[key]

    def add_prompt(self, key: str, prompt_template: str):

        self.prompts[key] = prompt_template




# prompt_manager = PromptManager()

# prompt_manager.add_prompt("custom_task", """
# ADD YOUR CUSTOM PROMPT HERE
# """)