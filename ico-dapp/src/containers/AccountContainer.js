import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'
// component
import Account from '../components/Account'

const AccountContainer = ({ account }, context) => {
  return (
    <Account address={account} />
  )
}

AccountContainer.contextTypes = {
  web3: PropTypes.object
}

const mapStateToProps = ({ account }) => ({ account })

export default connect(mapStateToProps)(AccountContainer)