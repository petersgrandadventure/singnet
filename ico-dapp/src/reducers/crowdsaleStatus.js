import { actionTypes } from '../actions/crowdsaleStatus'

const initialState = {
  isLoading: false,
  status: ''
}

const crowdsale = (state = initialState, action) => {
  switch (action.type) {
    case actionTypes.setStatus:
      return {
        ...state,
        status: action.payload
      }

    case actionTypes.isLoading:
      return {
        ...state,
        isLoading: action.payload
      }

    default:
      return state
  }
}

export default crowdsale