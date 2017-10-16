import { actionTypes } from '../actions/amount'

const amount = (state = { ether: 0, agi: 0 }, action) => {
  switch (action.type) {
    case actionTypes.setAmount:
      return action.payload
    default:
      return state
  }
}

export default amount