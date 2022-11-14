import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import useStore from '../../store';
import { HiOutlineMenu as OpenIcon } from 'react-icons/hi';

import PrimaryHeader from './components/PrimaryHeader';
import ExplorationPanel from '../exploration-panel';

const mainPanelVariants = {
  open: {
    x: 0
  },
  closed: {
    x: 'calc(100% + 0.5rem)'
  }
};

const secondaryPanelVariants = {
  open: {
    y: 0
  },
  closed: {
    y: 'calc(100% + 0.5rem)'
  }
};

function Overlay(): JSX.Element {
  const isMenuOpen = useStore((state) => state.isMenuOpen);
  const setIsMenuOpen = useStore((state) => state.setIsMenuOpen);

  return (
    <div className="flex w-full h-full space-x-2">
      <div className="flex flex-col justify-end flex-1">
        <div className="flex-1 hidden">hi</div>
        <motion.div
          variants={secondaryPanelVariants}
          animate={isMenuOpen ? 'open' : 'closed'}
          transition={{
            duration: 0.3,
            type: 'tween'
          }}
          className="h-24 rounded-md shadow-lg pointer-events-auto bg-white/80 backdrop-blur-sm">
          {/* Secondary Panel content */}
        </motion.div>
      </div>
      <div className="flex w-2/5 max-w-md">
        <motion.div
          variants={mainPanelVariants}
          animate={isMenuOpen ? 'open' : 'closed'}
          transition={{
            duration: 0.3,
            type: 'tween'
          }}
          className="relative w-full h-full rounded-md shadow-lg pointer-events-auto bg-white/80 backdrop-blur-sm">
          <AnimatePresence>
            {!isMenuOpen && (
              <motion.button
                initial={{ opacity: 0 }}
                animate={{ opacity: 1, transition: { duration: 1 } }}
                exit={{ opacity: 0, transition: { duration: 0.3 } }}
                className="shadow-md bg-blue-300 w-10 h-10 rounded-md absolute top-[0.5rem] left-0 translate-x-[calc(-100%-1rem)] flex items-center justify-center"
                onClick={() => setIsMenuOpen(true)}>
                <OpenIcon size={26} />
              </motion.button>
            )}
          </AnimatePresence>
          {/* Primary Panel content */}
          <div className="w-full p-2">
            <PrimaryHeader />
          </div>

          <div className="h-[1px] w-auto mx-2 bg-gray-300" />

          <div>
            <ExplorationPanel />
          </div>
        </motion.div>
      </div>
    </div>
  );
}

export default Overlay;
