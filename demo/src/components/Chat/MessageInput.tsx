import React, { useState } from 'react';

type Props = {
  sendMessage: (message: string) => void;
  isRunning: boolean;
};

const MessageInput = ({ sendMessage, isRunning }: Props) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!message.trim()) return;
    sendMessage(message);
    setMessage('');
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        disabled={isRunning}
      />
      <button type="submit" disabled={isRunning}>Send</button>
    </form>
  );
};

export default MessageInput;