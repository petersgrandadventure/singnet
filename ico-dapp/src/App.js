import React, { Component } from 'react'
import { Provider } from 'react-redux'
// store
import store from './store'
// containers
import Wrapper from './containers/Wrapper'
// css
import './App.css'

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <div className="App">
          <header className="App-header">
            <h1 className="App-title">SingularityNET token sale platform</h1>
          </header>
          <Wrapper />
        </div>
      </Provider>
    )
  }
}

export default App
