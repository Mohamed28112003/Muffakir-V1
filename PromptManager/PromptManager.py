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
قم بتحليل السؤال الجديد وحدد تصنيفه الصحيح.

قواعد الإخراج:
1. يجب أن تقدم إجابتك في الهيكل XML المحدد أدناه
2. اختر تصنيفًا واحدًا فقط: إما "original" (للأسئلة المستقلة) أو "history" (للأسئلة المعتمدة على السياق)
3. لا تضف أي نص أو تفسير أو علامات ترقيم خارج بنية XML

<output>
<classification>CLASSIFICATION</classification>
</output>

حيث:
- "original": يعني أن السؤال مستقل ولا يحتاج إلى السياق السابق لفهمه
- "history": يعني أن السؤال يعتمد على السياق السابق لفهمه
""",

"search_query":"""

أعد صياغة السؤال التالي لتكون مركزة حصريًا على البيانات والمعلومات الخاصة بمصر مع الحفاظ على السياق الأصلي. يجب أن تكون الصياغة: 
- طبيعية وبلغة عربية سليمة
- محددة جغرافيا بكلمة "مصر" أو "المصرية"
- تحافظ على جوهر السؤال الأصلي
- بدون إضافة أي تفاصيل خارجية

السؤال الأصلي: {original_query}

(الإجابة يجب أن تحتوي على السؤال الجديد فقط بدون أي كلمات إضافية)

""",

            "faithfulness_extraction": """
            استخرج الادعاءات الفردية من الإجابة التالية. رقم كل ادعاء في سطر منفصل:
            {answer}
            المطلوب: ١. تحديد كل حقيقة أو ادعاء منفصل ٢. الترقيم التسلسلي ٣. عدم إضافة تفسيرات
            قائمة الادعاءات:
            """,
             "faithfulness_verification": """
    هل الادعاء التالي مدعوم مباشرة بالسياق المرفق؟
    الادعاء: {claim}
    السياق: {context}
    
    أجب بكلمة واحدة فقط (نعم/لا):
    """,


"youtube": """ 

أنت مساعد ذكي مختص في تحسين استعلامات البحث عن محتوى تعليمي للطلاب على يوتيوب.

مهمتك هي تحويل الجملة أو الكلمة المفتاحية التي يقدمها المستخدم إلى استعلام بحث مُحسَّن وواضح، بحيث يركّز على طلب "فيديوهات شرح" لهذا الموضوع على يوتيوب، مع تخصيص النتائج لتكون مرتبطة بالمحتوى المصري إن أمكن.

التعليمات:
- استخدم لغة عربية رسمية ومفهومة.
- أضف كلمات مثل: "فيديوهات شرح"، و"في اليوتيوب"، وركز أن تكون النتائج لمصر إذا كان ذلك مناسبًا.
- حدد المجال بدقة إن أمكن (مثلاً: القانون الجنائي المصري).

مثال:
- إدخال المستخدم: القانون الجنائي
- استعلام محسن: فيديوهات شرح القانون الجنائي المصري في اليوتيوب

السؤال:
{original_query}

ابدأ فقط بجملة الاستعلام المحسنة بدون مقدمات إضافية.




""",

"mindmap":"""



حول النص التالي إلى JSON يمثل خريطة ذهنية.
تأكد أن كل فكرة رئيسية تصبح فرعًا رئيسيًا، والأفكار الفرعية تصبح أطفالًا له.
النص:
---
{context}
---
أعد فقط الـ JSON بدون أي شرح إضافي.


""",

"history_query_prompt":"""



أنت مساعد ذكي متخصص في فهم سياق المحادثات والإجابة على الأسئلة بناءً على السياق السابق.

في الاستفسار السابق، سأل المستخدم:
"{last_query}"

وكانت إجابتك:
"{last_response}"

الآن المستخدم يسأل سؤالًا جديدًا يعتمد على السياق السابق:
"{new_query}"

الرجاء الإجابة على السؤال الجديد مع الأخذ بعين الاعتبار السياق السابق. قدم إجابة كاملة ودقيقة تلبي احتياجات المستخدم.
""",


# Add these prompts to your existing PromptManager

# In the PromptManager.__init__ method, add these to self.prompts dictionary:

"summary_map": """
أنت خبير في تلخيص النصوص العربية. الرجاء تلخيص النص التالي بشكل واضح وموجز:

{text}

ملخص:
""",

"summary_combine": """
أنت خبير في دمج الملخصات باللغة العربية. فيما يلي مجموعة من الملخصات لأقسام مختلفة من نفس الوثيقة:

{text}

الرجاء دمج هذه الملخصات في ملخص واحد شامل ومترابط للوثيقة بأكملها. قم بتنظيم الملخص النهائي في فقرات مناسبة، مع التركيز على النقاط الرئيسية.

الملخص النهائي:
""",

"summary_direct": """
أنت خبير في تلخيص النصوص العربية. الرجاء تلخيص النص التالي بشكل واضح وموجز، مع التركيز على الأفكار والنقاط الرئيسية:

{text}

ملخص شامل:
""",

"summary_check": """
أنت خبير في تقييم جودة ملخصات النصوص. قم بتقييم الملخص التالي من حيث:
1. الشمولية (هل يغطي النقاط الرئيسية)
2. الإيجاز (هل هو مختصر بشكل مناسب)
3. الدقة (هل المعلومات الواردة فيه دقيقة)

النص الأصلي:
{original_text}

الملخص:
{summary}

تقييمك (قم بتقييم كل عنصر على مقياس من 1-5، ثم قدم تعليقًا موجزًا):
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
