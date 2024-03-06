// GoogleMapComponent.tsx
import React, {useState, useContext, useRef} from 'react';
import { APIProvider, Map, ControlPosition, MapControl, useMap } from '@vis.gl/react-google-maps';
import { SearchMapControl } from './SearchMapControl';
import MapHandler from './MapHandler';
import { ImageProcessingContext } from '../../context/ImageProcessingContext';
import { Tensor } from "onnxruntime-web";

interface GoogleMapComponentProps {
  defaultCenter: { lat: number; lng: number };
  defaultZoom: number;
}

const GoogleMapComponent: React.FC<GoogleMapComponentProps> = ({ defaultCenter, defaultZoom }) => {
  
  const [selectedPlace, setSelectedPlace] = useState<google.maps.places.PlaceResult | null>(null);
  const [isMapInteractive, setIsMapInteractive] = useState(true);
  const { setImageString, setTensor, setClicks } = useContext(ImageProcessingContext)!;
  const mapContainerRef = useRef<HTMLDivElement>(null);


  const map = useMap();
  const fetchAndSetImageData = async () => {
    if (!map || !mapContainerRef.current) return;

    const center = map.getCenter();
    const zoom = map.getZoom();
    // Make sure center and zoom are defined
    if (!center || zoom === undefined) {
      console.error("Map center or zoom is undefined.");
      return;
    }

    const centerLat = center.lat();
    const centerLng = center.lng();
    const mapWidth = mapContainerRef.current.offsetWidth;
    const mapHeight = mapContainerRef.current.offsetHeight;

    try {
      const response = await fetch('http://127.0.0.1:5000/api/compute_embedding', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          center: `${centerLat},${centerLng}`,
          zoom,
          size: `${mapWidth}x${mapHeight}`
        })
      });
      const data = await response.json();

      if (data.success && data.image) {
        setImageString(data.image);

        if(data.embedding && data.embedding.data && data.embedding.shape) {

          setTensor(new Tensor(data.embedding.dtype, data.embedding.data, data.embedding.shape));
        }
      } else {
        console.error('Failed to fetch data:', data.error);
      }
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const toggleMapInteraction = () => {
    setIsMapInteractive(!isMapInteractive);
    if (isMapInteractive) {
      fetchAndSetImageData();
      setClicks([]); // Reset clicks when starting a new session
    }
  };

  return (
      <div ref={mapContainerRef} style={{ width: '100%', height: '100%' }}>
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
      </div>
  );
};

export default GoogleMapComponent;
