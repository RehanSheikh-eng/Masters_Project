import React from 'react';
import {ControlPosition, MapControl} from '@vis.gl/react-google-maps';
import {PlaceAutocomplete} from './PlaceAutocomplete';

type CustomAutocompleteControlProps = {
  controlPosition: ControlPosition;
  onPlaceSelect: (place: google.maps.places.PlaceResult | null) => void;
};

export const SearchMapControl = ({
  controlPosition,
  onPlaceSelect
}: CustomAutocompleteControlProps) => {

  return (
    <MapControl position={controlPosition}>
      <div className="autocomplete-control">
        <PlaceAutocomplete onPlaceSelect={onPlaceSelect} />
      </div>
    </MapControl>
  );
};