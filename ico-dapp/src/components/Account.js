import React from 'react'
import PropTypes from 'prop-types'

const Account = ({ address }) => (
  <div style={{padding: 20}}>
    <span>account: {address}</span>
  </div>
)

Account.propTypes = {
  address: PropTypes.string.isRequired
}

export default Account