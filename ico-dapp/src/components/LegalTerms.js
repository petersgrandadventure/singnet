import React from 'react'
import PropTypes from 'prop-types'

const LegalTerms = ({isChecked, toggleCheck}) => (
  <div style={{padding: 20}}>
    <input id="chekbox" type="checkbox" value="legalTerms" checked={isChecked} onChange={() => toggleCheck(!isChecked)}/>
    <label htmlFor="checkbox">I agree with legal terms</label>
  </div>
)

LegalTerms.propTypes = {
  isChecked: PropTypes.bool.isRequired,
  toggleCheck: PropTypes.func.isRequired
}

export default LegalTerms