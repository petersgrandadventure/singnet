export const actionTypes = {
  setAmount: 'SET_AMOUNT'
}

const setAmount = (payload) => {
  return {
    type: actionTypes.setAmount,
    payload
  }
}

const ethToAgi = (amount) => (dispatch) => {
  // TODO: get conversion from contract
  dispatch(setAmount({ ether: amount, agi: amount * 100 }))
}

export default ethToAgi