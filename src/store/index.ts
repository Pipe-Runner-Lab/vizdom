import create from 'zustand';

type PrimaryMenuMode = 'explore' | 'compare';

interface Store {
  isMenuOpen: boolean;
  setIsMenuOpen: (open: boolean) => void;
  primaryMenuMode: PrimaryMenuMode;
  setPrimaryMenuMode: (mode: PrimaryMenuMode) => void;
}

const useStore = create<Store>((set) => ({
  isMenuOpen: true,
  setIsMenuOpen: (open: boolean) => set({ isMenuOpen: open }),
  primaryMenuMode: 'explore',
  setPrimaryMenuMode: (mode: PrimaryMenuMode) => set({ primaryMenuMode: mode })
}));

export default useStore;
