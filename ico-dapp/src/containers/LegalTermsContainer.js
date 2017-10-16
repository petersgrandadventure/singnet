import React from 'react'
import { connect } from 'react-redux'
// actions
import setLegalTerms from '../actions/legalTerms'
// components
import LegalTerms from '../components/LegalTerms'

const LegalTermsContainer = ({ legalTerms, setLegalTerms }) => (
  <LegalTerms isChecked={legalTerms} toggleCheck={(bool) => setLegalTerms(bool)} />
)

const mapStateToProps = ({ legalTerms }) => ({ legalTerms })

export default connect(mapStateToProps, { setLegalTerms })(LegalTermsContainer)