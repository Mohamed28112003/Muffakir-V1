from typing import Tuple, List, Dict, Any
from LLMProvider.LLMProvider import *
from PromptManager.PromptManager import *
from QueryClassification.QueryDocumentProcessor import *
import re
from Generation.DocumentRetriever import *


class QuizGeneration:
    def __init__(self, llm_provider: LLMProvider, prompt_manager: PromptManager, retriever: DocumentRetriever):
        self.llm_provider = llm_provider
        self.retriever = retriever
        self.prompt_manager = prompt_manager
        self.generation_prompt = self.prompt_manager.get_prompt("MCQ")

    def clean_text(self, text: str) -> str:

        ## ADD ANY 
        return re.sub(r'[^\u0600-\u06FF\s]', '', text)

    def generate_quiz(self, query: str) -> Dict[str, Any]:
        retrieval_result = self.retriever.retrieve_documents(query, 10)
        formatted_documents = self.retriever.format_documents(retrieval_result)
        all_questions = []
        all_options = []
        all_correct_answers = []
        all_explanations = []
        for doc in formatted_documents:
            try:
                prompt = self.generation_prompt.format(context=doc.page_content)
                llm = self.llm_provider.get_llm()
                response = llm.invoke(prompt)
                content = response.content if hasattr(response, 'content') else str(response)
                questions, options, correct_answers, explanations = self.parse_mcq_response(content)
                all_questions.extend(questions)
                all_options.extend(options)
                all_correct_answers.extend(correct_answers)
                all_explanations.extend(explanations)


            except Exception as e:
                print(f"Error generating quiz for document: {e}")
                self.llm_provider.switch_api_key()


        cleaned_questions = [self.clean_text(q) for q in all_questions]
        cleaned_options = [[self.clean_text(opt) for opt in option_group] for option_group in all_options]
        cleaned_correct_answers = [self.clean_text(ans) for ans in all_correct_answers]
        cleaned_explanations = [self.clean_text(exp) for exp in all_explanations]

        return {
            "questions": cleaned_questions,
            "options": cleaned_options,
            "correct_answers": cleaned_correct_answers,
            "explanations": cleaned_explanations
        }

    def parse_mcq_response(self, response_text: str) -> Tuple[List[str], List[List[str]], List[str], List[str]]:
        questions = []
        options_list = []
        correct_answers = []
        explanations = []
        question_sections = re.split(r'(?=السؤال:)', response_text)
        for section in question_sections:
            if not section.strip():
                continue
            try:
                question_match = re.search(r'(?:السؤال|Question):\s*(.+?)(?=\n(?:الخيارات|Options):)', section, re.DOTALL)
                if question_match:
                    question = question_match.group(1).strip()
                    questions.append(question)
                else:
                    continue
                options_text = re.search(r'(?:الخيارات|Options):\s*(.+?)(?=\n(?:الإجابة الصحيحة|Correct Answer):)', section, re.DOTALL)
                if options_text:
                    options_block = options_text.group(1).strip()
                    option_matches = re.findall(r'(?:[A-Dأ-د])\.\s*(.+?)(?=\n[A-Dأ-د]\.|$)', options_block, re.DOTALL)
                    options_list.append([opt.strip() for opt in option_matches])
                else:
                    options_list.append([])
                answer_match = re.search(r'(?:الإجابة الصحيحة|Correct Answer):\s*([A-Dأ-د])', section)
                if answer_match:
                    correct_answers.append(answer_match.group(1).strip())
                else:
                    correct_answers.append("")
                explanation_match = re.search(r'(?:الشرح|Explanation):\s*(.+?)(?=\n|$)', section, re.DOTALL)
                if explanation_match:
                    explanations.append(explanation_match.group(1).strip())
                else:
                    explanations.append("")
            except Exception as e:
                print(f"Error parsing question section: {e}")
        return questions, options_list, correct_answers, explanations
