import React from 'react';
import MapBase from 'react-map-gl';
import DeckGL, { LineLayer } from 'deck.gl/typed';

// Viewport settings
const INITIAL_VIEW_STATE = {
  longitude: -122.4,
  latitude: 37.8,
  zoom: 0,
  pitch: 0,
  bearing: 0
};

const data = [{ sourcePosition: [-122.41669, 37.7853], targetPosition: [-122.41669, 37.781] }];

function Map(): JSX.Element {
  const layers = [new LineLayer({ id: 'line-layer', data })];

  return (
    <div className="w-full h-full">
      <DeckGL initialViewState={INITIAL_VIEW_STATE} controller={true} layers={layers}>
        <MapBase
          mapStyle="mapbox://styles/mapbox/light-v10"
          mapboxAccessToken={process.env.REACT_APP_MAPBOX_TOKEN}
        ></MapBase>
      </DeckGL>
    </div>
  );
}

export default Map;
