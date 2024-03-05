// GoogleMapComponent.tsx
import React, {useState} from 'react';
import { APIProvider, Map, ControlPosition, MapControl } from '@vis.gl/react-google-maps';
import { SearchMapControl } from './SearchMapControl';
import MapHandler from './MapHandler';

interface GoogleMapComponentProps {
  apiKey: string;
  defaultCenter: { lat: number; lng: number };
  defaultZoom: number;
}

const GoogleMapComponent: React.FC<GoogleMapComponentProps> = ({ apiKey, defaultCenter, defaultZoom }) => {
  
  const [selectedPlace, setSelectedPlace] =
  useState<google.maps.places.PlaceResult | null>(null);

  const [isMapInteractive, setIsMapInteractive] = useState(true);

  const toggleMapInteraction = () => {
    setIsMapInteractive(!isMapInteractive);
  };

  return (
    <APIProvider apiKey={apiKey}>
      <Map
        mapTypeId={'satellite'}
        defaultZoom={3}
        defaultCenter={{ lat: 22.54992, lng: 0 }}
        gestureHandling={'greedy'}
        disableDefaultUI={true}
        style={{ width: '100%', height: '100%' }}
        draggable={isMapInteractive}
        scrollwheel={isMapInteractive}
        tilt={0}
      >
        <MapControl position={ControlPosition.TOP_LEFT}>
          <button onClick={toggleMapInteraction}>
            {isMapInteractive ? 'Start Chat' : 'End Chat'}
          </button>
        </MapControl>
        <SearchMapControl
          controlPosition={ControlPosition.TOP}
          onPlaceSelect={setSelectedPlace}
        />      
        <MapHandler 
          place={selectedPlace} 
        />
      </Map>
    </APIProvider>
  );
};

export default GoogleMapComponent;
