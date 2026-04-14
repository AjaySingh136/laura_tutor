'use client';

import { useState, useRef, useEffect } from 'react';
import { tutorApi } from '@/lib/api';
import { useTutorStore } from '@/lib/store';
import { toast } from 'react-hot-toast';
import { Send, Loader } from 'lucide-react';
import Markdown from 'react-markdown';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  assessment?: string;
  timestamp: Date;
}

export function ChatInterface() {
  const sessionId = useTutorStore((state) => state.sessionId);
  const topic = useTutorStore((state) => state.topic);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [currentAssessment, setCurrentAssessment] = useState<any>(null);
  const [assessmentAnswer, setAssessmentAnswer] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!inputValue.trim() || !sessionId) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await tutorApi.sendMessage(sessionId, inputValue);

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.data.tutor_response,
        assessment: response.data.assessment_question,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);

      if (response.data.assessment_question) {
        setCurrentAssessment({
          question: response.data.assessment_question,
          id: Date.now().toString(),
        });
      }
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to get response');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmitAssessment = async () => {
    if (!assessmentAnswer.trim() || !sessionId || !currentAssessment) return;

    setIsLoading(true);
    try {
      const response = await tutorApi.submitAnswer(
        sessionId,
        currentAssessment.id,
        assessmentAnswer
      );

      const feedbackMessage: Message = {
        id: (Date.now() + 2).toString(),
        role: 'assistant',
        content: `**Assessment Feedback:**\n\n${response.data.feedback}\n\n**Mastery Score:** ${response.data.mastery_score}/100`,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, feedbackMessage]);
      setCurrentAssessment(null);
      setAssessmentAnswer('');

      if (response.data.follow_up) {
        setTimeout(() => {
          const followupMessage: Message = {
            id: (Date.now() + 3).toString(),
            role: 'assistant',
            content: response.data.follow_up,
            timestamp: new Date(),
          };
          setMessages((prev) => [...prev, followupMessage]);
        }, 1000);
      }
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to submit answer');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 shadow-lg">
        <h1 className="text-2xl font-bold">{topic}</h1>
        <p className="text-blue-100">AI Tutor Session</p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center">
              <div className="text-6xl mb-4">👋</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                Ready to learn {topic}?
              </h2>
              <p className="text-gray-600">
                Ask me anything! I'm here to help you understand this topic.
              </p>
            </div>
          </div>
        )}

        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`message-bubble ${
                message.role === 'user'
                  ? 'user-message'
                  : 'assistant-message'
              }`}
            >
              <Markdown className="text-sm">{message.content}</Markdown>
              <span className="text-xs opacity-70 mt-2 block">
                {message.timestamp.toLocaleTimeString()}
              </span>
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="assistant-message message-bubble">
              <Loader className="inline-block animate-spin" size={20} />
              <span className="ml-2">Tutor is thinking...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Assessment */}
      {currentAssessment && !isLoading && (
        <div className="bg-amber-50 border-t-4 border-amber-400 p-6">
          <h3 className="font-semibold text-amber-900 mb-3">
            Quick Check: {currentAssessment.question}
          </h3>
          <div className="flex gap-2">
            <input
              type="text"
              value={assessmentAnswer}
              onChange={(e) => setAssessmentAnswer(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') handleSubmitAssessment();
              }}
              placeholder="Your answer..."
              className="flex-1 px-4 py-2 border border-amber-200 rounded-lg focus:ring-2 focus:ring-amber-500"
            />
            <button
              onClick={handleSubmitAssessment}
              disabled={!assessmentAnswer.trim()}
              className="px-6 py-2 bg-amber-500 hover:bg-amber-600 text-white rounded-lg font-semibold disabled:opacity-50 transition-colors"
            >
              Submit
            </button>
          </div>
        </div>
      )}

      {/* Input */}
      <form onSubmit={handleSendMessage} className="bg-white border-t p-6">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            placeholder="Ask me anything about this topic..."
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !inputValue.trim()}
            className="px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white rounded-lg font-semibold transition-all disabled:opacity-50 flex items-center gap-2"
          >
            {isLoading ? (
              <Loader className="animate-spin" size={20} />
            ) : (
              <Send size={20} />
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
