/**
 * App root component.
 *
 * Wraps the application in Redux Provider and renders
 * the LogInteraction page.
 */

import { Provider } from 'react-redux';
import store from './redux/store';
import LogInteraction from './pages/LogInteraction';

export default function App() {
  return (
    <Provider store={store}>
      <LogInteraction />
    </Provider>
  );
}
