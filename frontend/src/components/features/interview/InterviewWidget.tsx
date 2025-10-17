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
        try {
          const stream = await navigator.mediaDevices.getUserMedia({
            audio: {
              echoCancellation: true,
              noiseSuppression: true,
              sampleRate: 48000
            }
          });

          // WebM Opus format for better compatibility with Google Speech-to-Text
          let options: MediaRecorderOptions = {
            mimeType: 'audio/webm;codecs=opus'
          };

          // Check if the browser supports the desired format
          if (!MediaRecorder.isTypeSupported(options.mimeType!)) {
            console.warn('WebM Opus not supported, using default format');
            options = {};
          }

          mediaRecorderRef.current = new MediaRecorder(stream, options);

          mediaRecorderRef.current.ondataavailable = (event) => {
            if (event.data.size > 0 && socketRef.current?.readyState === WebSocket.OPEN) {
              socketRef.current.send(event.data);
            }
          };

          mediaRecorderRef.current.onerror = (event) => {
            console.error('MediaRecorder error:', event);
            setStatus('Error');
            setIsListening(false);
            cleanup();
          };

          // Send audio data every 1 second for better real-time performance
          mediaRecorderRef.current.start(1000);
        } catch (streamError) {
          console.error('Error accessing microphone:', streamError);
          setStatus('Error');
          setIsListening(false);
        }
      };

      socketRef.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === 'transcript') {
              setTranscribedText(data.text);
          } else if (data.type === 'suggestion') {
              setSuggestion(data.text);
          } else if (data.type === 'error') {
              console.error('Backend error:', data.text);
              setStatus('Error');
              setIsListening(false);
              cleanup();
          }
        } catch (parseError) {
          console.error('Error parsing WebSocket message:', parseError);
        }
      };

      socketRef.current.onclose = (event) => {
        console.log('WebSocket connection closed:', event.code, event.reason);
        setStatus('Idle');
        setIsListening(false);
      };

      socketRef.current.onerror = (error) => {
        console.error('WebSocket error:', error);
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
        {/* Status Indicator */}
        <div className="bg-gray-900/50 p-3 rounded-lg">
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${
              status === 'Listening' ? 'bg-green-500' :
              status === 'Connecting' ? 'bg-yellow-500 animate-pulse' :
              status === 'Error' ? 'bg-red-500' : 'bg-gray-500'
            }`} />
            <span className="text-sm text-gray-300">
              Status: {status === 'Listening' ? 'Listening for questions...' :
                      status === 'Connecting' ? 'Connecting...' :
                      status === 'Error' ? 'Connection Error' : 'Ready'}
            </span>
          </div>
        </div>

        {/* Transcribed Text Section */}
        <div className="bg-gray-900/50 p-4 rounded-lg min-h-[100px]">
          <h4 className="text-sm font-semibold text-gray-400 mb-2">Interviewer Question:</h4>
          <p className="text-gray-200">
            {transcribedText || (isListening ? 'Listening for interviewer questions...' : 'Start the session to see the transcript.')}
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
