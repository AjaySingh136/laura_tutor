'use client';

import { useState } from 'react';
import { tutorApi } from '@/lib/api';
import { useTutorStore } from '@/lib/store';
import { toast } from 'react-hot-toast';
import { ArrowRight, Youtube, BookOpen } from 'lucide-react';

export function SessionStart() {
  const [topic, setTopic] = useState('');
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [difficulty, setDifficulty] = useState('intermediate');
  const [enableAssessment, setEnableAssessment] = useState(true);
  const [isLoading, setIsLoading] = useState(false);

  const setSessionId = useTutorStore((state) => state.setSessionId);
  const setStoreTopic = useTutorStore((state) => state.setTopic);

  const handleStartSession = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!topic.trim()) {
      toast.error('Please enter a topic');
      return;
    }

    setIsLoading(true);
    try {
      const response = await tutorApi.createSession({
        topic: topic.trim(),
        difficulty_level: difficulty,
        youtube_url: youtubeUrl || undefined,
        enable_assessment: enableAssessment,
      });

      setSessionId(response.data.id);
      setStoreTopic(response.data.topic);
      toast.success('Session started! Let\'s learn.');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to start session');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-600 via-purple-600 to-pink-600 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-white rounded-2xl shadow-2xl p-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            AI Tutor
          </h1>
          <p className="text-gray-600 mb-8">
            Learn any topic with an expert AI tutor
          </p>

          <form onSubmit={handleStartSession} className="space-y-6">
            {/* Topic Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <BookOpen className="inline mr-2" size={18} />
                What do you want to learn?
              </label>
              <input
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="e.g., Quantum Computing, Photosynthesis, Calculus"
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={isLoading}
              />
            </div>

            {/* Difficulty Level */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Difficulty Level
              </label>
              <select
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={isLoading}
              >
                <option value="beginner">Beginner - Simple explanations</option>
                <option value="intermediate">Intermediate - Balanced depth</option>
                <option value="advanced">Advanced - Technical detail</option>
              </select>
            </div>

            {/* YouTube URL */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Youtube className="inline mr-2" size={18} />
                YouTube URL (Optional)
              </label>
              <input
                type="url"
                value={youtubeUrl}
                onChange={(e) => setYoutubeUrl(e.target.value)}
                placeholder="https://youtube.com/watch?v=..."
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                disabled={isLoading}
              />
              <p className="text-sm text-gray-500 mt-1">
                Paste a YouTube link and the tutor will learn from it
              </p>
            </div>

            {/* Assessment Toggle */}
            <div className="flex items-center">
              <input
                type="checkbox"
                id="assessment"
                checked={enableAssessment}
                onChange={(e) => setEnableAssessment(e.target.checked)}
                className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                disabled={isLoading}
              />
              <label htmlFor="assessment" className="ml-3 text-sm text-gray-700">
                Enable assessment questions during session
              </label>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold py-3 rounded-lg transition-all flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {isLoading ? 'Starting...' : 'Start Learning'} <ArrowRight size={20} />
            </button>
          </form>

          <div className="mt-6 pt-6 border-t border-gray-200">
            <h3 className="font-semibold text-gray-900 mb-3">Features:</h3>
            <ul className="space-y-2 text-sm text-gray-600">
              <li>✨ Expert AI explanations</li>
              <li>❓ Ask questions anytime</li>
              <li>📊 Get assessment feedback</li>
              <li>📹 Learn from YouTube videos</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
