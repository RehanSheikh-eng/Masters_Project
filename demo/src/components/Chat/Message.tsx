import React from 'react';
import { MessageInterface } from '../helpers/Interfaces';
type Props = {
  message: MessageInterface; // Assuming any is your Message type
  isLast: boolean;
};

const Message = ({ message, isLast }: Props) => {
  return (
    <div style={{ opacity: isLast ? 1 : 0.5 }}>
      <p>{message.text}</p>
    </div>
  );
};

export default Message;