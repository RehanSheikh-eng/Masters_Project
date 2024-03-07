import React from 'react';
import Message from './Message';
import { MessageInterface } from '../helpers/Interfaces';
type Props = {
  messages: MessageInterface[]; // Assuming any[] is your Message type
};

const MessageList = ({ messages }: Props) => {
  return (
    <div>
      {messages.map((message, index) => (
        <Message key={index} message={message} isLast={index === messages.length - 1} />
      ))}
    </div>
  );
};

export default MessageList;