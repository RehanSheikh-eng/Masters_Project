import React, { useContext, useEffect, useState } from 'react';
import { useChat } from '../../context/ChatContext';
import MessageInput from './MessageInput';
import MessageList from './MessageList';

const Chat = () => {
  const { sendMessage, messages, isRunning } = useChat();
  return (
    <div>
      <MessageList messages={messages} />
      <MessageInput sendMessage={sendMessage} isRunning={isRunning} />
    </div>
  );
};

export default Chat;
