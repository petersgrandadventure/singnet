import { createStore, applyMiddleware, compose } from 'redux'
// import devToolsEnhancer from 'remote-redux-devtools'
import rootReducer from '../reducers/index'
import thunk from 'redux-thunk'
// import logger from 'redux-logger'

const store = createStore(
  rootReducer,
  compose(applyMiddleware(thunk))
)


export default store

// devToolsEnhancer({ hostname: 'localhost', port: 8000 })