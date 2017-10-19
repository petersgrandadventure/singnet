import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
// actions
import { submitPayment } from '../actions/payment'

const Submit = ({ legalTerms, amount, account, submitPayment }) => (
  <input
    value="Buy"
    type="button"
    disabled={!(legalTerms && amount && account)}
    onClick={() => submitPayment(account, amount.ether)}
  />
)

Submit.propTypes = {
  legalTerms: PropTypes.bool.isRequired,
  account: PropTypes.string.isRequired,
  submitPayment: PropTypes.func.isRequired,
  amount: PropTypes.shape({
    agi: PropTypes.number.isRequired,
    ether: PropTypes.number.isRequired
  })
}

const mapStateToProps = (store) => (store)
const mapDispatchToProps = (dispatch) => ({
  submitPayment: (account, amount) => dispatch(submitPayment(account, amount))
})

export default connect(mapStateToProps, mapDispatchToProps)(Submit)