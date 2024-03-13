import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useImageProcessing } from './ImageProcessingContext';
import { MessageInterface } from '../components/helpers/Interfaces';

interface ChatContextType {
  messages: MessageInterface[];
  combinedImageBase64: string | null;
  isRunning: boolean;
  setCombinedImageBase64: (combinedImageBase64: string | null) => void;
  sendMessage: (message: string) => Promise<void>;
  resetConversation: () => void;
  
}

const ChatContext = createContext<ChatContextType | undefined>(undefined);

export const ChatProvider = ({ children }: { children: ReactNode }) => {

  const [messages, setMessages] = useState<MessageInterface[]>([]);
  const { image, maskImg } = useImageProcessing();
  const [combinedImageBase64, setCombinedImageBase64] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const sendMessage = async (message: string) => {
    setIsRunning(true);
    try {
      // Construct the payload, including the base64 image
      const response = await fetch('http://127.0.0.1:5000/api/upload_gpt4v', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: message,
          file: combinedImageBase64
        })
      });
      const data = await response.json();

      if (data.success && data.analysis) {
        const newMessage = data.analysis;
        setMessages([...messages, { id: Date.now(), text: newMessage, role: 'assistant' }]);
      } else {
        console.error('Error sending message:', data.error);
      }
      // Handle response, update messages

    } catch (error) {
      console.error('Error sending message:', error);
    }
    setIsRunning(false);
  };

  useEffect(() => {
    combineAndEncodeImage();
  }, [image, maskImg]);

  const resetConversation = () => {
    setMessages([]);
  };

  const combineAndEncodeImage = async () => {
    if (!image || !maskImg) return;
  
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = image.width;
    canvas.height = image.height;
  
    // Draw the original image
    ctx!.drawImage(image, 0, 0);
    // Draw the mask image on top
    ctx!.globalAlpha = 0.4;
    ctx!.drawImage(maskImg, 0, 0);
    // Convert the canvas content to base64
    const combinedImageBase64 = canvas.toDataURL('image/png');
    console.log("Combined image base64:", combinedImageBase64);
    setCombinedImageBase64(combinedImageBase64);
  };

  const value = {
    messages,
    combinedImageBase64,
    isRunning,
    setCombinedImageBase64,
    sendMessage,
    resetConversation,
  };
  
  return (
    <ChatContext.Provider value={value}>
      {children}
    </ChatContext.Provider>
  );
};

export const useChat = () => {
  const context = useContext(ChatContext);
  if (!context) throw new Error('useChat must be used within a ChatProvider');
  return context;
};
