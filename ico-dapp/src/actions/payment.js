const { web3 } = window

export const submitPayment = (account, amount) => (dispatch) => {
  web3.eth.sendTransaction(
    {
      from: account,
      to: "0xddd78c1a0eb35ab17cf54385604ef75bc6cfec8e",//web3.eth.accounts[1],
      value: web3.toWei(amount, "ether")
    },
    (err, res) => err ? dispatch(paymentRejected(err)) : dispatch(paymentSucceed(res))
  )
} 

export const paymentRejected = (payload) => ({
  type: actionTypes.paymentRejected,
  payload
})

export const paymentSucceed = (payload) => ({
  type: actionTypes.paymentSucceed,
  payload
})

export const actionTypes = {
  paymentSucceed: 'PAYMENT_SUCCEED',
  paymentRejected: 'PAYMENT_REJECTED'
}