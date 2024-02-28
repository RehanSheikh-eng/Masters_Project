import React from 'react';
import { ImageProcessingProvider } from './context/ImageProcessingContext';
import Stage from './components/Stage';
import './assets/scss/App.scss'; // Assuming your styles are here

const App = () => {
  return (
    <ImageProcessingProvider>
      <div className="app">
        <Stage />
        {/* Any other components that should be part of your app's layout can go here */}
      </div>
    </ImageProcessingProvider>
  );
};

export default App;
