import React, { Component } from 'react'
import { Web3Provider } from 'react-web3'
import { Provider } from 'react-redux'
// store
import store from './store'
// containers
import Submit from './containers/Submit'
import AmountContainer from './containers/AmountContainer'
import AccountContainer from './containers/AccountContainer'
import LegalTermsContainer from './containers/LegalTermsContainer'
import './App.css';

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <div className="App">
          <Web3Provider>
            <header className="App-header">
              <h1 className="App-title">SingularityNET token sale platform</h1>
            </header>
            <div style={{paddingTop: 50}}>
              <AccountContainer />
              <AmountContainer />
              <LegalTermsContainer />
              <Submit />
            </div>
          </Web3Provider>
        </div>
      </Provider>
    )
  }
}

export default App
