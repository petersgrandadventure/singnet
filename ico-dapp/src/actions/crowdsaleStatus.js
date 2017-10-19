import AgiCrowdsale from '../contract'

export const checkCrowdsaleStatus = () => async (dispatch) => {
  try {
    dispatch(isLoading(true))
    const startTime = await AgiCrowdsale.startTime() * 1000
    const endTime = await AgiCrowdsale.endTime() * 1000
    const now = new Date().getTime()

    if (now < startTime) {
      dispatch(setCrowdsaleStatus(statusTypes.tooEarly))
    }

    if (now >= startTime && now <= endTime) {
      dispatch(setCrowdsaleStatus(statusTypes.open))
    }

    if (now > endTime) {
      dispatch(setCrowdsaleStatus(statusTypes.tooLate))
    }

    dispatch(isLoading(false))
  } catch(error) {
    dispatch(isLoading(false))
  }
}

export const setCrowdsaleStatus = (payload) => ({
  type: actionTypes.setStatus,
  payload
})

export const isLoading = (payload) => ({
  type: actionTypes.isLoading,
  payload
})

export const actionTypes = {
  isLoading: 'IS_LOADING',
  setStatus: 'SET_CROWDSALE_STATUS'
}

export const statusTypes = {
  open: 'OPEN',
  tooLate: 'TOO_LATE',
  tooEarly: 'TOO_EARLY'
}