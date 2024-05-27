import React from 'react';
import { ImageProcessingProvider } from './context/ImageProcessingContext';
import { ChatProvider } from './context/ChatContext';
import Stage from './components/Stage';
import './assets/scss/App.scss'; // Assuming your styles are here
import GoogleMapComponent from './components/GoogleMapsComponent/GoogleMapComponent';
import { APIProvider } from '@vis.gl/react-google-maps';
import Chat from './components/Chat/Chat';

const App = () => {
  const GOOGLE_API_KEY = ""; 
  return (
    <ImageProcessingProvider>
      <ChatProvider>
        <div className="app">
          <div>
            <Chat/>
          </div>
          <div>
            <Stage />
          </div>

          <div style={{ width: '100vw', height: '100vh' }}>
            <APIProvider apiKey={GOOGLE_API_KEY}>
              <GoogleMapComponent
                defaultCenter={{ lat: 22.54992, lng: 0 }}
                defaultZoom={3}
              />
            </APIProvider>
          </div>

        </div>
      </ChatProvider>
    </ImageProcessingProvider>
  );
};

export default App;
