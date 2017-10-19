import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
// actions
import ethToAgi from '../actions/amount'
// components
import Amount from '../components/Amount'

const AmountContainer = ({ amount, ethToAgi }) => (
  <Amount amount={amount} convert={(amount) => ethToAgi(amount)} />
)

AmountContainer.propTypes = {
  ethToAgi: PropTypes.func.isRequired,
  amount: PropTypes.shape({
    agi: PropTypes.number.isRequired,
    ether: PropTypes.number.isRequired
  })
}

const mapStateToProps = ({ amount }) => ({ amount })
const mapDispatchToProps = (dispatch) => ({
  ethToAgi: (amount) => dispatch(ethToAgi(amount))
})

export default connect(mapStateToProps, mapDispatchToProps)(AmountContainer)