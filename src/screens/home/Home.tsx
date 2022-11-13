import React from 'react';
import Map from '../../components/map';
import Overlay from '../../components/overlay/Overlay';

function Home(): JSX.Element {
  return (
    <div className="h-full">
      <Map />
      <div className="absolute top-0 bottom-0 left-0 right-0 p-4 overflow-hidden pointer-events-none">
        <Overlay />
      </div>
    </div>
  );
}

export default Home;
