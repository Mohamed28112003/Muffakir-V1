from typing import Tuple, List, Dict, Optional, Any
from LLMProvider import *
from PromptManager import *
from QueryDocumentProcessor import *
import re
from DocumentRetriever import *


class QuizGeneration:

    def __init__(self, llm_provider: LLMProvider, prompt_manager: PromptManager,
                 retriever: DocumentRetriever):

        self.llm_provider = llm_provider
        self.retriever = retriever
        self.prompt_manager = prompt_manager
        self.generation_prompt = self.prompt_manager.get_prompt("MCQ")

    def generate_quiz(self, query: str) -> Dict[str, Any]:
        """
        Generate MCQ quiz questions based on retrieved documents from a query.

        Args:
            query: The search query to retrieve relevant documents

        Returns:
            A dictionary containing lists of questions, options, correct answers, and explanations
        """
        # Retrieve documents
        retrieval_result = self.retriever.retrieve_documents(query, 10)
        formatted_documents = self.retriever.format_documents(retrieval_result)

        print("LENGHT : ",len(formatted_documents))
        print("lenght 2 : ",len(retrieval_result))

        # Initialize lists to store parsed quiz elements
        all_questions = []
        all_options = []
        all_correct_answers = []
        all_explanations = []

        # Process each document
        for doc in formatted_documents:
            try:
                # Format prompt with document content
                prompt = self.generation_prompt.format(
                    context=doc.page_content,
                )

                # Generate Q&A using LLM
                llm = self.llm_provider.get_llm()
                response = llm.invoke(prompt)

                # Extract response content
                content = response.content if hasattr(response, 'content') else str(response)

                # Parse the response to extract structured data
                questions, options, correct_answers, explanations = self.parse_mcq_response(content)

                # Add parsed data to the result lists
                all_questions.extend(questions)
                all_options.extend(options)
                all_correct_answers.extend(correct_answers)
                all_explanations.extend(explanations)

            except Exception as e:
                print(f"Error generating quiz for document: {e}")
                self.llm_provider.switch_api_key()
                # Continue with the next document instead of recursion

        # Return structured results
        return {
            "questions": all_questions,
            "options": all_options,
            "correct_answers": all_correct_answers,
            "explanations": all_explanations
        }

    def parse_mcq_response(self, response_text: str) -> Tuple[List[str], List[List[str]], List[str], List[str]]:
        """
        Parse the LLM response to extract questions, options, correct answers, and explanations
        using the new Arabic prompt format.

        Args:
            response_text: Raw text response from the LLM

        Returns:
            Tuple containing lists of questions, options (as lists), correct answers, and explanations
        """
        # Initialize lists to store parsed elements
        questions = []
        options_list = []
        correct_answers = []
        explanations = []

        # Split response into sections based on the new prompt format; each question starts with "السؤال:"
        question_sections = re.split(r'(?=السؤال:)', response_text)

        for section in question_sections:
            if not section.strip():
                continue

            try:
                # Extract question (captures text until the next key "الخيارات:" is encountered)
                question_match = re.search(r'(?:السؤال|Question):\s*(.+?)(?=\n(?:الخيارات|Options):)', section, re.DOTALL)
                if question_match:
                    question = question_match.group(1).strip()
                    questions.append(question)
                else:
                    continue  # Skip if no question found

                # Extract options block (captures text until the next key "الإجابة الصحيحة:" is encountered)
                options_text = re.search(r'(?:الخيارات|Options):\s*(.+?)(?=\n(?:الإجابة الصحيحة|Correct Answer):)', section, re.DOTALL)
                if options_text:
                    options_block = options_text.group(1).strip()
                    # Parse individual options (matching A, B, C, D or أ, ب, ج, د)
                    option_matches = re.findall(r'(?:[A-Dأ-د])\.\s*(.+?)(?=\n[A-Dأ-د]\.|$)', options_block, re.DOTALL)
                    options_list.append([opt.strip() for opt in option_matches])
                else:
                    options_list.append([])  # Empty list if no options found

                # Extract correct answer
                answer_match = re.search(r'(?:الإجابة الصحيحة|Correct Answer):\s*([A-Dأ-د])', section)
                if answer_match:
                    correct_answers.append(answer_match.group(1).strip())
                else:
                    correct_answers.append("")  # Empty string if no answer found

                # Extract explanation using "الشرح:" (captures text until the end of the section)
                explanation_match = re.search(r'(?:الشرح|Explanation):\s*(.+?)(?=\n|$)', section, re.DOTALL)
                if explanation_match:
                    explanations.append(explanation_match.group(1).strip())
                else:
                    explanations.append("")  # Empty string if no explanation found

            except Exception as e:
                print(f"Error parsing question section: {e}")
                # Continue with the next section

        return questions, options_list, correct_answers, explanations