import React from 'react'
import PropTypes from 'prop-types'

const Account = ({ address }) => (
  <div>
    <span>account: {address}</span>
  </div>
)

Account.propTypes = {
  address: PropTypes.string.isRequired
}

export default Account