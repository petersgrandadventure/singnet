export const actionTypes = {
  setLegalTerms: 'SET_LEGAL_TERMS'
}

const setLegalTerms = (payload) => {
  return {
    type: actionTypes.setLegalTerms,
    payload
  }
}

export default setLegalTerms