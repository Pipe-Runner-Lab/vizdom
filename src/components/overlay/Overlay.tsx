import React from 'react';
import { motion } from 'framer-motion';
import useStore from '../../store';
import { HiOutlineMenu as OpenIcon } from 'react-icons/hi';
import { VscChromeClose as CloseIcon } from 'react-icons/vsc';

const mainPanelVariants = {
  open: {
    x: 0
  },
  closed: {
    x: 'calc(100% + 1rem)'
  }
};

const secondaryPanelVariants = {
  open: {
    y: 0
  },
  closed: {
    y: 'calc(100% + 1rem)'
  }
};

function Overlay(): JSX.Element {
  const isMenuOpen = useStore((state) => state.isMenuOpen);
  const setIsMenuOpen = useStore((state) => state.setIsMenuOpen);

  return (
    <div className="flex w-full h-full space-x-4">
      <div className="flex flex-col justify-end flex-1">
        <div className="flex-1 hidden">hi</div>
        <motion.div
          variants={secondaryPanelVariants}
          animate={isMenuOpen ? 'open' : 'closed'}
          transition={{
            duration: 0.3,
            type: 'tween'
          }}
          className="h-24 bg-white rounded-md shadow-lg pointer-events-auto">
          {/* Secondary Panel content */}
        </motion.div>
      </div>
      <div className="flex w-1/3 max-w-sm">
        <motion.div
          variants={mainPanelVariants}
          animate={isMenuOpen ? 'open' : 'closed'}
          transition={{
            duration: 0.3,
            type: 'tween'
          }}
          className="relative w-full h-full bg-white rounded-md shadow-lg pointer-events-auto">
          <button
            className="shadow-md bg-white w-10 h-10 rounded-md absolute top-0 left-0 translate-x-[calc(-100%-1rem)] flex items-center justify-center p-0"
            onClick={() => setIsMenuOpen(!isMenuOpen)}>
            {isMenuOpen ? <CloseIcon size={26} /> : <OpenIcon size={26} />}
          </button>
          {/* Primary Panel content */}
        </motion.div>
      </div>
    </div>
  );
}

export default Overlay;
