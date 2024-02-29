import React from 'react';
import { ImageProcessingProvider } from './context/ImageProcessingContext';
import Stage from './components/Stage';
import './assets/scss/App.scss'; // Assuming your styles are here
import GoogleMapComponent from './components/GoogleMapsComponent/GoogleMapComponent';

const App = () => {
  const GOOGLE_API_KEY = "AIzaSyAtwbpPJw7ExShbQwodo-YQauutmlWsjWU";
  return (
    <ImageProcessingProvider>
      <div className="app">
        <div>
          {/* <Stage /> */}
        </div>

        <div style={{ width: '100vw', height: '100vh' }}>
          <GoogleMapComponent
            apiKey={GOOGLE_API_KEY!}
            defaultCenter={{ lat: 22.54992, lng: 0 }} // Example default center
            defaultZoom={3} // Example default zoom level
          />
        </div>
      </div>
    </ImageProcessingProvider>
  );
};

export default App;
