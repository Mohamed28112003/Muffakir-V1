
import re
import pandas as pd
import numpy as np
from tqdm import tqdm
from pathlib import Path
from typing import List, Dict
from LLMProvider.LLMProvider import LLMProvider
from VectorDB.ChromaDBManager import ChromaDBManager
from PromptManager.PromptManager import PromptManager
from sklearn.metrics.pairwise import cosine_similarity

class EvaluationDataHandler:
    def __init__(self, rag_manager, db_manager, eval_data_path="./evaluation_data/legal_qa.csv"):
        self.rag_manager = rag_manager
        self.llm_provider = rag_manager.llm_provider
        self.embedding_provider = db_manager.embedding_provider
        self.prompt_manager = PromptManager()
        self.eval_data_path = eval_data_path
        self.selected_questions = None
        self.sample_seed = 42  # Fixed seed for reproducibility

    def _clean_text(self, text: str) -> str:
        """Clean Arabic text"""
        return re.sub(r'[^\u0600-\u06FF0-9\s.,؟!]', '', str(text)).strip()

    def _stratified_sample(self, sample_size=200):
        """Get stratified sample of questions"""
        full_df = pd.read_csv(self.eval_data_path, usecols=['question', 'context'])
        full_df = full_df.dropna()
        
        # Create context length bins
        full_df['context_length'] = full_df['context'].apply(len)
        full_df['length_bin'] = pd.qcut(full_df['context_length'], q=4, labels=False)
        
        # Stratified sampling
        sample = full_df.groupby('length_bin', group_keys=False)\
            .apply(lambda x: x.sample(n=int(sample_size/4), random_state=self.sample_seed))
        
        # Clean and return
        sample['question'] = sample['question'].apply(self._clean_text)
        sample['context'] = sample['context'].apply(self._clean_text)
        return sample.drop(columns=['context_length', 'length_bin'])

    def evaluate_model(self, model_name: str, output_dir="evaluation_results"):
        """Run full evaluation for a model"""
        # Initialize output
        Path(output_dir).mkdir(exist_ok=True)
        output_path = Path(output_dir) / f"eval_{model_name.replace('/', '-')}.csv"
        
        # Get sample questions
        if not self.selected_questions:
            self.selected_questions = self._stratified_sample()
            
        results = []
        
        # Process questions
        for _, row in tqdm(self.selected_questions.iterrows(), total=200, desc=f"Evaluating {model_name}"):
            try:
                question = row['question']
                context = row['context']
                
                # Generate answer
                response = self.rag_manager.generate_answer(question)
                answer = response.get("answer", "")
                
                # Calculate metrics
                faithfulness = self._calculate_faithfulness(answer, context)
                relevancy = self._calculate_relevancy(question, answer)
                
                results.append({
                    'question': question,
                    'context': context,
                    'generated_answer': answer,
                    'faithfulness_score': faithfulness,
                    'answer_relevancy_score': relevancy
                })
                
            except Exception as e:
                print(f"Error processing question: {str(e)}")
                continue

        # Save results
        results_df = pd.DataFrame(results)
        results_df.to_csv(output_path, index=False)
        
        # Add averages
        with open(output_path, 'a') as f:
            f.write(f"\n\nAvg_Faithfulness,{results_df['faithfulness_score'].mean():.4f}")
            f.write(f"\nAvg_Answer_Relevancy,{results_df['answer_relevancy_score'].mean():.4f}")
            
        return output_path

    def _calculate_faithfulness(self, answer: str, context: str) -> float:
        """Calculate faithfulness score"""
        claims = self._extract_claims(answer)
        if not claims: return 0.0
        
        verified = []
        for claim in claims:
            prompt = self.prompt_manager.get_prompt("faithfulness_verification").format(
                claim=claim, context=context[:3000]
            )
            try:
                response = self.llm_provider.get_llm().invoke(prompt)
                verified.append(1 if "نعم" in response.content else 0)
            except:
                verified.append(0)
        return np.mean(verified)

    def _calculate_relevancy(self, question: str, answer: str) -> float:
        """Calculate answer relevancy score"""
        generated_questions = self._generate_questions(answer)
        if not generated_questions: return 0.0
        
        question_embed = self.embedding_provider.embed_query(question)
        answer_embeds = self.embedding_provider.embed_documents(generated_questions)
        return cosine_similarity([question_embed], answer_embeds)[0].mean()

    def _generate_questions(self, answer: str) -> List[str]:
        """Generate questions from answer"""
        prompt = f"Generate 3 Arabic questions based on this answer:\n{answer}"
        try:
            response = self.llm_provider.get_llm().invoke(prompt)
            return [q.split('. ')[1] for q in response.content.split('\n') if q.startswith(('1', '2', '3'))]
        except:
            return []

    def _extract_claims(self, answer: str) -> List[str]:
        """Extract claims from answer"""
        prompt = self.prompt_manager.get_prompt("faithfulness_extraction").format(answer=answer)
        response = self.llm_provider.get_llm().invoke(prompt)
        return [c.split('. ')[1] for c in response.content.split('\n') if c.startswith(('1', '2', '3'))]