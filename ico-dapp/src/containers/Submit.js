import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
// import Web3 from 'web3'

// const web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"))
const { web3 } = window

const Submit = ({ legalTerms, amount, account }) => {
  return (
    <input
      value="Buy"
      type="button"
      disabled={!(legalTerms && amount && account)}
      onClick={
        () => web3.eth.sendTransaction(
          {
            from: account,
            to: "0xadd720987528b9b9bc6cebedc5f38e6f80e6de47",//web3.eth.accounts[1],
            value: web3.toWei(amount.ether, "ether")
          },
          (err, res) => err ? console.log(err) : console.log(res)
        )
      }
    />
  )
}

Submit.propTypes = {
  legalTerms: PropTypes.bool.isRequired,
  account: PropTypes.string.isRequired,
  amount: PropTypes.shape({
    agi: PropTypes.number.isRequired,
    ether: PropTypes.number.isRequired
  })
}

const mapStateToProps = (store) => (store)

export default connect(mapStateToProps)(Submit)