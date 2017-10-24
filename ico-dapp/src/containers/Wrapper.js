import PropTypes from 'prop-types'
import { connect } from 'react-redux'
import React, { Component } from 'react'
import { Web3Provider } from 'react-web3'
// containers
import Submit from './Submit'
import AmountContainer from './AmountContainer'
import AccountContainer from './AccountContainer'
import LegalTermsContainer from './LegalTermsContainer'
// actions
import { checkCrowdsaleStatus, statusTypes } from '../actions/crowdsaleStatus'

class Wrapper extends Component {

  componentWillMount() {
    this.props.checkCrowdsaleStatus()
  }

  componentWillReceiveProps(nextProps) {
    const { payment: { response, error } } = this.props

    if (nextProps.payment.response && nextProps.payment.response !== response) {
      alert('Transaction Succeed')
    }

    if (nextProps.payment.error && nextProps.payment.error !== error) {
      alert('Transaction rejected')
    }
  }
  
  render() {
    const { crowdsale } = this.props

    if (crowdsale.isLoading) {
      return <span>Loading...</span>
    }
    
    if (crowdsale.status === statusTypes.tooEarly) {
      return (
        <div style={{paddingTop: 50}}>
          <span>ICO not yet started</span>
        </div>
      )
    }

    if (crowdsale.status === statusTypes.tooLate) {
      return (
        <div style={{paddingTop: 50}}>
          <span>ICO has been closed</span>
        </div>
      )
    }

    return (
      <Web3Provider>
        <div style={{paddingTop: 50}}>
          <AccountContainer />
          <AmountContainer />
          <LegalTermsContainer />
          <Submit />
        </div>
      </Web3Provider>
    )
  }

}

Wrapper.propTypes = {
  payment: PropTypes.object.isRequired,
  crowdsale: PropTypes.object.isRequired,
  checkCrowdsaleStatus: PropTypes.func.isRequired
}

const mapStateToProps = ({ crowdsale, payment }) => ({ crowdsale, payment })
const mapDispatchToProps = (dispatch) => ({
  checkCrowdsaleStatus: () => dispatch(checkCrowdsaleStatus())
})

export default connect(mapStateToProps, mapDispatchToProps)(Wrapper)