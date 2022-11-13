import create from 'zustand';

interface Store {
  isMenuOpen: boolean;
  setIsMenuOpen: (open: boolean) => void;
}

const useStore = create<Store>((set) => ({
  isMenuOpen: true,
  setIsMenuOpen: (open: boolean) => set({ isMenuOpen: open })
}));

export default useStore;
