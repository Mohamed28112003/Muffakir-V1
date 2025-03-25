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
- أجب بـ "dummy_query" فقط إذا كان السؤال غير قانوني، غير أخلاقي، أو عامًا بعيدًا عن السياق القانوني

يجب أن تكون الإجابة واحدة من هذه الخيارات فقط دون أي شرح إضافي:
vector_db , dummy_query
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
٣. احذف أي كلمات أو أحرف غير عربية (مثل الإنجليزية أو غيرها) من الإجابة، مع الاحتفاظ بالروابط والمصادر الأجنبية كما هي دون تغيير.
٤. في حال وجود معلومات خاطئة أو تكرار، قم بتصحيحها أو حذفها.
٥. احتفظ بكافة الروابط والمصادر الموجودة في الإجابة دون تغيير، وتأكد من تنسيقها بشكل جيد.
٦. قدّم إجابة مُحسّنة، مختصرة وواضحة تركز على تقديم المعلومات الصحيحة مع الحفاظ على الروابط والمصادر.

الإجابة: {answer}

الإجابة المحسّنة:
""",

            "MCQ": """
أنت خبير في إنشاء الاختبارات التعليمية متخصص في صياغة أسئلة الاختيار من متعدد (MCQs).

## السياق

{context}

## التعليمات
استنادًا إلى السياق أعلاه، قم بإنشاء سؤال اختيار من متعدد عالي الجودة يتسم بما يلي:
1. يختبر فهم المفاهيم الرئيسية أو الحقائق أو العلاقات الموجودة في النص.
2. يحتوي على إجابة صحيحة واحدة فقط وثلاثة خيارات خاطئة محتملة.
3. يغطي المعلومات المهمة بدلاً من التفاصيل الثانوية.
4. يكون واضحًا، مختصرًا، وغير غامض.
5. يتضمن شرحًا موجزًا يوضح سبب صحة الإجابة الصحيحة.

## تنسيق الاستجابة
لكل سؤال، اتبع التنسيق التالي:

السؤال: [نص السؤال]

الخيارات:
أ. [نص الخيار]
ب. [نص الخيار]
ج. [نص الخيار]
د. [نص الخيار]

الإجابة الصحيحة: [حرف الخيار الصحيح]

الشرح: [شرح موجز يوضح سبب صحة الإجابة الصحيحة]

يجب أن تتضمن استجابتك الأسئلة الاختيارية المولدة فقط وفقًا للتنسيق المذكور أعلاه.
لا تُضف أي تعليقات أو شروحات إضافية خارج التنسيق المحدد.
""",

"history_classification_prompt": """
أنت مساعد مختص في تحليل الأسئلة وتحديد ما إذا كان السؤال الجديد يحتاج إلى استخدام سياق المحادثة السابقة أم أنه مستقل بذاته.

المعلومات:
سياق المحادثة السابقة:
{conversation_history}

السؤال الجديد:
{new_query}

المهمة:
قرر بين خيارين فقط:
1. إذا كان السؤال الجديد مستقلاً ولا يحتاج إلى السياق السابق - أجب بكلمة "original"
2. إذا كان السؤال يعتمد على السياق السابق لفهمه - أجب بكلمة "history"

القواعد:
- الإجابة يجب أن تكون كلمة واحدة فقط
- ممنوع إضافة أي شرح أو نص إضافي
- ممنوع إعادة صياغة السؤال
- ممنوع استخدام علامات الترقيم

""",

"search_query":"""

أعد صياغة السؤال التالي لتكون مركزة حصريًا على البيانات والمعلومات الخاصة بمصر مع الحفاظ على السياق الأصلي. يجب أن تكون الصياغة: 
- طبيعية وبلغة عربية سليمة
- محددة جغرافيا بكلمة "مصر" أو "المصرية"
- تحافظ على جوهر السؤال الأصلي
- بدون إضافة أي تفاصيل خارجية

السؤال الأصلي: {original_query}

(الإجابة يجب أن تحتوي على السؤال الجديد فقط بدون أي كلمات إضافية)

"""
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
