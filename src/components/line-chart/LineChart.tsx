import React, { useEffect, useState } from 'react';
import { Line } from '@ant-design/plots';

function LineChart(): JSX.Element {
  const [data, setData] = useState<Array<{ Date: string; value: number }>>([]);

  useEffect(() => {
    asyncFetch();
  }, []);

  const asyncFetch = (): void => {
    fetch('http://127.0.0.1:5000/dummy_data')
      // eslint-disable-next-line @typescript-eslint/promise-function-async
      .then((response) => response.json())
      .then((json) =>
        setData(json.map((item: [number, number, number]) => ({ Date: item[1], Value: item[2] })))
      )
      .catch((error) => {
        console.log('fetch data failed', error);
      });
  };

  const config = {
    data,
    xField: 'Date',
    yField: 'Value',
    xAxis: {
      // type: 'timeCat',
      tickCount: 5
    }
  };

  return (
    <div className="w-full">
      <Line {...config} />
    </div>
  );
}

export default LineChart;
