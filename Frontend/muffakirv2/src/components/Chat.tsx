'use client';

import ThemeToggle from "./ThemeToggle";
import ButtonHandler from "./ButtonHandler";
import LanguageToggle from "./LanguageToggle";
import translations from "../translations/translations";
import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import UserProfile from "./UserProfile";
import { PiStudentBold } from "react-icons/pi";
import React from "react";

type Message = {
  id: number;
  text: string;
  isUser: boolean;
  timestamp: Date;
  isTyping: boolean;
};

function ChatPage() {
  const [lang, setLang] = useState<'en' | 'ar'>('en');
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [isSending, setIsSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const typingIntervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    const savedLang = localStorage.getItem('lang') === 'ar' ? 'ar' : 'en';
    setLang(savedLang);
    document.documentElement.setAttribute('lang', savedLang);
  }, []);

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth", block: "end" });
    }
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const text = inputText.trim();
    if (!text) return;

    // Disable send button immediately
    setIsSending(true);

    const userMessage: Message = {
      id: Date.now(),
      text: text,
      isUser: true,
      timestamp: new Date(),
      isTyping: false,
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');

    // Delay before starting the AI response simulation
    setTimeout(() => {
      const fullText = `${text} (this is a dummy response)`;

      const aiResponse: Message = {
        id: Date.now(),
        text: '', // Start with empty text
        isUser: false,
        timestamp: new Date(),
        isTyping: true,
      };

      setMessages(prev => [...prev, aiResponse]);

      const baseSpeed = 150; // Base speed in milliseconds per character
      const speedFactor = Math.max(1, Math.log(fullText.length));
      const typingSpeed = baseSpeed / speedFactor;
      let index = 0;

      typingIntervalRef.current = setInterval(() => {
        setMessages(prev => {
          const lastMessage = prev[prev.length - 1];
          if (lastMessage.isTyping && index < fullText.length) {
            const updatedMessages = [...prev];
            updatedMessages[updatedMessages.length - 1] = {
              ...lastMessage,
              text: fullText.substring(0, index + 1),
            };
            index++;
            return updatedMessages;
          }
          if (index >= fullText.length) {
            if (typingIntervalRef.current) {
              clearInterval(typingIntervalRef.current);
              typingIntervalRef.current = null;
            }
            setIsSending(false);
            return prev.map(msg =>
              msg.id === lastMessage.id ? { ...msg, isTyping: false } : msg
            );
          }
          return prev;
        });
      }, typingSpeed);
    }, 1000);
  };

  // Cancel the AI response typing without deleting the message
  const handleCancelSending = () => {
    if (typingIntervalRef.current) {
      clearInterval(typingIntervalRef.current);
      typingIntervalRef.current = null;
    }
    setMessages(prev => {
      const lastMessage = prev[prev.length - 1];
      if (lastMessage && lastMessage.isTyping) {
        return prev.map(msg =>
          msg.id === lastMessage.id ? { ...msg, isTyping: false } : msg
        );
      }
      return prev;
    });
    setIsSending(false);
  };

  const handleLanguageChange = () => {
    const newLang = lang === 'en' ? 'ar' : 'en';
    setLang(newLang);
    localStorage.setItem('lang', newLang);
    document.documentElement.setAttribute('lang', newLang);
  };

  return (
    <main className="container">
      <ThemeToggle />
      <LanguageToggle lang={lang} onToggle={handleLanguageChange} />
      <UserProfile guest={translations[lang].guest} />

      <div className="chat-container">
        <Link href="/" className="title-link">
          <h1 className="title">{translations[lang].welcome}</h1>
        </Link>
        <div className="chat-messages">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.isUser ? 'user-message' : 'assistant-message'}`}
            >
              {!message.isUser && (
                <div className="bot-icon-container">
                  <PiStudentBold size={32} />
                </div>
              )}
              <div className="message-content">
                {message.text}
                {message.isTyping && (
                  <span className="typing-indicator">
                    <span>.</span>
                    <span>.</span>
                    <span>.</span>
                  </span>
                )}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>
        <div className="chat-input-container">
          <form className="chat-form" onSubmit={handleSubmit}>
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  handleSubmit(e);
                }
              }}
              placeholder={translations[lang].typeMessage}
              className="chat-input"
            />
            {/* Pass the isSending state and cancel handler */}
            <ButtonHandler lang={lang} isSending={isSending} onCancel={handleCancelSending} />
          </form>
        </div>
      </div>
    </main>
  );
}

export default ChatPage;
