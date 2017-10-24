import { combineReducers } from 'redux'
// reducers
import amount from './amount'
import account from './account'
import payment from './payment'
import legalTerms from './legalTerms'
import crowdsale from './crowdsaleStatus'

const rootReducer = combineReducers({
  amount,
  account,
  payment,
  crowdsale,
  legalTerms,
})

export default rootReducer