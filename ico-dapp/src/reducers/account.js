import { actionTypes } from '../actions/account'

const { request, success, failure } = actionTypes

const account = (state = null, action) => {
  switch (action.type) {
    // case request: 
    //   return { ...state, isLoading: action.payload }
    // case success:
    //   return { ...state, address: action.payload }
    // case failure:
    //   return { ...state, address: null, error: action.payload }
    // default:
    //   return state
    case 'web3/RECEIVE_ACCOUNT':
      return action.address

    case 'web3/CHANGE_ACCOUNT':
      return action.address
    default:
      return state
  }
}

export default account