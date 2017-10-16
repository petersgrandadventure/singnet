import { combineReducers } from 'redux'
// reducers
import amount from './amount'
import account from './account'
import legalTerms from './legalTerms'

const rootReducer = combineReducers({
  amount,
  account,
  legalTerms
})

export default rootReducer