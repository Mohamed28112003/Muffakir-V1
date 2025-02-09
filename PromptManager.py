class PromptManager:
    """
    A centralized manager for all prompt templates used in the pipeline.
    """
    def __init__(self):

        self.prompts = {

"query_classification_prompt":
            '''
السؤال: {query_transformed}

حدد الفئة المناسبة وفقًا للقواعد:
- أجب بـ "vector_db" فقط إذا كان السؤال عن قوانين أو تشريعات موجودة في قاعدة البيانات القانونية
- أجب بـ "web_search" فقط إذا تطلب السؤال معلومات حديثة أو غير قانونية
- أجب بـ "dummy_query" فقط إذا كان السؤال غير قانوني، غير أخلاقي، أو عامًا بعيدًا عن السياق القانوني

يجب أن تكون الإجابة واحدة من هذه الخيارات فقط دون أي شرح إضافي:
vector_db، web_search، dummy_query
''',

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
                "استخدم السياق التالي للإجابة على السؤال باللغة العربية فقط،",
                "[السياق]: {context}",
                "[السؤال]: {question}",
                "[التعليمات]:",
                "١. الإجابة يجب أن تكون باللغة العربية فقط",
                "٢. استخدام المعلومات من السياق المقدم حصريًا",
                "٣. إذا كان السؤال غير مرتبط بالسياق، اذكر إجابة مناسبة",
                "٤. إذا لم توجد معلومات للإجابة على السؤال، اكتب: لا يمكنني الإجابة على هذا السؤال",
                "[الإجابة]:",
            ]),

            "hallucination_check_prompt": """
انت مساعد ذكي متخصص في تقييم صحة الإجابات.
**التعليمات:**
١. افحص الإجابة المُقدمة للتأكد من خلوها من المعلومات المختلقة (hallucinations).
٢. تأكد من أن الإجابة لا تحتوي على معلومات غير ضرورية أو مكررة.
٣. في حال وجود معلومات خاطئة أو تكرار، قم بتصحيحها أو حذفها.
٤. احتفظ بكافة الروابط والمصادر الموجودة في الإجابة دون تغيير، وتأكد من تنسيقها بشكل جيد.
٥. قدّم إجابة مُحسّنة، مختصرة وواضحة تركز على تقديم المعلومات الصحيحة مع الحفاظ على الروابط والمصادر.
الإجابة: {answer}

الإجابة المحسّنة:
""",
        }

    def get_prompt(self, key: str) -> str:
        if key not in self.prompts:
            raise ValueError(f"Prompt '{key}' not found in PromptManager.")
        return self.prompts[key]

    def add_prompt(self, key: str, prompt_template: str):
        self.prompts[key] = prompt_template

# Example usage:
# prompt_manager = PromptManager()
# print(prompt_manager.get_prompt("hallucination_check_prompt"))
