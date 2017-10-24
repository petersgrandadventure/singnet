import { actionTypes } from '../actions/payment'

const initialState = {
  error: null,
  response: null,
}

const payment = (state = initialState, action) => {
  switch (action.type) {
    case actionTypes.paymentSucceed:
      return {
        ...state,
        response: action.payload
      }

    case actionTypes.paymentRejected:
      return {
        ...state,
        error: action.payload
      }

    default:
      return state
  }
}

export default payment