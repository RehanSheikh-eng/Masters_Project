// GoogleMapComponent.tsx
import React, {useState} from 'react';
import { APIProvider, Map, ControlPosition } from '@vis.gl/react-google-maps';
import { CustomMapControl } from './MapControl';
import MapHandler from './MapHandler';

interface GoogleMapComponentProps {
  apiKey: string;
  defaultCenter: { lat: number; lng: number };
  defaultZoom: number;
}

const GoogleMapComponent: React.FC<GoogleMapComponentProps> = ({ apiKey, defaultCenter, defaultZoom }) => {
  
  const [selectedPlace, setSelectedPlace] =
  useState<google.maps.places.PlaceResult | null>(null);
  
  return (
    <APIProvider apiKey={apiKey}>
      <Map
        mapTypeId={'satellite'}
        defaultZoom={3}
        defaultCenter={{ lat: 22.54992, lng: 0 }}
        gestureHandling={'greedy'}
        disableDefaultUI={true}
        style={{ width: '100%', height: '100%' }}
      />

      <CustomMapControl
        controlPosition={ControlPosition.TOP}
        onPlaceSelect={setSelectedPlace}
      />

      <MapHandler 
        place={selectedPlace} 
      />
    </APIProvider>
  );
};

export default GoogleMapComponent;
