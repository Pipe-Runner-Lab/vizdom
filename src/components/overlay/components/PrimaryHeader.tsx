import React from 'react';
import { GoGraph as ExploreIcon } from 'react-icons/go';
import { IoIosGitCompare as CompareIcon } from 'react-icons/io';
import { VscChromeClose as CloseIcon } from 'react-icons/vsc';
import { clsx as cx } from 'clsx';
import useStore from '../../../store';

function PrimaryHeader(): JSX.Element {
  const primaryMenuMode = useStore((state) => state.primaryMenuMode);
  const setIsMenuOpen = useStore((state) => state.setIsMenuOpen);

  return (
    <div className="flex justify-between w-full">
      <div className="flex space-x-2">
        <button
          className={cx(
            'flex items-center justify-center w-10 h-10  rounded-full outline -outline-offset-1 outline-1',
            primaryMenuMode === 'explore' ? 'outline-sky-400 bg-sky-100' : 'outline-gray-300'
          )}>
          <ExploreIcon
            size={18}
            className={cx(primaryMenuMode === 'explore' ? 'fill-sky-500' : 'fill-gray-400')}
          />
        </button>
        <button
          className={cx(
            'flex items-center justify-center w-10 h-10  rounded-full outline -outline-offset-1 outline-1',
            primaryMenuMode === 'compare' ? 'outline-sky-400 bg-sky-100' : 'outline-gray-300'
          )}>
          <CompareIcon
            size={18}
            className={cx(primaryMenuMode === 'compare' ? 'fill-sky-500' : 'fill-gray-400')}
          />
        </button>
      </div>
      <button
        className="flex items-center justify-center w-10 h-10 bg-red-300 rounded-md shadow-lg"
        onClick={() => setIsMenuOpen(false)}>
        <CloseIcon size={26} />
      </button>
    </div>
  );
}

export default PrimaryHeader;
