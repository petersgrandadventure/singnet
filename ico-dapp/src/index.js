import React from 'react'
import ReactDOM from 'react-dom'
import { createStore, combineReducers } from 'redux'
import { Provider } from 'react-redux'
import { Router, Route, IndexRoute, browserHistory } from 'react-router'
import { syncHistoryWithStore, routerReducer } from 'react-router-redux'

import { Web3Provider } from 'react-web3';

import * as reducers from './reducers'
import App from './components/App'
import Home from './components/Home'
import Foo from './components/Foo'
import Bar from './components/Bar'

import registerServiceWorker from './registerServiceWorker';

registerServiceWorker()

const reducer = combineReducers({
  ...reducers,
  routing: routerReducer
})


const store = createStore(
  reducer
)
const history = syncHistoryWithStore(browserHistory, store)

ReactDOM.render(
  <Web3Provider>
    <Provider store={store}>
      <div>
        <Router history={history}>
          <Route path="/" component={App}>
            <IndexRoute component={Home} />
            <Route path="foo" component={Foo} />
            <Route path="bar" component={Bar} />
          </Route>
        </Router>
      </div>
    </Provider>
  </Web3Provider>,
  document.getElementById('root')
)
