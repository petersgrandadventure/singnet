import { actionTypes } from '../actions/legalTerms'

const legalTerms = (state = false, action) => {
  switch (action.type) {
    case actionTypes.setLegalTerms:
      return action.payload
    default:
      return state
  }
}

export default legalTerms