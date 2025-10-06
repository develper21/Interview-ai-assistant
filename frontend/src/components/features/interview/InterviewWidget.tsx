'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Mic, Square, Bot, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';

const InterviewWidget = () => {
  const [isListening, setIsListening] = useState(false);
  const [suggestion, setSuggestion] = useState('');
  const [transcribedText, setTranscribedText] = useState('');
  const [status, setStatus] = useState('Idle'); // 'Idle', 'Connecting', 'Listening', 'Error'

  // Refs for WebSocket and MediaRecorder
  const socketRef = useRef<WebSocket | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  // Function to handle WebSocket and MediaRecorder cleanup
  const cleanup = () => {
      if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
          mediaRecorderRef.current.stop();
      }
      if (socketRef.current) {
          socketRef.current.close();
      }
      mediaRecorderRef.current = null;
      socketRef.current = null;
  };

  useEffect(() => {
    // Cleanup on component unmount
    return () => cleanup();
  }, []);
  
  const handleToggleListening = async () => {
    if (isListening) {
      // Stop listening
      setIsListening(false);
      setStatus('Idle');
      cleanup();
      return;
    }

    // Start listening
    setIsListening(true);
    setStatus('Connecting');
    setSuggestion('');
    setTranscribedText('');

    try {
      // Connect to WebSocket server
      socketRef.current = new WebSocket('ws://127.0.0.1:8000/ws'); // Backend URL
      
      socketRef.current.onopen = async () => {
        setStatus('Listening');
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorderRef.current = new MediaRecorder(stream);

        mediaRecorderRef.current.ondataavailable = (event) => {
          if (event.data.size > 0 && socketRef.current?.readyState === WebSocket.OPEN) {
            socketRef.current.send(event.data);
          }
        };

        // Send audio data every 2 seconds
        mediaRecorderRef.current.start(2000); 
      };

      socketRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data); // Assuming backend sends JSON
        if (data.type === 'transcript') {
            setTranscribedText(data.text);
        } else if (data.type === 'suggestion') {
            setSuggestion(data.text);
        }
      };

      socketRef.current.onclose = () => {
        setStatus('Idle');
        setIsListening(false);
      };

      socketRef.current.onerror = () => {
        setStatus('Error');
        setIsListening(false);
        cleanup();
      };

    } catch (error) {
      console.error('Failed to start microphone:', error);
      setStatus('Error');
      setIsListening(false);
    }
  };

  return (
    <Card className="w-full h-full flex flex-col bg-gray-800 border-gray-700">
      <CardHeader className="flex-row items-center justify-between">
        <CardTitle className="flex items-center gap-2">
          <Bot className="text-indigo-400"/>
          Live AI Assistant
        </CardTitle>
        <Button 
          onClick={handleToggleListening} 
          variant={isListening ? 'destructive' : 'default'} 
          size="sm"
          className="w-32"
        >
          {isListening ? <Square className="mr-2 h-4 w-4" /> : <Mic className="mr-2 h-4 w-4" />}
          {isListening ? 'Stop' : 'Start'}
        </Button>
      </CardHeader>
      <CardContent className="flex-1 flex flex-col gap-4 overflow-auto">
        {/* Transcribed Text Section */}
        <div className="bg-gray-900/50 p-4 rounded-lg min-h-[100px]">
          <h4 className="text-sm font-semibold text-gray-400 mb-2">Interviewer Question:</h4>
          <p className="text-gray-200">
            {transcribedText || (isListening ? 'Listening...' : 'Start the session to see the transcript.')}
          </p>
        </div>
        
        {/* AI Suggestion Section */}
        <div className="bg-gray-900/50 p-4 rounded-lg flex-1">
          <h4 className="text-sm font-semibold text-indigo-400 mb-2">AI Suggestion:</h4>
          <div className="text-gray-200 whitespace-pre-wrap font-sans">
            {suggestion ? suggestion : 
                <div className="flex items-center justify-center h-full text-gray-500">
                {isListening ? <Loader2 className="animate-spin h-8 w-8"/> : 'Suggestions will appear here.'}
                </div>
            }
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default InterviewWidget;
