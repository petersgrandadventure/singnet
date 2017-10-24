import React from 'react'
import PropTypes from 'prop-types'

const reg = new RegExp('^[0-9]+$')

export default class Amount extends React.Component {
  state = { amount: '' }
  
  convert(event) {
    const { value } = event.target
    this.setState(
      { amount: value },
      () => this.props.convert(reg.test(this.state.amount) ? parseInt(this.state.amount) : 0)
    )
  }

  render() {
    const { amount: { agi } } = this.props
    return (
      <div>
        <input
          type="text"
          placeholder={'Eth'}
          style={{marginRight: 20}}
          value={this.state.amount}
          onChange={(event) => this.convert(event)}
        />
        <input
          type="text"
          disabled={true}
          placeholder='AGI'
          ref={(ref) => this._agi = ref}
          value={agi || ''}
        />
      </div>
    )
  }
}

Amount.propTypes = {
  convert: PropTypes.func.isRequired,
  amount: PropTypes.shape({
    agi: PropTypes.number.isRequired,
    ether: PropTypes.number.isRequired
  })
}