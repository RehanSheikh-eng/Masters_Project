import React from 'react';

interface StartChatButtonProps {
  isMapInteractive: boolean;
  toggleMapInteraction: () => void;
}

const StartChatButton: React.FC<StartChatButtonProps> = ({ isMapInteractive, toggleMapInteraction }) => {
  return (
    <button onClick={toggleMapInteraction}>
      {isMapInteractive ? 'Start Chat' : 'End Chat'}
    </button>
  );
};

export default StartChatButton;