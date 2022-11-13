import React from 'react';
import MapBase from 'react-map-gl';

function Map(): JSX.Element {
  return (
    <div className="w-full h-full">
      <MapBase
        initialViewState={{
          longitude: -122.4,
          latitude: 37.8,
          zoom: 0
        }}
        mapStyle="mapbox://styles/mapbox/light-v10"
        mapboxAccessToken={process.env.REACT_APP_MAPBOX_TOKEN}
      />
    </div>
  );
}

export default Map;
