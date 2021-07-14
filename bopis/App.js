import {Provider} from 'react-redux';
import store from './features/store'
import React from 'react';
import NavigatorStack from './layout/NavigatorStack'


 function App() {
  return (
    <Provider store={store}>
      <NavigatorStack />
    </Provider>
  );
}
export default App;
