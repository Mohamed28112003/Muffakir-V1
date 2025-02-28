'use client';
import Link from "next/link";
import ThemeToggle from "../components/ThemeToggle";
import LanguageToggle from "../components/LanguageToggle";
import translations from "../translations/translations";
import { useEffect, useState } from "react";
import UserProfile from "../components/UserProfile";
import React from "react";

type Question = {
  id: number;
  text: string;
  options: string[];
  correctAnswer: string;
};

function TestPage() {
  const [lang, setLang] = useState<'en' | 'ar'>('en');
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [userAnswers, setUserAnswers] = useState<string[]>([]);
  const [score, setScore] = useState<number | null>(null);

  // Sample questions - replace with your actual questions
  const questions: Question[] = [
    {
      id: 1,
      text: translations[lang].question1,
      options: [
        translations[lang].option1a,
        translations[lang].option1b,
        translations[lang].option1c,
        translations[lang].option1d,
      ],
      correctAnswer: translations[lang].option1a,
    },
    {
      id: 2,
      text: translations[lang].question2, // new question text key
      options: [
        translations[lang].option2a,  // new option keys
        translations[lang].option2b,
        translations[lang].option2c,
        translations[lang].option2d,
      ],
      correctAnswer: translations[lang].option2a,
    },
    // you can add more questions as needed...
  ];

  useEffect(() => {
    const savedLang = localStorage.getItem('lang') === 'ar' ? 'ar' : 'en';
    setLang(savedLang);
    document.documentElement.setAttribute('lang', savedLang);
  }, []);

  const handleLanguageChange = () => {
    const newLang = lang === 'en' ? 'ar' : 'en';
    setLang(newLang);
    localStorage.setItem('lang', newLang);
    document.documentElement.setAttribute('lang', newLang);
  };

  const handleAnswerSelect = (answer: string) => {
    const newAnswers = [...userAnswers];
    newAnswers[currentQuestion] = answer;
    setUserAnswers(newAnswers);
  };

  const handleNextQuestion = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(prev => prev + 1);
    }
  };

  const handlePreviousQuestion = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(prev => prev - 1);
    }
  };

  const calculateScore = () => {
    const correct = questions.filter((q, index) => 
      userAnswers[index] === q.correctAnswer
    ).length;
    setScore(correct);
  };

  

  return (
    <main className='container'>
      <ThemeToggle />
      <LanguageToggle lang={lang} onToggle={handleLanguageChange} />
      <UserProfile guest={translations[lang].guest}/>

      <div className="test-container">
        <Link href="/" className="title-link">
          <h1 className="title">{translations[lang].testTitle}</h1>
        </Link>

        {score === null ? (
          <div className="question-container">
            <div className="progress">
              {translations[lang].question} {currentQuestion + 1} {translations[lang].of} {questions.length}
            </div>

            <div className="question-card">
              <h3>{questions[currentQuestion].text}</h3>
              <div className="options-container">
                {questions[currentQuestion].options.map((option, index) => (
                  <button
                    key={index}
                    className={`option-button ${
                      userAnswers[currentQuestion] === option ? 'selected' : ''
                    }`}
                    onClick={() => handleAnswerSelect(option)}
                  >
                    {option}
                  </button>
                ))}
              </div>
            </div>

            <div className="navigation-buttons">
              <button
                className="nav-button prev-button"
                onClick={handlePreviousQuestion}
                disabled={currentQuestion === 0}
              >
                {translations[lang].previous}
              </button>
              
              {currentQuestion < questions.length - 1 ? (
                <button
                  className="nav-button next-button"
                  onClick={handleNextQuestion}
                >
                  {translations[lang].next}
                </button>
              ) : (
                <button
                  className="nav-button submit-button"
                  onClick={calculateScore}
                >
                  {translations[lang].submit}
                </button>
              )}
            </div>
          </div>
        ) : (
          <div className="result-container">
            <h2>{translations[lang].yourScore} {score}/{questions.length}</h2>
            <button
              className="restart-button"
              onClick={() => {
                setCurrentQuestion(0);
                setUserAnswers([]);
                setScore(null);
              }}
            >
              {translations[lang].tryAgain}
            </button>
          </div>
        )}
      </div>
      </main>
  );
}

export default TestPage;