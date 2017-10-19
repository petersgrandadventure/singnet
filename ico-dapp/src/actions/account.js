export const actionTypes = {
  request: 'FETCH_ACCOUNT_REQUEST',
  success: 'FETCH_ACCOUNT_SUCCESS',
  failure: 'FETCH_ACCOUNT_FAILURE'
}

const isFetching = (payload) => {
  return {
    type: actionTypes.request,
    payload
  }
}

const fetchSuccess = (payload) => {
  return {
    type: actionTypes.success,
    payload
  }
}

const fetchFailure = (payload) => {
  return {
    type: actionTypes.failure,
    payload
  }
}

const fetchAccount = () => (dispatch) => {
  dispatch(isFetching(true))

  // TODO: call web3 and dispatch actions

  dispatch(isFetching(false))
}

export default fetchAccount