'use client';
import React, { useState } from 'react';
import { Mic, Square, Bot, Loader } from 'lucide-react';

const SessionPage = () => {
  const [isListening, setIsListening] = useState(false);
  const [suggestion, setSuggestion] = useState('');
  const [transcribedText, setTranscribedText] = useState('');

  const handleToggleListening = () => {
    setIsListening(!isListening);
    // TODO: Connect to WebSocket and start/stop audio streaming
    if (!isListening) {
      setTranscribedText("Interviewer: Tell me about a challenging project you worked on...");
      setSuggestion("Loading suggestion...");
      // Simulate API call
      setTimeout(() => {
        setSuggestion(
          "1. Start with the STAR method (Situation, Task, Action, Result).\n" +
          "2. Describe the project and the core challenge clearly.\n" +
          "3. Explain your specific role and actions taken.\n" +
          "4. Conclude with a positive, measurable outcome."
        );
      }, 2000);
    } else {
      setTranscribedText('');
      setSuggestion('');
    }
  };

  return (
    <div className="flex flex-col h-full">
      <h1 className="text-4xl font-bold mb-8">Live Interview Session</h1>
      
      <div className="flex-1 bg-gray-800 rounded-2xl p-8 border border-gray-700 flex flex-col gap-8">
        {/* Control Button */}
        <button
          onClick={handleToggleListening}
          className={`w-48 mx-auto flex items-center justify-center gap-3 py-4 px-6 text-lg font-semibold rounded-full transition-all duration-300 transform hover:scale-105 ${
            isListening ? 'bg-red-600 hover:bg-red-700' : 'bg-indigo-600 hover:bg-indigo-700'
          }`}
        >
          {isListening ? <Square size={24} /> : <Mic size={24} />}
          <span>{isListening ? 'Stop Session' : 'Start Session'}</span>
        </button>

        {/* Transcribed Text Area */}
        <div className="bg-gray-900 p-4 rounded-lg min-h-[80px]">
          <h3 className="text-sm font-semibold text-gray-400 mb-2">Transcribed Question:</h3>
          <p className="text-gray-200">{transcribedText || 'Waiting for interviewer to speak...'}</p>
        </div>

        {/* AI Suggestion Area */}
        <div className="bg-gray-900 p-6 rounded-lg flex-1">
           <h3 className="flex items-center gap-2 text-md font-semibold text-indigo-400 mb-4">
            <Bot size={20}/>
            AI Suggestion
          </h3>
          {suggestion === 'Loading suggestion...' ? (
            <div className="flex items-center justify-center h-full">
              <Loader size={32} className="animate-spin text-gray-500" />
            </div>
          ) : (
            <pre className="text-gray-200 whitespace-pre-wrap font-sans">
              {suggestion || 'Click "Start Session" to get real-time suggestions.'}
            </pre>
          )}
        </div>
      </div>
    </div>
  );
};

export default SessionPage;
