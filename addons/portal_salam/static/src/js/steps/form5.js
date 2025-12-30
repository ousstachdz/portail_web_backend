class Form5 extends Component {
  static props = ['state']
  setup() {
    this.state = useState({
      formData: {
        password: '',
        confirm_password: '',
      },
    })
  }

  handleChange(event) {
    const { state } = this.props
    const { name, value } = event.target
    state.formData[name] = value
  }

  getBarColor(level) {
    switch (level) {
      case 1:
        return 'red'
      case 2:
        return 'orange'
      case 3:
        return 'yellow'
      case 4:
        return 'lightgreen'
      case 5:
        return 'green'
      default:
        return 'gray'
    }
  }

  static template = xml`
  <div class="d-flex flex-column align-items-center">
    <div class="col-12">

      <div class="bg-light p-3 rounded shadow-sm mb-4">
        <h5>إنشاء حساب</h5>
        <div class="row">
          <div class="col-md-6">
            <div class="form-group">
              <label for="password">كلمة السر</label>
              <input type="password" 
              class="form-control"
              id="password" 
              t-att-value="props.state.formData.password"
              name="password" 
              t-on-keyup="handleChange" 
              required="required"
              />
              <div class="level-indicator">
                <div class="level-indicator-bar" 
                     t-att-style="'width:' + (props.state.formData.passwordSecurityLevel * 20) + '%' + ';background-color:' + getBarColor(props.state.formData.passwordSecurityLevel)">
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="form-group">
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col-md-6">
            <div class="form-group">
              <label for="confirm_password">تأكيد كلمة السر</label>    
              <input type="password"
              class="form-control"
              id="confirm_password" 
              name="confirm_password" 
              t-att-value="props.state.formData.confirm_password"
              t-on-keyup="handleChange" 
              required="required"/>
            </div>
          </div>
          <div class="col-md-6">
            <div class="form-group">
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  `
}
